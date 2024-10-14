from django.contrib import admin

from .models import LipaNaMpesaOnline, PaymentTransaction

# Register your models here.

class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'TransID',
        'TransTime',
        'TransAmount',
        'BusinessShortCode',
        'BillRefNumber',
        'OrgAccountBalance',
        'MSISDN',
        'FirstName',
        
    ]

admin.site.register(LipaNaMpesaOnline)
admin.site.register(PaymentTransaction,  PaymentTransactionAdmin)