from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price_per_night', 'host_name', 'created_at']
        read_only_fields = ['created_at']

class BookingSerializer(serializers.ModelSerializer):
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'guest_name', 'check_in', 'check_out', 'created_at']
        read_only_fields = ['created_at', 'guest_name']

    def create(self, validated_data):
        validated_data['guest_name'] = self.context['request'].user
        return super().create(validated_data)
