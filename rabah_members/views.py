from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from rabah_events.tasks import create_multiple_members
from rabah_members.forms import (
    MemberCreateForm,
    MemberEditForm,
    AddExistingMemberToFamilyForm,
    UpdateExistingMemberFamilyRelationShipForm,
    MemberUploadCreateForm, MemberInvitationForm, MemberInvitationAcceptForm,
)
from rabah_members.models import Member, FAMILY_RELATIONSHIP_CHOICES, MemberInvitation
from rabah_members.utils import query_members
from rabah_organisations.models import Group
from users.forms import UserProfileUpdateForm
from users.mixin import AuthAndAdminOrganizationMemberMixin, AuthAndOrganizationMixin
from users.models import User
from users.tasks import send_member_activate_account
from .utils import convert_file_to_dictionary, generate_qr_code


class MemberAutocompleteView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used for auto complete when searching members on the frontend
    """

    def get(self, request):
        query = request.GET.get("query", "")

        # Perform a simple case-insensitive search for members
        members = Member.objects.filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            & Q(organisation_id=self.organisation_id)
        )

        suggestions = [
            {
                "name": f"{member.user.first_name} {member.user.last_name}",
                "id": member.id,
                "image_url": member.user.user_profile.profileImageURL,
                "additional_info": member.family_relationship,
            }
            for member in members
        ]

        return JsonResponse(suggestions, safe=False)


class MembersDashboardView(AuthAndAdminOrganizationMemberMixin, ListView):
    """
    This is used to get all the members currently on breeze nd add members
    """

    template_name = "dashboard/members.html"
    queryset = Member.objects.all()
    paginate_by = 20
    context_object_name = "members"

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        query = self.request.GET.get("search")

        queryset = Member.objects.filter(organisation_id=self.organisation_id)
        ordering = self.get_ordering()
        if query:
            queryset = query_members(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create an instance of form and pass it to the context
        form = MemberUploadCreateForm(self.organisation_id)
        member_invitation_form = MemberInvitationForm(self.organisation_id)
        context["member_upload_create"] = form
        context["member_invitation_form"] = member_invitation_form
        return context


class GroupMembersView(AuthAndOrganizationMixin, ListView):
    """
    This is used to get members inside the group, same as members list HTML.
    """

    template_name = "dashboard/members.html"
    context_object_name = "members"
    form_class = MemberUploadCreateForm
    paginate_by = 20

    def get_queryset(self):
        organisation_id = self.organisation_id
        group_id = self.kwargs.get("group_id")

        group = Group.objects.filter(
            id=group_id, organisation_id=organisation_id
        ).first()
        if not group:
            # You may want to handle the case when the group does not exist
            return Member.objects.none()

        members = group.member_set.all()

        # Include search functionality
        query = self.request.GET.get("search")
        if query:
            members = query_members(item=members, query=query)

        return members

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the form to the context
        context["member_upload_create"] = self.form_class()

        return context


class MemberCreateView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to create members it the create  page with the member form
    """

    def get(self, request):
        organisation_id = self.organisation_id
        is_admin_user = Member.objects.is_admin_user(self.request.user, organisation_id)
        if not is_admin_user:
            return redirect(request.META.get("HTTP_REFERER"))
        form = MemberCreateForm(organisation_id)
        context = {"form": form}

        return render(request, "dashboard/add_member.html", context)

    def post(self, request):
        organisation_id = self.organisation_id
        form = MemberCreateForm(organisation_id, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "member created successfully")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return render(request, "dashboard/add_member.html", {"form": form})


class MemberUploadCreateView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to create the member using files for creating multiple users at once
    """

    def post(self, request):
        form = MemberUploadCreateForm(self.organisation_id, request.POST, request.FILES)
        if form.is_valid():
            member_file = form.cleaned_data.get("member_file")
            groups = form.cleaned_data.get("groups")
            data, header_dictionary = convert_file_to_dictionary(member_file)

            # Convert QuerySet to a serializable format
            groups_serializable = list(groups.values())

            # Ensure that the data is serializable
            data_serializable = [dict(item) for item in data]

            create_multiple_members.delay(
                data=data_serializable,
                organisation_id=self.organisation_id,
                groups=groups_serializable,
            )
            messages.success(request, "successfully upload member file")
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")
        return redirect(request.META.get("HTTP_REFERER"))


class MemberDetailView(AuthAndOrganizationMixin, View):
    """
    this is used to get the detail of a member and also update the member
    """

    def get(self, request, id):
        organisation_id = self.organisation_id
        member = Member.objects.filter(id=id).first()
        if not member:
            render(request, "404.html")

        member_form = MemberEditForm(self.organisation_id, instance=member)
        user_form = UserProfileUpdateForm(instance=member.user.user_profile)
        member_create_form = MemberCreateForm(organisation_id)
        add_existing_member_form = AddExistingMemberToFamilyForm(
            organisation_id=organisation_id, current_member_id=member.id
        )
        family_relationship_choices = FAMILY_RELATIONSHIP_CHOICES

        context = {
            "member": member,
            "member_form": member_form,
            "user_form": user_form,
            "member_create_form": member_create_form,
            "add_existing_member_form": add_existing_member_form,
            "family_relationship_choices": family_relationship_choices,
        }
        return render(request, "dashboard/members_detail.html", context)

    def post(self, request, id):
        member = Member.objects.filter(id=id).first()
        if not member:
            render(request, "404.html")
        member_form = MemberEditForm(self.organisation_id, instance=member, data=self.request.POST)
        if member_form.is_valid():
            member_form.save()
            messages.success(request, "successfully update member")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class AddFamilyMemberView(AuthAndOrganizationMixin, View):
    """
    this is used to add a family member to a member, which is a new member
    """

    def post(self, request, member_id):
        member = Member.objects.filter(id=member_id).first()

        if not member:
            return JsonResponse({"errors": ["member id not found "]})
        if not member.family:
            member.create_family()
        print("organisation_id:", self.organisation_id)
        form = MemberCreateForm(
            organisation_id=self.organisation_id, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            instance = form.save()
            #  add to the family
            instance.family = member.family
            instance.save()
            return JsonResponse(
                {"success": True, "message": "Successfully add member to family"}
            )
        else:
            # Return form errors in the JSON response
            errors_list = [
                error
                for field, error_list in form.errors.items()
                for error in error_list
            ]
            return JsonResponse({"errors": errors_list}, status=400)


class AddExistingMemberToFamilyView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to add existing member to a family
    """

    def post(self, request, member_id):
        member = Member.objects.filter(id=member_id).first()

        if not member:
            return JsonResponse({"errors": ["member id not found "]})
        if not member.family:
            member.create_family()

        form = AddExistingMemberToFamilyForm(
            organisation_id=self.organisation_id,
            current_member_id=member.id,
            data=request.POST,
        )
        if form.is_valid():
            result = form.save()
            if result:
                return JsonResponse(
                    {"success": True, "message": "Successfully add member to family"}
                )
            else:
                return JsonResponse(
                    {"errors": ["member already in family"]}, status=400
                )
        else:
            # Return form errors in the JSON response
            errors_list = [
                error
                for field, error_list in form.errors.items()
                for error in error_list
            ]
            return JsonResponse({"errors": errors_list}, status=400)


class UpdateExistingMemberFamilyRelationShipView(
    AuthAndAdminOrganizationMemberMixin, View
):

    def post(self, request):
        form = UpdateExistingMemberFamilyRelationShipForm(data=self.request.POST)
        if form.is_valid():
            result = form.save()
            if result:
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Successfully update family relationship",
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {"errors": ["Error updating family relationship"]}, status=400
                )
        else:
            # Return form errors in the JSON response
            errors_list = [
                error
                for field, error_list in form.errors.items()
                for error in error_list
            ]
            return JsonResponse({"errors": errors_list}, status=400)


class MemberAddLoginPermissionView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to add login permission to a member
    """

    def post(self, request, member_id):
        member = Member.objects.filter(id=member_id).first()
        if not member:
            return JsonResponse({"errors": ["member id not found "]})
        user = member.user
        token = user.generate_token()

        # Generate activation URL for the MemberCreatePasswordView
        activation_url = (
                request.build_absolute_uri(
                    reverse("user:member_create_password", kwargs={"token": token})
                )
                + f"?member_id={member_id}"
        )  # Pass member_id as a query parameter

        send_member_activate_account.delay(
            self.request.user.first_name,
            activation_url,
            member.user.email,
            member.user.first_name,
            member.user.last_name
        )
        messages.success(request, "Successfully send activation link to member")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class MemberInvitationCreateView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to create member invitation and also link to be shared to the user
    """

    def post(self, request):
        form = MemberInvitationForm(self.organisation_id, request.POST)
        if form.is_valid():
            instance = MemberInvitation.objects.invitation_exists(organisation_id=self.organisation_id,
                                                                  groups=form.cleaned_data['groups'])
            if not instance:
                instance = form.save(commit=False)
                instance.organisation_id = self.organisation_id
                instance.save()
                instance.groups.set(form.cleaned_data['groups'])

            url = reverse('rabah_members:member-accept-invitation', kwargs={'member_invitation_id': instance.id})
            url = f"{request.build_absolute_uri('/')}{url[1:]}"
            image = generate_qr_code(url)
            return JsonResponse({"success": True, "image": image, "url": url})
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")
        return JsonResponse({"success": True})


class MemberAcceptInvitationView(View):
    """
    this page is used by non-logged-in user that are invited
    """

    def get(self, request, member_invitation_id):
        form = MemberInvitationAcceptForm()
        context = {
            "form": form,
            "member_invitation_id": member_invitation_id

        }
        return render(request, "dashboard/member_invite.html", context)

    def post(self, request, member_invitation_id):
        user = None

        member_invitation = MemberInvitation.objects.filter(id=member_invitation_id).first()
        if not member_invitation:
            messages.error(request, "an invalid id is passed ")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        form = MemberInvitationAcceptForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            mobile = form.cleaned_data.get("mobile")
            address = form.cleaned_data.get("address")
            career = form.cleaned_data.get("career")
            email = form.cleaned_data.get("email")
            gender = form.cleaned_data.get("gender")
            date_of_birth = form.cleaned_data.get("date_of_birth")

            if email == "":
                email = None

            if email is not None:
                user = User.objects.filter(email=email).first()

            if not user:
                user = User.objects.create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    mobile=mobile
                )

            if Member.objects.filter(user=user,organisation_id=member_invitation.organisation.id).exists():
                messages.error(request, "user is already a member of this organisation")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            user_profile = user.user_profile
            user_profile.address = address
            user_profile.career = career
            user_profile.gender = gender
            user_profile.date_of_birth = date_of_birth
            user_profile.save()

            instance = Member()
            instance.user = user
            instance.organisation_id = member_invitation.organisation_id
            instance.save()
            instance.groups.set(member_invitation.groups.all())

            messages.success(request, "successfully join the organisation")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
