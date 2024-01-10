from django.urls import path
from .. import views


urlpatterns = [
    path("user/", views.MembershipViews.as_view(), name="user-membership"),
]
