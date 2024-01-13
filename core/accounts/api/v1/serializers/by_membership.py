from rest_framework import serializers
from blog.models import *


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"
        read_only_fields = ["user"]
