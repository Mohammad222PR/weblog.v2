from django.urls import path
from accounts.api.v1 import views

urlpatterns = [
    # ACCOUNT REGISTRATION
    path('obtain/token/create', views.ObtainTokenView.as_view(), name='obt-token'),
    path('obtain/pair/token', views.ObtainPairTokenView.as_view(), name='obt-pair-token'),
    path('obtain/token/delete', views.CustomDiscardAuthView.as_view(), name='discard-auth'),
]
