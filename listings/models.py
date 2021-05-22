from django.contrib.auth.models import User
from django.db import models


class Listing(models.Model):
    HOTEL = 'hotel'
    APARTMENT = 'apartment'
    LISTING_TYPE_CHOICES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
    )

    listing_type = models.CharField(
        max_length=16,
        choices=LISTING_TYPE_CHOICES,
        default=APARTMENT
    )
    title = models.CharField(max_length=255,)
    country = models.CharField(max_length=255,)
    city = models.CharField(max_length=255,)

    def price(self):
        try:
            return self.booking_info.price
        except:
            return 0

    def __str__(self):
        return self.title
    

class HotelRoomType(models.Model):
    hotel = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_room_types'
    )
    title = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.hotel} - {self.title}'


class HotelRoom(models.Model):
    hotel_room_type = models.ForeignKey(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_rooms'
    )
    room_number = models.CharField(max_length=255,)

    def __str__(self):
        return self.room_number


class BookingInfo(models.Model):
    listing = models.OneToOneField(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info'
    )
    hotel_room_type = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info',
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        if self.listing:
            obj = self.listing
        else:
            obj = self.hotel_room_type
            
        return f'{obj} {self.price}'


# for apartment reserved information can be retrieved from this model
class BookedListing(models.Model):
    reserved_from = models.DateField(default=None,
                                     null=True)
    reserved_to = models.DateField(default=None,
                                   null=True)
    reserved_by = models.ForeignKey(User,
                                    on_delete=models.PROTECT,
                                    related_name="bookings",
                                    null=True,
                                    default=None)
    apartment = models.ForeignKey(Listing,
                                  on_delete=models.PROTECT,
                                  related_name='booked_apartment',
                                  null=True,
                                  default=None)
    hotel_room = models.ForeignKey(HotelRoom,
                                   on_delete=models.PROTECT,
                                   related_name='booked_hotel_room',
                                   null=True,
                                   default=None)

    def __str__(self):
        if self.apartment is not None:
            return self.apartment.title
        if self.hotel_room is not None:
            return f'{self.hotel_room.hotel_rooms}-{self.hotel_room.room_number}'
        return '---'