__author__ = 'justasic'
from django.contrib import admin
from NutmegCRM.apps.tickets.models import Ticket, Comment

class TicketAdmin(admin.ModelAdmin):
    list_display = ['customer']
    list_filter = ['item_model', 'date', 'item_manufacture']
    search_fields = ['item_model', 'item_manufacture', 'customer']
    date_heirachy = 'date'
    save_on_top = True
    #prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author']
    list_filter = ['author', 'created', 'ticket']
    search_fields = ['ticket', 'author']
    date_heirachy = 'created'
    save_on_top = True
    #prepopulated_fields = {"slug": ("title",)}

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment, CommentAdmin)