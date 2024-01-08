from django.urls import path
from .. import views


urlpatterns = [
    path('list/', views.BlogListAndCreateView.as_view(), name='blog-list-and-create'),
    path('list/<int:pk>', views.BlogDetailAndUpdateView.as_view(), name='blog-detail-and-update'),
]
