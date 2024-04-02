from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from rabah_contributions.forms import ContributionForm, ContributionTypeForm
from rabah_contributions.models import ContributionType, Contribution
from rabah_contributions.utils import query_contributions
from rabah_members.utils import get_member
from users.mixin import AuthAndAdminOrganizationMemberMixin


# Create your views here.


class ContributionTypeView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to create the contribution type
    """

    def get(self, request):
        contribution_types = ContributionType.objects.filter(
            organisation_id=self.organisation_id
        )

        # Paginate the contribution types
        page = request.GET.get("page", 1)
        paginator = Paginator(
            contribution_types, 10
        )  # Show 10 contribution types per page

        try:
            contribution_types = paginator.page(page)
        except PageNotAnInteger:
            contribution_types = paginator.page(1)
        except EmptyPage:
            contribution_types = paginator.page(paginator.num_pages)

        form = ContributionTypeForm()
        context = {
            "form": form,
            "contribution_types": contribution_types,
        }
        return render(request, "dashboard/contribution_type.html", context)

    def post(self, request):
        form = ContributionTypeForm(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.organisation_id = self.organisation_id
            instance.save()
            messages.success(
                self.request, "Contribution type has been added successfully"
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            # Loop through form errors and add them as error messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error occurred in {field}: {error}")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ContributionTypeUpdateView(AuthAndAdminOrganizationMemberMixin, View):

    def post(self, request, contribution_type_id):
        instance = ContributionType.objects.filter(
            organisation_id=self.organisation_id, id=contribution_type_id
        ).first()
        if not instance:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        form = ContributionTypeForm(data=self.request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Update Contribution type")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error occurred in {field}: {error}")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ContributionTypeDeleteView(AuthAndAdminOrganizationMemberMixin, View):

    def get(self, request, contribution_type_id):
        instance = ContributionType.objects.filter(
            organisation_id=self.organisation_id, id=contribution_type_id
        ).first()
        if not instance:
            messages.error(request, "Invalid Contribution type ")
        else:
            instance.delete()
            messages.success(request, "Successfully deleted contribution type")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class GivingContributionView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to add giving transactions for members which you can easily
    track the amount a use have currently given out
    """

    def get(self, request):
        form = ContributionForm()

        context = {"form": form}
        return render(request, "dashboard/giving_transaction.html", context)

    def post(self, request):
        member = get_member(self.request.user, self.organisation_id)

        form = ContributionForm(data=self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by_id = member.id
            instance.organisation_id = member.organisation_id
            instance.save()
            messages.success(self.request, "Transaction has been added successfully")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            # Loop through form errors and add them as error messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error occurred in {field}: {error}")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ContributionsView(AuthAndAdminOrganizationMemberMixin, View):
    def get(self, request, contribution_type_id):
        query = self.request.GET.get("query")
        contribution_type = ContributionType.objects.filter(
            id=contribution_type_id
        ).first()

        if not contribution_type:
            messages.error(request, "No contribution type")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        contributions = Contribution.objects.filter(
            contribution_type=contribution_type, organisation_id=self.organisation_id
        )

        # Apply search query if provided
        if query:
            contributions = query_contributions(query=query, item=contributions)

        # Pagination logic
        page = request.GET.get("page", 1)
        paginator = Paginator(contributions, 10)  # Show 10 contributions per page

        try:
            contributions = paginator.page(page)
        except PageNotAnInteger:
            contributions = paginator.page(1)
        except EmptyPage:
            contributions = paginator.page(paginator.num_pages)

        context = {
            "contributions": contributions,
            "contribution_type": contribution_type,
        }
        return render(request, "dashboard/contributions.html", context)

    def post(self, request):
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ContributionDeleteView(AuthAndAdminOrganizationMemberMixin, View):

    def get(self, request, contribution_id):
        instance = Contribution.objects.filter(
            organisation_id=self.organisation_id, id=contribution_id
        ).first()
        if not instance:
            messages.error(request, "Invalid Contribution  ")
        else:
            instance.delete()
            messages.success(request, "Successfully deleted contribution ")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ContributionUpdateView(AuthAndAdminOrganizationMemberMixin, View):

    def get(self, request, contribution_id):
        contribution = Contribution.objects.filter(id=contribution_id).first()
        if not contribution:
            messages.error(request, "Contribution with this id does not exists ")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        form = ContributionForm(instance=contribution)
        contribution = contribution
        context = {"form": form, "contribution": contribution}
        return render(request, "dashboard/giving_transaction.html", context)

    def post(self, request, contribution_id):
        member = get_member(self.request.user, self.organisation_id)
        contribution = Contribution.objects.filter(id=contribution_id).first()
        if not contribution:
            messages.error(request, "Contribution with this id does not exists ")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        form = ContributionForm(data=self.request.POST, instance=contribution)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.organisation_id = member.organisation_id
            instance.save()
            messages.success(self.request, "Transaction has been added successfully")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            # Loop through form errors and add them as error messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error occurred in {field}: {error}")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
