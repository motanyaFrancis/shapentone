from django.shortcuts import redirect, render
# from authentication.forms import InvoiceForm
from django.urls import reverse
from django.views.generic import ListView

from articles.models import Article
from authentication.models import SubscriptionSetup
from myRequest.api.lipaNaMpesa import lipa_na_mpesa
from setup.models import Policy

# Create your views here.


class IndexView(ListView):
    template_name = "index.html"
    queryset = Article.objects.all().order_by("date_created")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["posts"] = self.queryset.reverse()[:3]
        context["subscriptions"] = SubscriptionSetup.objects.order_by("amount")
        # context['create_invoice_form'] = InvoiceForm(prefix='invoice_form')

        return context


def about(request):
    return render(request, "about.html")


class PrivacyPolicy(ListView):
    template_name = "privacy-policy.html"
    queryset = Policy.objects.filter(title="Privacy Policy")
    context_object_name = "policy"

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicy, self).get_context_data(**kwargs)
        return context


class TermsOfUse(ListView):
    template_name = "terms-of-use.html"
    queryset = Policy.objects.filter(title="Terms of Use")
    context_object_name = "policy"

    def get_context_data(self, **kwargs):
        context = super(TermsOfUse, self).get_context_data(**kwargs)
        return context


class CookiePolicy(ListView):
    template_name = "cookie-policy.html"
    queryset = Policy.objects.filter(title="Cookie Policy")
    context_object_name = "policy"

    def get_context_data(self, **kwargs):
        context = super(CookiePolicy, self).get_context_data(**kwargs)
        return context


def payments(request):
    if request.method == "GET":
        try:
            # logger = logging.getLogger("selfservice")
            # logger.info("Payment initiated. Request Headers: %s", request.headers)

            phone_number = "254719397014"
            amount = 1
            account_reference = "Victor Fitness"
            transaction_desc = "Subscription"

            is_secure = request.is_secure()

            callback_url = request.build_absolute_uri(
                reverse("mpesa_stk_push_callback")
            )
            if not is_secure and callback_url.startswith("http://"):
                callback_url = "https://" + callback_url[len("http://") :]

            print("callback_url: ", callback_url)

            response = lipa_na_mpesa(
                amount, phone_number, callback_url, account_reference, transaction_desc
            )
            print("response: ", response)
            print("     ")

            return redirect("index")
        except Exception as e:
            print(e)
            # logger.error("Payment initiation failed. Error: %s", e)
            return redirect("index")
