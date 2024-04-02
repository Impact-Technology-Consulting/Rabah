from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from django.views.generic import ListView

from users.mixin import AuthAndAdminOrganizationMemberMixin
from .forms import GroupForm  # Replace with the actual import path
from .models import Group  # Replace with the actual import path
from .utils import query_groups  # Replace with the actual import path for query_groups


class GroupListView(AuthAndAdminOrganizationMemberMixin, ListView):
    template_name = "dashboard/groups.html"
    model = Group
    context_object_name = "groups"
    paginate_by = 5

    def get_queryset(self):
        organisation_id = self.organisation_id
        queryset = Group.objects.filter(organisation_id=organisation_id)
        query = self.request.GET.get("search")

        if query:
            queryset = query_groups(item=queryset, query=query)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GroupForm(self.organisation_id)
        return context

    def post(self, request, *args, **kwargs):
        organisation_id = self.organisation_id
        form = GroupForm(organisation_id, request.POST, request.FILES)
        if form.is_valid():
            group = form.save()
            messages.success(request, "Group created successfully")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return render(request, "dashboard/groups.html", {"form": form})


class GroupUpdateView(AuthAndAdminOrganizationMemberMixin, View):

    def post(self, request, id):
        organisation_id = self.organisation_id
        group = Group.objects.filter(organisation_id=organisation_id, id=id).first()
        if not group:
            return redirect(request.META.get("HTTP_REFERER"))
        form = GroupForm(organisation_id, request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group updated successfully")
        return redirect(request.META.get("HTTP_REFERER"))


class GroupDetailView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to  get the detail of a group
    """

    def get(self, request, id):
        organisation_id = self.organisation_id
        group = Group.objects.filter(organisation_id=organisation_id, id=id).first()
        if not group:
            return redirect(request.META.get("HTTP_REFERER"))
        members = group.member_set.all()
        group_update_form = GroupForm(organisation_id, instance=group)
        context = {
            "group": group,
            "members": members,
            "group_update_form": group_update_form,
        }
        return render(request, "dashboard/group_detail.html", context)


class GroupDeleteView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to delete a group
    """

    def get(self, request, id):
        organisation_id = self.organisation_id
        group = Group.objects.filter(organisation_id=organisation_id, id=id).first()
        if not group:
            return redirect(request.META.get("HTTP_REFERER"))
        group.delete()
        return redirect(request.META.get("HTTP_REFERER"))
