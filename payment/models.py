from django.db import models


class LipaNaMpesaOnline(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, blank=True, null=True)
    MerchantRequestID = models.CharField(max_length=20, blank=True, null=True)
    ResultCode = models.IntegerField(blank=True, null=True)
    ResultDesc = models.CharField(max_length=120, blank=True, null=True)
    Amount = models.FloatField(blank=True, null=True)
    MpesaReceiptNumber = models.CharField(max_length=15, blank=True, null=True)
    TransactionDate = models.DateTimeField(blank=True, null=True)
    PhoneNumber = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return f"{self.PhoneNumber} has sent {self.Amount} >> {self.MpesaReceiptNumber}"


class PaymentTransaction(models.Model):
    """
    Represents a Pay Bill transaction.
    """
    # Transaction details
    # TransID = models.CharField(max_length=20, unique=True)
    TransID = models.CharField(max_length=20, unique=True)
    TransTime = models.CharField(max_length=20)
    TransAmount = models.DecimalField(max_digits=10, decimal_places=2)

    # Business details
    BusinessShortCode = models.CharField(max_length=10)
    BillRefNumber = models.CharField(max_length=20)
    InvoiceNumber = models.CharField(max_length=20, blank=True, null=True)
    OrgAccountBalance = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    # Customer details
    ThirdPartyTransID = models.CharField(max_length=20, blank=True, null=True)
    MSISDN = models.CharField(max_length=15)
    FirstName = models.CharField(max_length=50)
    MiddleName = models.CharField(max_length=50, blank=True, null=True)
    LastName = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Transaction ID: {self.TransID} - Amount: {self.TransAmount}"

    class Meta:
        verbose_name_plural = "Payment Transactions"
