from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from NutmegCRM.apps.crm.models import Customer
from NutmegCRM.apps.tickets.models import Ticket

# Create your views here.

def index(request):
    customers = Customer.objects.all();
    ctx = RequestContext(request, {'customers': customers})

    return render_to_response('crm/index.html', ctx)