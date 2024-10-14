from django.urls import path

from base import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("privacy-policy/", views.PrivacyPolicy.as_view(), name="privacy-policy"),
    path("terms-of-use/", views.TermsOfUse.as_view(), name="terms-of-use"),
    path("cookies-policy/", views.CookiePolicy.as_view(), name="cookies-policy"),
    path("about/", views.about, name="about"),
    path("pay", views.payments, name="payments"),
]
