from rest_framework import serializers
from accounts.models import *


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["email", "user"]


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get('request')
        if Membership.user == request.user:
            raise serializers.ValidationError('you are have membership')
        return super().validate(attrs)