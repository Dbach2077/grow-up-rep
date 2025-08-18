from django_filters import rest_framework as filters
from .models import Letter, Parcel

class BaseShipmentFilter(filters.FilterSet):
    # datatime filter for created_at field
    created_at_after = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    # Full name filters for sender and recipient
    sender_full_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        abstract = True
        fields = ['sender_full_name', 'recipient_full_name', 'origin_location', 'destination_location', 'created_at_after']


class LetterFilter(BaseShipmentFilter):
    class Meta(BaseShipmentFilter.Meta):
        model = Letter
        # Add specific fields for Letter model
        fields = BaseShipmentFilter.Meta.fields + ['letter_type']


class ParcelFilter(BaseShipmentFilter):
    class Meta(BaseShipmentFilter.Meta):
        model = Parcel
        # Add specific fields for Parcel model
        fields = BaseShipmentFilter.Meta.fields + ['parcel_type', 'notification_phone']