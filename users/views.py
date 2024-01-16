from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from rabah_organisations.models import Organisation
from users.forms import UserProfileUpdateForm, ChangePasswordForm, RabahSignupForm, RabahLoginForm
from users.mixin import AuthAndOrganizationMixin
from users.models import User, UserProfile


# Create your views here.

class RabahSignupView(View):
    template_name = 'account/signup.html'

    def get(self, request):
        # if the user is authenticated, redirect the user to dashboard page
        if self.request.user.is_authenticated:
            return redirect("rabah_dashboard:dashboard")
        form = RabahSignupForm()
        return render(request, "account/signup.html", {"form": form})

    def post(self, request):
        form = RabahSignupForm(self.request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            organisation_name = form.cleaned_data.get("organisation_name")
            password = form.cleaned_data.get("password1")
            confirm_password = form.cleaned_data.get("password2")
            if password != confirm_password:
                form.add_error("password", "Password and confirm password must be the same")

            if User.objects.filter(email=email).exists():
                form.add_error("email", "User with this email already exists")
            else:
                # create the user
                user = User.objects.create(email=email, last_name=last_name, first_name=first_name)
                user.set_password(password)
                user.save()
                if not user:
                    return render(request, "account/signup.html", {"form": form})

                organisation = Organisation.objects.create(name=organisation_name, owner=user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("rabah_dashboard:dashboard")

        return render(request, "account/signup.html", {"form": form})


class RabahLoginView(View):
    template_name = 'account/login.html'

    def get(self, request):
        form = RabahLoginForm()
        # if the user is authenticated, redirect the user to dashboard page
        if self.request.user.is_authenticated:
            return redirect("rabah_dashboard:dashboard")
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RabahLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            # Check if the user exists
            user = User.objects.filter(email=email).first()
            if not user:
                form.add_error(None, "User with this email does not exist")
            else:
                # Check if the password is correct
                if check_password(password, user.password):

                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # redirect to the dashboard
                    return redirect("rabah_dashboard:dashboard")
                else:
                    form.add_error("password", "Invalid password")
        return render(request, self.template_name, {'form': form})


class CustomLogout(View):
    def get(self, request):
        logout(request)
        return redirect('account_login')  # Redirect to the desired URL after logout


class UserProfileView(LoginRequiredMixin, View):
    """
    this is used to get the user profile and also update it
    """

    def get(self, request):
        user_profile = self.request.user.user_profile
        form = UserProfileUpdateForm(instance=user_profile)
        change_form = ChangePasswordForm()
        context = {
            "form": form,
            "change_form": change_form,
            "user_profile": user_profile,
        }
        return render(request, "dashboard/user_profile.html", context)

    def post(self, request):
        user_profile = self.request.user.user_profile
        form = UserProfileUpdateForm(data=self.request.POST, files=self.request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MemberUserProfileUpdateView(AuthAndOrganizationMixin, View):
    """
    Used on the member edit page to edit the member info

    """

    def post(self, request, profile_id):
        user_profile = UserProfile.objects.filter(id=profile_id).first()
        if not user_profile:
            messages.error(request, "profile does not exists")
        form = UserProfileUpdateForm(data=self.request.POST, files=self.request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.info(request, "member info successfully updated")
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"Error in {field}: {error}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeUserPassword(LoginRequiredMixin, View):

    def post(self, request):
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            if password != confirm_password:
                messages.error(request, "Password does not match")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user = self.request.user
            user.set_password(password)
            user.save()
            user = authenticate(request, username=user.username, password=password,
                                backend='django.contrib.auth.backends.ModelBackend')
            if user is not None:
                login(request, user)
            messages.info(request, "Successfully Update password")
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
