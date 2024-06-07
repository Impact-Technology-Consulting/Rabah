from rabah_organisations.models import Organisation


def context_processor(request):
    global sub_organisations

    if request.COOKIES.get("parent_organisation_id"):
        sub_organisations = Organisation.objects.filter(parent_id=request.COOKIES.get("parent_organisation_id"))
        print("Sub Organisations ", sub_organisations)
        print("Sub Organisations ", request.COOKIES.get("parent_organisation_id"))
        return {
            "sub_organisations": sub_organisations,
        }
    print("No Sub Organisations ")
    return {

    }
