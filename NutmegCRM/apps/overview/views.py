__author__ = 'justasic'
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from NutmegCRM.apps.crm.models import Customer
from NutmegCRM.apps.tickets.models import Ticket, Comment

def index(request):

    customers = Customer.objects.all()

    # get various statistical totals

    ctx = RequestContext(request, {
        'customers': customers,
        'ttotal': Ticket.objects.count(), # Total ticket count
        'ctotal': Customer.objects.count(), # Customer count
        'qtotal': Ticket.objects.filter(status='0').count(), # Total tickets in queue
        'testtotal': Ticket.objects.filter(status='2').count(), # Total tickets which are in testing
        'comptotal': Ticket.objects.filter(status='3').count(), # Total tickets completed
    })

    return render_to_response('index.html', ctx)