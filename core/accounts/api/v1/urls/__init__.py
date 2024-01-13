from django.urls import path, include

app_name = "api-v1"

urlpatterns = [
    path("profile/", include("accounts.api.v1.urls.profile")),
    path("obtain/token/", include("accounts.api.v1.urls.obtaintoken")),
    path("accounts/", include("accounts.api.v1.urls.accounts")),
    path("membership/", include("accounts.api.v1.urls.buy_membership")),
]
