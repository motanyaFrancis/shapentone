import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets

from authentication.models import SubscriptionSetup, UserSubscription
from myRequest.api.lipaNaMpesa import lipa_na_mpesa
from payment.forms import *
from payment.models import PaymentTransaction
from payment.serializers import TransactionSerializer


class PaymentInvoice(View):
    template_name = 'invoice.html'

    def get(self, request, pk):
        subscription = UserSubscription.objects.get(pk=pk)
        context = {
            'subscription': subscription
        }
        return render(request, self.template_name, context)


class PaymentGateway(View):
    template_name = 'payment.html'
    # form_class = InvoiceCreationForm()

    def get(self, request, invoice_number):
        
        subscription = get_object_or_404(
            UserSubscription, invoice_no=invoice_number)
        
        context = {
            'subscription': subscription,
            
        }
        return render(request, self.template_name, context)

    def post(self, request, invoice_number):
        if request.method == 'POST':
            try:

                # phone_number = "254719397014"/
                phone_number = request.POST.get('phoneNumber')
                float_amount = float(request.POST.get('amount'))
                amount = int(float_amount)
                account_reference = request.POST.get('account_reference')
                transaction_desc = "GYM"
                print(phone_number, amount, account_reference)

                is_secure = request.is_secure()

                callback_url = request.build_absolute_uri(
                    reverse('mpesa_stk_push_callback'))
                if not is_secure and callback_url.startswith('https://'):
                    callback_url = 'https://www.shapentone360.com/api/transactions/'
                   # callback_url = 'https://' + callback_url[len('http://'):]

                print("callback_url: ", callback_url)

                response = lipa_na_mpesa(
                    amount, phone_number, callback_url, account_reference, transaction_desc)
                print("response: ", response)
                print(" ")

                return redirect("payment", invoice_number=invoice_number)
            except Exception as e:
                print(e)
                # logger.error("Payment initiation failed. Error: %s", e)
                return redirect("index")


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = PaymentTransaction.objects.all()
    serializer_class = TransactionSerializer

    logger = logging.getLogger('payment')

    def list(self, request, *args, **kwargs):
        
        response = self.queryset() 
        
        self.logger.info(f"API response: {response.content}")


def package_details(request):
    return render(request, 'package_details.html')


@method_decorator(login_required, name='dispatch')
class PackageDetails(View):
    template_name = 'package_details.html'

    def get(self, request, pk):
        package = get_object_or_404(SubscriptionSetup, pk=pk)

        return render(request, self.template_name, {'package': package})


@login_required
def package_selection(request):
    if request.method == 'POST':
        package_id = request.POST.get('package')
        package = get_object_or_404(SubscriptionSetup, id=package_id)
        invoice, created = UserSubscription.objects.update_or_create(
            subscription=package,
            user=request.user,
           
        )

        if created:
            invoice.init_rec()  # This will set the invoice_no
            invoice.save()

        return redirect('payment', invoice_number=invoice.invoice_no)
    else:

        return redirect('package_details', package_id)
