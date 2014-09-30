__author__ = 'justasic'
from django.db import models
from django.contrib.auth.models import User
from apps.crm.models import Customer


class Ticket(models.Model):
    """
    This is the ticket model used for customer tickets.
    The ticket crm is fairly simple. You have customer information linked in the CRM crm
    then it links the contact info to this ticket model. The ticket model allows for unlimited
    pictures and comments while keeping it linked to the customer's information.
    This allows us to view previous customer repairs.

    This ticket is analogous to an invoice
    """
    # Date the ticket was filed
    date = models.DateTimeField(auto_now_add=True)
    # Current status of item
    status = models.CharField(max_length=1, choices=('queued', 'in-shop', 'testing', 'completed'))
    # The model of the item
    item_model = models.CharField(max_length=255)
    # The manufacture of the item
    item_manufacture = models.CharField(max_length=255)
    # The customer
    customer = models.ForeignKey(Customer)

    class Admin:
        pass


class Comment(models.Model):
    """
    The comment class allows for each ticket to have comments attached. This allows
    us to comment on a particular issue related to the item in the invoice.
    """
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    body = models.TextField()
    ticket = models.ForeignKey(Ticket)

    def __unicode__(self):
        return u"%s: %s" % (self.ticket, self.ticket.customer.first_name)

    class Admin:
        pass