from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from bookings.models import Booking, Building, Room


class BookingApi(APIView):
    class BookingsCreateApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Booking
            fields = ["start_time", "end_time", "description", "room"]

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
                "id",
            ]

        def get_room_name(self, obj):
            return obj.room.name


class BookingsListApi(BookingApi):
    def get(self, request):
        bookings = Booking.objects.filter(
            organization=request.user.get_or_create_organization()
        )

        output_serializer = self.BookingsListApiSerializer(bookings, many=True)
        return Response(data=output_serializer.data)


class BookingsCreateApi(BookingApi):
    def post(self, request):
        serializer = self.BookingsCreateApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = Booking.objects.create(
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
            description=serializer.validated_data["description"],
            room=serializer.validated_data["room"],
            booked_by=request.user,
            organization=request.user.get_or_create_organization(),
        )

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


class RoomApi(APIView):
    class RoomsListApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = ["name", "number", "building", "capacity", "description", "id"]

    class RoomsCreateApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = ["name", "description"]


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
            # number=serializer.validated_data["number"],
            # capacity=serializer.validated_data["capacity"],
            description=serializer.validated_data["description"],
            organization=organization,
            building=Building.objects.filter(organization=organization).first(),
        )

        output_serializer = self.RoomsListApiSerializer(room)
        return Response(data=output_serializer.data)
