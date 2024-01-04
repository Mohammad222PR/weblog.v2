from rest_framework import generics
from ..serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60))
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(user=self.request.user)
        return obj


