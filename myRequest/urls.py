from django.urls import path

from myRequest import views

urlpatterns = [
    path("payments/",views.LipaNaMpesaAPIView.as_view(),name="mpesa_stk_push_callback"),
]