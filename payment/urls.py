from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import TransactionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    # path('invoice/<int:pk>', views.PaymentInvoice.as_view(), name='invoice'),
    path('payment/<str:invoice_number>/', views.PaymentGateway.as_view(), name='payment'),
    path('api/', include(router.urls)),
    path('package_details/<int:pk>/', views.PackageDetails.as_view(), name='package_details'),
    path('select_package/', views.package_selection, name='package_selection'),
]
