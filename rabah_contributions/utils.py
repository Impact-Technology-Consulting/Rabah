import operator
from functools import reduce

from django.db import models
from django.db.models import Q

from rabah_contributions.models import Contribution


def query_contributions(query, item):
    """
    this query list is used to filter item more of like a custom query the return the query set
    :param query:
    :param item:
    :return:
    """
    query_list = []
    query_list += query.split()
    query_list = sorted(query_list, key=lambda x: x[-1])
    query = reduce(
        operator.or_,
        (Q(member__user__email__icontains=x) |
         Q(method__icontains=f"{x}".upper()) |
         Q(description__icontains=x) |
         Q(member__user__first_name__icontains=x) |
         Q(member__user__last_name__icontains=x) |
         Q(member__user__first_name=[x]) for x in query_list)
    )
    object_list = item.filter(query).distinct()
    return object_list


def total_contribution_amount(organisation_id):
    try:
        contributions = Contribution.objects.filter(organisation_id=organisation_id)
        total_amount = contributions.aggregate(models.Sum('amount'))['amount__sum'] or 0
        return total_amount
    except:
        return 0
