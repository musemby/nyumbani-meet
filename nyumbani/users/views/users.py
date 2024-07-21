from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from organizations.models import UserOrganization
from users.models import User


class UserApi(APIView):
    class UsersListApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "phone_number",
                "is_staff",
                "is_admin",
                "id",
            ]


class UsersListApi(UserApi):
    def get(self, request):
        # users = User.objects.filter(
        #     organization=request.user.get_or_create_organization()
        # )

        user_org_maps = UserOrganization.objects.filter(
            organization=request.user.get_or_create_organization()
        )

        users = User.objects.filter(id__in=user_org_maps.values_list("user", flat=True))

        output_serializer = self.UsersListApiSerializer(users, many=True)
        return Response(data=output_serializer.data)


class UsersDetailApi(UserApi):
    def get(self, request, pk=None):
        user = User.objects.get(pk=request.user.id if pk is None or pk == "me" else pk)
        output_serializer = self.UsersListApiSerializer(user)
        return Response(data=output_serializer.data)
