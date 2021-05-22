from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from listings.models import Listing
from listings.serializers import ListingSerializer, FilterParamSerializer


class AppAuthTokenView(ObtainAuthToken):
    authentication_classes = ()


# assuming that booking is done by logged in user
class ListingAPIView(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ListingSerializer
    queryset = Listing.objects.none()

    def get_queryset(self):
        qs = Listing.objects.all()
        qs = self.filter_params(qs)
        qs = qs.order_by('booking_info__price')
        return qs

    def filter_params(self, qs):
        params = self.request.query_params
        ser = FilterParamSerializer(data=params)
        try:
            ser.is_valid(raise_exception=True)
        except Exception as e:
            return qs
        else:
            data = ser.validated_data
            check_in = data.get('check_in')
            check_in = check_in[0] if isinstance(check_in, list) else check_in
            check_in = check_in.strftime("%Y-%m-%d")
            check_out = data.get('check_out')
            check_out = check_out[0] if isinstance(check_out, list) else check_out
            check_out = check_out.strftime("%Y-%m-%d")
            max_price = data.get('max_price')
            max_price = max_price[0] if isinstance(max_price, list) else max_price
            if check_in and check_out:
                qs = qs.filter(
                        # Q(booked_apartment__isnull=True) |
                        # Q(booked_apartment__reserved_to__lte=check_in) |
                        # Q(booked_apartment__reserved_from__gte=check_out) |
                        ~Q(booked_apartment__reserved_from__gte=check_in, booked_apartment__reserved_to__lte=check_in)).filter(
                        ~Q(booked_apartment__reserved_from__gte=check_out, booked_apartment__reserved_to__lte=check_out)
                        #
                        # ~Q(booked_apartment__reserved_from__lte=check_in, booked_apartment__reserved_from__gte=check_out) |
                        # ~Q(booked_apartment__reserved_to__lte=check_in, booked_apartment__reserved_to__gte=check_in) |
                        # ~Q(booked_apartment__reserved_to__lte=check_out, booked_apartment__reserved_to__gte=check_out) |
                        # ~Q(booked_apartment__reserved_from__lte=check_in, booked_apartment__reserved_from__gte=check_in) |
                        # ~Q(booked_apartment__reserved_from__lte=check_out, booked_apartment__reserved_from__gte=check_out) |

                        # Q(hotel_room_types__hotel_rooms__booked_hotel_room__isnull=True) |
                        # Q(hotel_room_types__hotel_rooms__booked_hotel_room__reserved_to__lte=check_in) |
                        # Q(hotel_room_types__hotel_rooms__booked_hotel_room__reserved_from__gte=check_out) |
                        # ~Q(hotel_room_types__hotel_rooms__booked_hotel_room__reserved_from__gte=check_in,
                        #    hotel_room_types__hotel_rooms__booked_hotel_room__reserved_to__lte=check_in)
                        # ~Q(hotel_room_types__hotel_rooms__booked_hotel_room__reserved_from__gte=check_out,
                        #    hotel_room_types__hotel_rooms__booked_hotel_room__reserved_to__lte=check_out)
                # ).exclude(
                #
                #     Q(booked_apartment__reserved_from__gte=check_in, booked_apartment__reserved_to__lte=check_in) |
                #     Q(booked_apartment__reserved_from__gte=check_out, booked_apartment__reserved_to__lte=check_out) |
                #
                #     Q(booked_apartment__reserved_from__lte=check_in, booked_apartment__reserved_from__gte=check_out) |
                #     Q(booked_apartment__reserved_to__lte=check_in, booked_apartment__reserved_to__gte=check_in) |
                #     Q(booked_apartment__reserved_to__lte=check_out, booked_apartment__reserved_to__gte=check_out) |
                #     Q(booked_apartment__reserved_from__lte=check_in, booked_apartment__reserved_from__gte=check_in) |
                #     Q(booked_apartment__reserved_from__lte=check_out, booked_apartment__reserved_from__gte=check_out)
                )
            if max_price:
                qs = qs.filter(booking_info__price__lt=max_price)
            # print(qs.query)
        return qs

