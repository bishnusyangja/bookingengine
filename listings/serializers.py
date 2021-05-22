from rest_framework import serializers

from listings.models import Listing


class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = ('title', 'country', 'city', 'listing_type', "price", )


class FilterParamSerializer(serializers.Serializer):
    max_price = serializers.IntegerField()
    check_in = serializers.DateField(format="%Y-%m-%d")
    check_out = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        fields = ('max_price', 'check_in', 'check_out', )
