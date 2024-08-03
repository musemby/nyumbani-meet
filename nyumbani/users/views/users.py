from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from organizations.models import UserOrganization
from users.models import User


class UserApi(APIView):
    class UsersListApiSerializer(serializers.ModelSerializer):
        is_admin = serializers.SerializerMethodField()

        class Meta:
            model = User
            fields = [
                "phone_number",
                "name",
                "house_number",
                "is_staff",
                "is_admin",
                "id",
            ]

        def get_is_admin(self, obj: User):
            if obj.is_staff:
                return True

            if obj.is_admin:
                return True

            if obj.nyumbani_role == "admin":
                return True

            if self.context.get("request_user") is None:
                return False

            request_user = self.context["request_user"]
            request_org = request_user.get_or_create_organization()

            if request_user.id != obj.id:
                return False

            return request_user.is_organization_admin(request_org)


class UsersListApi(UserApi):
    def get(self, request):
        user_org_maps = UserOrganization.objects.filter(
            organization=request.user.get_or_create_organization()
        )

        users = User.objects.filter(id__in=user_org_maps.values_list("user", flat=True))

        output_serializer = self.UsersListApiSerializer(
            users, many=True, context={"request_user": request.user}
        )
        return Response(data=output_serializer.data)


class UsersDetailApi(UserApi):
    def get(self, request, pk=None):
        user = User.objects.get(pk=request.user.id if pk is None or pk == "me" else pk)
        output_serializer = self.UsersListApiSerializer(user)
        return Response(data=output_serializer.data)
