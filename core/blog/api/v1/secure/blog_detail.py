from rest_framework.permissions import BasePermission ,SAFE_METHODS
from accounts.models import *
from blog.models import *


class IsOwnerOrReadonly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return Profile.user == request.user 
        
