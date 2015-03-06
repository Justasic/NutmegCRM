__author__ = 'justasic'
from django.shortcuts import render_to_response, render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from NutmegCRM.apps.crm.models import Customer
from NutmegCRM.apps.tickets.models import Ticket, Comment
from django.template.context import RequestContext

def index(request):

    ctx = RequestContext(request, {})
    return render_to_response('tickets/index.html', ctx)

# Display a ticket and it's comments!
def ticket(request, invoiceid):

    # Get the customer's ticket and their information if we can, otherwise just 404.
    ticket = get_object_or_404(Ticket, pk=invoiceid)

    # Get the comments for the ticket as well
    comments = Comment.objects.filter(ticket=ticket)

    # Create a template context and then let Django handle the rest in the templates! :D
    ctx = RequestContext(request, {
        'ticket': ticket,
        'customer': ticket.customer,
        'comments': comments,
    })

    return render_to_response('tickets/ticket.html', ctx)


def newticket(request):
    pass