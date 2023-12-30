from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from rabah_members.forms import MemberCreateForm, MemberEditForm, AddExistingMemberToFamilyForm, \
    UpdateExistingMemberFamilyRelationShipForm
from rabah_members.models import Member, FAMILY_RELATIONSHIP_CHOICES
from rabah_members.utils import query_members
from users.forms import UserProfileUpdateForm
from users.mixin import AuthAndAdminOrganizationMemberMixin, AuthAndOrganizationMixin


class MemberAutocompleteView(AuthAndAdminOrganizationMemberMixin, View):
    def get(self, request):
        query = request.GET.get('query', '')

        # Perform a simple case-insensitive search for members
        members = Member.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) &
                                        Q(organisation_id=self.organisation_id))

        suggestions = [{"name": f"{member.user.first_name} {member.user.last_name}", "id": member.id,
                        "image_url": member.user.user_profile.profileImageURL,
                        "additional_info": member.family_relationship} for member in
                       members]

        return JsonResponse(suggestions, safe=False)


class MembersDashboardView(AuthAndAdminOrganizationMemberMixin, ListView):
    """
    This is used to get all the members currently on breeze nd add members
    """
    template_name = "dashboard/members.html"
    queryset = Member.objects.all()
    paginate_by = 5
    context_object_name = "members"

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        query = self.request.GET.get('search')

        queryset = Member.objects.filter(organisation_id=self.organisation_id)
        ordering = self.get_ordering()
        if query:
            queryset = query_members(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class AdminAddMemberPageView(AuthAndAdminOrganizationMemberMixin, View):

    def get(self, request):
        organisation_id = self.organisation_id
        is_admin_user = Member.objects.is_admin_user(self.request.user, organisation_id)
        if not is_admin_user:
            return redirect(request.META.get('HTTP_REFERER'))
        form = MemberCreateForm(organisation_id)
        context = {
            "form": form
        }

        return render(request, "dashboard/add_member.html", context)

    def post(self, request):
        organisation_id = self.organisation_id
        form = MemberCreateForm(organisation_id, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "member created successfully")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, "dashboard/add_member.html", {'form': form})


class GroupMembersView(AuthAndOrganizationMixin, View):
    """
    this is used to create members inside the group detail page
    """

    def get(self, request, group_id):
        organisation_id = self.organisation_id
        members = Member.objects.filter(organisation_id=organisation_id)
        context = {
            "members": members,
        }
        return render(request, "dashboard/members.html", context)


class MemberDetailView(AuthAndOrganizationMixin, View):
    """
    this is used to get the detail of a member and also update the member
    """

    def get(self, request, id):
        organisation_id = self.organisation_id
        member = Member.objects.filter(id=id).first()
        if not member:
            render(request, "404.html")

        member_form = MemberEditForm(instance=member)
        user_form = UserProfileUpdateForm(instance=member.user.user_profile)
        member_create_form = MemberCreateForm(organisation_id)
        add_existing_member_form = AddExistingMemberToFamilyForm(organisation_id=organisation_id,
                                                                 current_member_id=member.id)
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
        member_form = MemberEditForm(instance=member, data=self.request.POST)
        if member_form.is_valid():
            member_form.save()
            messages.success(request, "successfully update member")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
        form = MemberCreateForm(organisation_id=self.organisation_id, data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save()
            #  add to the family
            instance.family = member.family
            instance.save()
            return JsonResponse({"success": True, "message": "Successfully add member to family"})
        else:
            # Return form errors in the JSON response
            errors_list = [error for field, error_list in form.errors.items() for error in error_list]
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

        form = AddExistingMemberToFamilyForm(organisation_id=self.organisation_id, current_member_id=member.id,
                                             data=request.POST)
        if form.is_valid():
            result = form.save()
            if result:
                return JsonResponse({"success": True, "message": "Successfully add member to family"})
            else:
                return JsonResponse({"errors": ["member already in family"]}, status=400)
        else:
            # Return form errors in the JSON response
            errors_list = [error for field, error_list in form.errors.items() for error in error_list]
            return JsonResponse({"errors": errors_list}, status=400)


class UpdateExistingMemberFamilyRelationShipView(AuthAndAdminOrganizationMemberMixin, View):

    def post(self, request):
        form = UpdateExistingMemberFamilyRelationShipForm(data=self.request.POST)
        if form.is_valid():
            result = form.save()
            if result:
                return JsonResponse({"success": True, "message": "Successfully update family relationship"}, status=200)
            else:
                return JsonResponse({"errors": ["Error updating family relationship"]}, status=400)
        else:
            # Return form errors in the JSON response
            errors_list = [error for field, error_list in form.errors.items() for error in error_list]
            return JsonResponse({"errors": errors_list}, status=400)
