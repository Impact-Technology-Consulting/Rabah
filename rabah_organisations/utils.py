import operator
from functools import reduce

from django.db.models import Q


def query_groups(query, item):
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
        (Q(name__icontains=x) |
         Q(name=[x]) for x in query_list)
    )
    object_list = item.filter(query).distinct()
    return object_list
