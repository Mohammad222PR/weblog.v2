from django.urls import path
from .. import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("list/", views.BlogListAndCreateView.as_view(), name="blog-list"),
    path(
        "list/<int:pk>",
        views.BlogDetailAndUpdateView.as_view(),
        name="blog-detail-and-update",
    ),
    path(
        "tag/list/<int:pk>",
        views.TagView.as_view(),
        name="tag-list",
    ),
    path(
        "category/list/<int:pk>",
        views.CategoryView.as_view(),
        name="tag-list",
    ),
]

# router = DefaultRouter()
# router.register(r"comment", views.CommentView, basename="comment")
#
# urlpatterns += router.urls
