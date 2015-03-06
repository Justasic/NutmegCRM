from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template.context import RequestContext
from NutmegCRM.apps.crm.models import Customer
from NutmegCRM.apps.tickets.models import Ticket

# Create your views here.

def index(request):
    customers = Customer.objects.all();
    ctx = RequestContext(request, {'customers': customers})

    return render_to_response('crm/index.html', ctx)

def info(request, lastname, firstname):

    # Get our info or 404.
    customer = get_object_or_404(Customer, first_name__iexact=firstname, last_name__iexact=lastname)
    tickets = Ticket.objects.filter(customer_id=customer.id)

    ctx = RequestContext(request, {
        'tickets': tickets,
        'customer': customer,
    })

    # Render our template with our info.
    return render_to_response('crm/customer.html', ctx)