import operator
from functools import reduce

from django.db.models import Q


def query_member_attendance(search, item):
    """
    This query list is used to filter items more like a custom query that returns the queryset.
    :param search:
    :param status:
    :param item:
    :return:
    """
    query_list = search.split() if search else []
    query_list = sorted(query_list, key=lambda x: x[-1])

    # Build the Q object for search
    search_query = reduce(
        operator.or_,
        (Q(user__email__icontains=x) |
         Q(user__first_name__icontains=x) |
         Q(user__last_name__icontains=x) |
         Q(user__first_name=[x]) for x in query_list)
    ) if query_list else Q()

    # Combine both search and status queries with AND condition
    query = search_query & status_query

    object_list = item.filter(query).distinct()
    return object_list
