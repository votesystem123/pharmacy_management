from django.contrib import admin
from dashboard.models import AiUser, suppiler, Medicine, Customer, Invoice, InvoiceItem
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group),
admin.site.register(AiUser),
admin.site.register(suppiler),
admin.site.register(Medicine),
admin.site.register(Customer),
admin.site.register(Invoice),
admin.site.register(InvoiceItem),


