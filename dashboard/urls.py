from django.urls import path

from dashboard import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('workout/<slug:slug>/', views.WorkoutDetailView.as_view(), name='workout'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('program/<int:pk>/', views.ProgramDetailsView.as_view(), name='program_details'),
]
