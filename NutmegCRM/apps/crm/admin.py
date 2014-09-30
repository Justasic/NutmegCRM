from django.contrib import admin
from NutmegCRM.apps.crm.models import Customer

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name']
    list_filter = ['first_name', 'created', 'last_name']
    search_fields = ['first_name', 'last_name', 'email']
    date_heirachy = 'created'
    save_on_top = True
    #prepopulated_fields = {"slug": ("title",)}

admin.site.register(Customer, CustomerAdmin)