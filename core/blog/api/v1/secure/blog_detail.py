from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import Profile
from blog.models import Blog

class IsOwnerOrReadonly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class IsCommentOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
