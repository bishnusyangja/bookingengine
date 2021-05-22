import json

from django.contrib.auth.models import User
from django.test import TestCase

from model_mommy import mommy
from rest_framework.test import APIClient

from listings.models import Listing, BookingInfo, BookedListing


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
        l1 = mommy.make(Listing)
        l2 = mommy.make(Listing)
        l3 = mommy.make(Listing)
        l4 = mommy.make(Listing)
        l5 = mommy.make(Listing)
        mommy.make(BookingInfo, listing=l1, price=200)
        mommy.make(BookingInfo, listing=l2, price=300)
        mommy.make(BookingInfo, listing=l3, price=50)
        mommy.make(BookingInfo, listing=l4, price=50)
        mommy.make(BookingInfo, listing=l5, price=50)

        mommy.make(BookedListing, apartment=l1, reserved_from='2021-01-04', reserved_to='2021-01-08')
        mommy.make(BookedListing, apartment=l2, reserved_from='2021-01-10', reserved_to='2021-01-15')
        mommy.make(BookedListing, apartment=l3, reserved_from='2021-01-15', reserved_to='2021-01-18')
        mommy.make(BookedListing, apartment=l4, reserved_from='2021-01-25', reserved_to='2021-01-29')
        mommy.make(BookedListing, apartment=l5, reserved_from='2021-01-07', reserved_to='2021-01-10')

        data = dict(max_price=500,
                    check_in="2021-01-12",
                    check_out="2021-01-20")
        resp = self.client.get(self.url, data,
                               **self.get_authentication_headers())
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.json()['count'], 2)
        self.assertEqual(resp.json()['count'], 2)


