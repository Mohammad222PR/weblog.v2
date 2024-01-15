from rest_framework import serializers
from accounts.models import *


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get("request")
        if Membership.user == request.user:
            raise serializers.ValidationError("you are have membership")
        return super().validate(attrs)


class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = "__all__"


class ProfileSerializers(serializers.ModelSerializer):
    membership = serializers.SerializerMethodField()
    factor = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    skills = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Skills.objects.all())

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["email", "user"]

    def get_membership(self, obj):
        request = self.context.get("request")
        try:
            queryset = Membership.objects.get(user=request.user)
            member = MembershipSerializer(instance=queryset)
            return member.data
        except:
            return None

    def get_factor(self, obj):
        request = self.context.get("request")
        try:
            queryset = Factor.objects.filter(user=request.user)
            member = FactorSerializer(instance=queryset, many=True)
            return member.data
        except:
            return None
