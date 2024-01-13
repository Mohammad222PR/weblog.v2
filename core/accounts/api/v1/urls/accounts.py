from django.urls import path
from accounts.api.v1 import views

urlpatterns = [
    # ACCOUNT REGISTRATION
    path("register", views.RegisterView.as_view(), name="register"),
    path(
        "activation/confirm/<str:token>",
        views.ActivateVerificationView.as_view(),
        name="verify",
    ),
    path("activation/resend", views.ResendActivationTokenView.as_view(), name="resend"),
]
