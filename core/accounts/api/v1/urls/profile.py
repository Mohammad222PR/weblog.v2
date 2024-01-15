from django.urls import path
from .. import views

urlpatterns = [path("user/", views.ProfileView.as_view(), name="profile")]
