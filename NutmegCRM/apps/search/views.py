__author__ = 'justasic'
from NutmegCRM.apps.crm.models import Customer
from NutmegCRM.apps.tickets.models import Ticket


def search_helper(count, query):
    import itertools
    model_list = Customer.objects.filter(title__icontains=query, status=1)

    for L in range(1, count+1):
        for subset in itertools.permutations(query, L):
            count1 = 1
            query1 = subset[0]
            while count1 != len(subset):
                query1 = query1 + " " + subset[count1]
                count1 += 1
            model_list = Customer.objects.filter(title__icontains=query1, status=1)

    return model_list.distinct()