import json

from django.contrib.auth.models import User
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIClient

from listings.models import Listing, BookingInfo, BookedListing, HotelRoomType, HotelRoom


class BookingAPITestCase(TestCase):
    client = APIClient()
    headers = {}
    username = ''
    password = ''
    url = "/api/v1/units/"
    token_url = "/api/auth-token/"

    def setUp(self):
        self.username = 'bishnu'
        self.password = '1'
        user = mommy.make(User, username=self.username, is_staff=True, is_superuser=True)
        user.set_password(self.password)
        user.save()

    def get_auth_token(self):
        resp = self.client.post(self.token_url, data={'username': self.username, 'password': self.password})
        return resp.json().get('token')

    def get_authentication_headers(self):
        token = self.get_auth_token()
        return {"HTTP_AUTHORIZATION": f"Token {token}", "CONTENT_TYPE": "application/json"}

    def test_booking_api_without_authentication(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_booking_api_with_authentication(self):
        resp = self.client.get(self.url, **self.get_authentication_headers())
        self.assertEqual(resp.status_code, 200)

    def test_booking_case_1(self):
        mommy.make(Listing, _quantity=3)
        resp = self.client.get(self.url, **self.get_authentication_headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['count'], 3)

    def test_booking_case_2(self):
        l1 = mommy.make(Listing)
        l2 = mommy.make(Listing)
        l3 = mommy.make(Listing)
        l4 = mommy.make(Listing)
        l5 = mommy.make(Listing)
        l6 = mommy.make(Listing)
        mommy.make(BookingInfo, listing=l1, price=200)
        mommy.make(BookingInfo, listing=l2, price=300)
        mommy.make(BookingInfo, listing=l3, price=100)
        mommy.make(BookingInfo, listing=l4, price=150)
        mommy.make(BookingInfo, listing=l5, price=50)
        mommy.make(BookingInfo, listing=l6, price=120)

        data = dict(max_price=200,
                                check_in="2021-05-09",
                                check_out="2021-05-12")
        resp = self.client.get(self.url, data,
                               **self.get_authentication_headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['count'], 4)

    def test_booking_case_3(self):
        l1 = mommy.make(Listing, title="l1")
        l2 = mommy.make(Listing, title="l2")
        l3 = mommy.make(Listing, title="l3")
        l4 = mommy.make(Listing, title="l4")
        l5 = mommy.make(Listing, title="l5")
        l6 = mommy.make(Listing, title="l6")
        mommy.make(BookingInfo, listing=l1, price=200)
        mommy.make(BookingInfo, listing=l2, price=300)
        mommy.make(BookingInfo, listing=l3, price=50)
        mommy.make(BookingInfo, listing=l4, price=20)
        mommy.make(BookingInfo, listing=l5, price=10)
        mommy.make(BookingInfo, listing=l6, price=10)

        mommy.make(BookedListing, apartment=l1, reserved_from='2021-01-04', reserved_to='2021-01-08')
        mommy.make(BookedListing, apartment=l2, reserved_from='2021-01-10', reserved_to='2021-01-15')
        mommy.make(BookedListing, apartment=l3, reserved_from='2021-01-15', reserved_to='2021-01-18')
        mommy.make(BookedListing, apartment=l4, reserved_from='2021-01-25', reserved_to='2021-01-29')
        mommy.make(BookedListing, apartment=l5, reserved_from='2021-01-07', reserved_to='2021-01-10')
        mommy.make(BookedListing, apartment=l6, reserved_from='2021-01-17', reserved_to='2021-01-24')

        data = dict(max_price=500,
                    check_in="2021-01-12",
                    check_out="2021-01-20")
        resp = self.client.get(self.url, data,
                               **self.get_authentication_headers())
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.json()['count'], 3)

    def test_booking_case_4(self):
        l1 = mommy.make(Listing, title="l1")
        l2 = mommy.make(Listing, title="l2")
        l3 = mommy.make(Listing, title="l3")
        l4 = mommy.make(Listing, title="l4")
        l5 = mommy.make(Listing, title="l5")
        l6 = mommy.make(Listing, title="l6")
        mommy.make(BookingInfo, listing=l1, price=200)
        mommy.make(BookingInfo, listing=l2, price=300)
        mommy.make(BookingInfo, listing=l3, price=50)
        mommy.make(BookingInfo, listing=l4, price=20)
        mommy.make(BookingInfo, listing=l5, price=10)
        mommy.make(BookingInfo, listing=l6, price=10)

        h1 = mommy.make(HotelRoomType, hotel=l1)
        h2 = mommy.make(HotelRoomType, hotel=l2)
        h3 = mommy.make(HotelRoomType, hotel=l3)
        h4 = mommy.make(HotelRoomType, hotel=l4)
        h5 = mommy.make(HotelRoomType, hotel=l5)
        h6 = mommy.make(HotelRoomType, hotel=l6)

        h1r1 = mommy.make(HotelRoom, hotel_room_type=h1, room_number=6)
        h1r2 = mommy.make(HotelRoom, hotel_room_type=h1, room_number=5)
        h1r3 = mommy.make(HotelRoom, hotel_room_type=h1, room_number=7)

        h2r1 = mommy.make(HotelRoom, hotel_room_type=h2, room_number=6)
        h2r2 = mommy.make(HotelRoom, hotel_room_type=h2, room_number=5)
        h2r3 = mommy.make(HotelRoom, hotel_room_type=h2, room_number=7)

        h3r1 = mommy.make(HotelRoom, hotel_room_type=h3, room_number=6)
        h3r2 = mommy.make(HotelRoom, hotel_room_type=h3, room_number=5)
        h3r3 = mommy.make(HotelRoom, hotel_room_type=h3, room_number=7)

        mommy.make(BookedListing, hotel_room=h1r1, reserved_from='2021-01-04', reserved_to='2021-01-08')
        mommy.make(BookedListing, hotel_room=h2r1, reserved_from='2021-01-10', reserved_to='2021-01-15')
        mommy.make(BookedListing, hotel_room=h1r2, reserved_from='2021-01-15', reserved_to='2021-01-18')
        mommy.make(BookedListing, hotel_room=h1r3, reserved_from='2021-01-25', reserved_to='2021-01-29')
        mommy.make(BookedListing, hotel_room=h2r2, reserved_from='2021-01-07', reserved_to='2021-01-10')
        mommy.make(BookedListing, hotel_room=h3r1, reserved_from='2021-01-17', reserved_to='2021-01-24')

        data = dict(max_price=500,
                    check_in="2021-01-12",
                    check_out="2021-01-20")
        resp = self.client.get(self.url, data,
                               **self.get_authentication_headers())
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.json()['count'], 4)


