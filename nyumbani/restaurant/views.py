from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from .models import Restaurant, Menu


class RestaurantApi(APIView):
    class RestaurantCreateApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Restaurant
            fields = ["name", "description"]

    class RestaurantListApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Restaurant
            fields = ["name", "description", "id"]


class RestaurantListApi(RestaurantApi):
    def get(self, request):
        restaurants = Restaurant.objects.filter(
            organization=request.user.get_or_create_organization()
        )
        output_serializer = self.RestaurantListApiSerializer(restaurants, many=True)
        return Response(data=output_serializer.data)


class RestaurantCreateApi(RestaurantApi):
    def post(self, request):
        serializer = self.RestaurantCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = request.user.get_or_create_organization()

        restaurant = Restaurant.objects.create(
            name=serializer.validated_data["name"],
            description=serializer.validated_data["description"],
            organization=organization,
        )

        output_serializer = self.RestaurantListApiSerializer(restaurant)
        return Response(data=output_serializer.data)


class RestaurantUpdateApi(RestaurantApi):
    def put(self, request, pk):
        serializer = self.RestaurantCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.name = serializer.validated_data["name"]
        restaurant.description = serializer.validated_data["description"]
        restaurant.save()

        output_serializer = self.RestaurantListApiSerializer(restaurant)
        return Response(data=output_serializer.data)


class RestaurantDeleteApi(RestaurantApi):
    def delete(self, request, pk):
        if not Restaurant.objects.filter(
            pk=pk,
            organization=request.user.get_or_create_organization(),
        ).exists():
            return Response(status=404)

        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.delete()
        return Response(status=204)


class MenuApi(APIView):
    class MenuCreateApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Menu
            fields = ["name", "description", "restaurant", "file"]

    class MenuListApiSerializer(serializers.ModelSerializer):
        restaurant_name = serializers.SerializerMethodField()

        class Meta:
            model = Menu
            fields = [
                "name",
                "description",
                "restaurant",
                "file",
                "id",
                "restaurant_name",
                "is_active_menu",
            ]

        def get_restaurant_name(self, obj):
            if obj.restaurant is None:
                return None
            return obj.restaurant.name


class MenuListApi(MenuApi):
    def get(self, request):
        menus = Menu.objects.filter(
            organization=request.user.get_or_create_organization()
        )
        output_serializer = self.MenuListApiSerializer(menus, many=True)
        return Response(data=output_serializer.data)


class MenuCreateApi(MenuApi):
    def post(self, request):
        serializer = self.MenuCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = request.user.get_or_create_organization()

        menu = Menu.objects.create(
            name=serializer.validated_data["name"],
            description=serializer.validated_data["description"],
            restaurant=serializer.validated_data["restaurant"],
            file=serializer.validated_data["file"],
            organization=organization,
        )

        output_serializer = self.MenuListApiSerializer(menu)
        return Response(data=output_serializer.data)


class MenuUpdateApi(MenuApi):
    def put(self, request, pk):
        serializer = self.MenuCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu = Menu.objects.get(pk=pk)
        menu.name = serializer.validated_data["name"]
        menu.description = serializer.validated_data["description"]
        menu.restaurant = serializer.validated_data["restaurant"]
        menu.file = serializer.validated_data["file"]
        menu.save()

        output_serializer = self.MenuListApiSerializer(menu)
        return Response(data=output_serializer.data)


class MenuSetActiveApi(MenuApi):
    def put(self, request, pk):
        menu = Menu.objects.get(pk=pk)

        # set others inactive
        Menu.objects.filter(
            organization=request.user.get_or_create_organization()
        ).exclude(pk=pk).update(is_active_menu=False)

        menu.is_active_menu = True
        menu.save()

        return Response(status=204)


class MenuActiveRenderApi(MenuApi):
    def get(self, request):
        menu = Menu.objects.get(
            organization=request.user.get_or_create_organization(), is_active_menu=True
        )

        serializer = self.MenuListApiSerializer(menu)

        return Response(data=serializer.data)


class MenuDeleteApi(MenuApi):
    def delete(self, request, pk):
        if not Menu.objects.filter(
            pk=pk,
            organization=request.user.get_or_create_organization(),
        ).exists():
            return Response(status=404)

        menu = Menu.objects.get(pk=pk)
        menu.delete()
        return Response(status=204)
