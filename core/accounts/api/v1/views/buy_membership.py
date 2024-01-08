from rest_framework.views import APIView
from blog.models import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser


class MembershipViews(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MembershipSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        try:
            mem = Membership.objects.get(user=request.user)
            serializer = MembershipSerializer(instance=mem)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Membership.DoesNotExist:
            raise Response({"detail": "you are bot have membership"})

    def post(self, request):
        if not Membership.objects.filter(user=request.user).exists():
            serializers = self.serializer_class(data=request.data)
            if serializers.is_valid():
                serializers.validated_data["user"] = request.user
                serializers.save()
                return Response(
                    {
                        "email": request.user.email,
                        "username": request.user.username,
                        "membership": request.user.membership,
                    }
                )
        else:
            return Response(
                {"detail": "you are have a membership you cannot buy again"}
            )
