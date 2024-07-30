from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from bookings.models import Booking, Building, Room

from bookings.services import send_booking_created_notification
from users.models import User


class BookingApi(APIView):
    class BookingsCreateApiSerializer(serializers.ModelSerializer):
        tenant = serializers.UUIDField(required=False, allow_null=True, default=None)

        class Meta:
            model = Booking
            fields = ["start_time", "end_time", "description", "room", "tenant"]

    class BookingsListApiSerializer(serializers.ModelSerializer):
        room_name = serializers.SerializerMethodField()

        class Meta:
            model = Booking
            fields = [
                "start_time",
                "end_time",
                "description",
                "organization",
                "room",
                "room_name",
                "booked_by",
                "id",
            ]

        def get_room_name(self, obj):
            if obj.room is None:
                return None
            return obj.room.name


class BookingsListApi(BookingApi):
    def get(self, request):
        bookings = Booking.objects.filter(
            organization=request.user.get_or_create_organization()
        ).order_by("start_time")

        output_serializer = self.BookingsListApiSerializer(bookings, many=True)
        return Response(data=output_serializer.data)


class BookingsCreateApi(BookingApi):
    def post(self, request):
        serializer = self.BookingsCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if (
            request.user.is_staff
            and serializer.validated_data.get("tenant", None) is not None
        ):
            user = User.objects.get(pk=serializer.validated_data["tenant"])
            print("tenant selected by admin", user)
        else:
            user = request.user

        booking = Booking.objects.create(
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
            description=serializer.validated_data["description"],
            room=serializer.validated_data["room"],
            booked_by=user,
            organization=user.get_or_create_organization(),
        )

        send_booking_created_notification(booking.id)

        output_serializer = self.BookingsListApiSerializer(booking)
        return Response(data=output_serializer.data)


class BookingsDeleteApi(BookingApi):
    def delete(self, request, pk):
        if not Booking.objects.filter(
            pk=pk,
            organization=request.user.get_or_create_organization(),
            booked_by=request.user,
        ).exists():
            return Response(status=404)

        booking = Booking.objects.get(pk=pk)
        booking.delete()
        return Response(status=204)


class BookingsUpdateApi(BookingApi):
    def put(self, request, pk):
        if not Booking.objects.filter(
            pk=pk,
            organization=request.user.get_or_create_organization(),
            booked_by=request.user,
        ).exists():
            return Response(status=404)

        serializer = self.BookingsCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = Booking.objects.get(pk=pk)
        booking.start_time = serializer.validated_data["start_time"]
        booking.end_time = serializer.validated_data["end_time"]
        booking.description = serializer.validated_data.get("description", None)
        booking.save()

        output_serializer = self.BookingsListApiSerializer(booking)
        return Response(data=output_serializer.data)


class RoomApi(APIView):
    class RoomsListApiSerializer(serializers.ModelSerializer):
        building_name = serializers.SerializerMethodField()

        class Meta:
            model = Room
            fields = [
                "name",
                "number",
                "building",
                "capacity",
                "description",
                "id",
                "building_name",
            ]

        def get_building_name(self, obj):
            if obj.building is None:
                return None
            return obj.building.name

    class RoomsCreateApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = [
                "name",
                "number",
                "description",
                "building",
                "capacity",
            ]


class RoomsListApi(RoomApi):
    def get(self, request):
        rooms = Room.objects.filter(
            organization=request.user.get_or_create_organization()
        )
        output_serializer = self.RoomsListApiSerializer(rooms, many=True)
        return Response(data=output_serializer.data)


class RoomsCreateApi(RoomApi):
    def post(self, request):
        serializer = self.RoomsCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = request.user.get_or_create_organization()

        room = Room.objects.create(
            name=serializer.validated_data["name"],
            number=serializer.validated_data.get("number", None),
            capacity=serializer.validated_data.get("capacity", None),
            description=serializer.validated_data.get("description", None),
            organization=organization,
            building=serializer.validated_data.get("building", None),
        )

        output_serializer = self.RoomsListApiSerializer(room)
        return Response(data=output_serializer.data)


class BuildingApi(APIView):
    class BuildingsListApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Building
            fields = ["name", "number", "location", "description", "id"]

    class BuildingsCreateApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Building
            fields = ["name", "number", "location", "description"]


class BuildingsListApi(BuildingApi):
    def get(self, request):
        buildings = Building.objects.filter(
            organization=request.user.get_or_create_organization()
        )
        output_serializer = self.BuildingsListApiSerializer(buildings, many=True)
        return Response(data=output_serializer.data)


class BuildingsCreateApi(BuildingApi):
    def post(self, request):
        serializer = self.BuildingsCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = request.user.get_or_create_organization()

        building = Building.objects.create(
            name=serializer.validated_data["name"],
            number=serializer.validated_data.get("number", None),
            location=serializer.validated_data.get("location", None),
            description=serializer.validated_data.get("description", None),
            organization=organization,
        )

        output_serializer = self.BuildingsListApiSerializer(building)
        return Response(data=output_serializer.data)


class BuildingsDeleteApi(BuildingApi):
    def delete(self, request, pk):
        if not Building.objects.filter(
            pk=pk,
            organization=request.user.get_or_create_organization(),
        ).exists():
            return Response(status=404)

        building = Building.objects.get(pk=pk)
        building.delete()
        return Response(status=204)
