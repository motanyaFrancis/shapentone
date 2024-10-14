
from django.urls import path

from authentication import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('registration/success/', views.signup_success, name='registration_success'),
    path('account-verified/', views.account_verified, name='account_verified'),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path("login/", views.LoginRequest.as_view(), name="login"),
    path("logout/", views.logout_request, name="logout"),
    
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/settings/", views.UpdateProfile.as_view(), name="user_settings"),
    # path('settings/update_profile/', views.UpdateProfile.as_view(), name="update-profile"),
    path(
        "settings/password_change/",
        views.PasswordChange.as_view(),
        name="password_change",
    ),
    # path('create_invoice', views.InvoiceCreateView.as_view(), name='create_invoice' ),
    path('create_user_program/', views.CreateUserProgramView.as_view(), name='create_user_program'),
    path('intake_questionare/', views.Intake.as_view(), name='intake_questionare'),
    path('auth/', views.auth, name='auth'),
]
