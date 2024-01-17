from django.shortcuts import redirect

from rabah_members.models import Member, Organisation


class AuthAndOrganizationMixin:
    """
    Mixin to check for authentication and organization ID in cookies.
    """

    organisation_id = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        self.organisation_id = request.COOKIES.get("organisation_id")

        if not self.organisation_id:
            return redirect("rabah_dashboard:user_organisations")

        organisation = Organisation.objects.filter(id=self.organisation_id).first()

        if not organisation:
            return redirect("rabah_dashboard:user_organisations")
        member = Member.objects.is_admin_user(request.user, self.organisation_id)
        if not member:
            return redirect("rabah_dashboard:user_organisations")
        return super().dispatch(request, *args, **kwargs)


class AuthAndAdminOrganizationMemberMixin:
    """
    Mixin to check for authentication and organization ID in cookies.
    """

    organisation_id = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        self.organisation_id = request.COOKIES.get("organisation_id")

        if not self.organisation_id:
            return redirect("rabah_dashboard:user_organisations")

        organisation = Organisation.objects.filter(id=self.organisation_id).first()

        if not organisation:
            return redirect("rabah_dashboard:user_organisations")

        is_admin = Member.objects.is_admin_user(request.user, self.organisation_id)

        if not is_admin:
            return redirect("rabah_dashboard:user_organisations")

        return super().dispatch(request, *args, **kwargs)


class AuthAndAdminOrganizationNotSubscribedMixin:
    """
    Mixin to check for authentication and organization ID in cookies.
    """

    organisation_id = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        self.organisation_id = request.COOKIES.get("organisation_id")

        if not self.organisation_id:
            return redirect("rabah_dashboard:user_organisations")

        organisation = Organisation.objects.filter(id=self.organisation_id).first()

        if not organisation:
            return redirect("rabah_dashboard:user_organisations")

        is_admin = Member.objects.is_admin_user(request.user, self.organisation_id)

        if not is_admin:
            return redirect("rabah_dashboard:user_organisations")

        return super().dispatch(request, *args, **kwargs)
