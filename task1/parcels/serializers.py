from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Letter, Parcel
from . import constants as const

class BaseShipmentSerializer(serializers.ModelSerializer):
    origin_postcode = serializers.IntegerField(
        validators=[MinValueValidator(const.POSTCODE_MIN_VALUE, message=const.ERROR_MSG_POSTCODE_LENGTH)],
    )
    destination_postcode = serializers.IntegerField(
        validators=[MinValueValidator(const.POSTCODE_MIN_VALUE, message=const.ERROR_MSG_POSTCODE_LENGTH)],
    )

    class Meta:
        fields = [
            'id', 'sender_full_name', 'recipient_full_name', 'origin_location',
            'destination_location', 'origin_postcode', 'destination_postcode',
            'created_at', 'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        if 'origin_postcode' in data and 'destination_postcode' in data:
            if data['origin_postcode'] == data['destination_postcode']:
                raise serializers.ValidationError(const.ERROR_MSG_POSTCODE_MATCH)
        if 'origin_location' in data and 'destination_location' in data:
            if data['origin_location'].lower() == data['destination_location'].lower():
                raise serializers.ValidationError(const.ERROR_MSG_LOCATION_MATCH)
        return data

class LetterSerializer(BaseShipmentSerializer):
    letter_type_display = serializers.CharField(source='get_letter_type_display', read_only=True)

    weight_kg = serializers.DecimalField(
        max_digits=const.WEIGHT_MAX_DIGITS,
        decimal_places=const.WEIGHT_DECIMAL_PLACES,
        validators=[MinValueValidator(const.WEIGHT_MIN_VALUE, message=const.ERROR_MSG_WEIGHT_POSITIVE)]
    )

    class Meta(BaseShipmentSerializer.Meta):
        model = Letter
        fields = BaseShipmentSerializer.Meta.fields + ['letter_type', 'letter_type_display', 'weight_kg']

class ParcelSerializer(BaseShipmentSerializer):
    parcel_type_display = serializers.CharField(source='get_parcel_type_display', read_only=True)

    payment_amount = serializers.DecimalField(
        max_digits=const.PAYMENT_MAX_DIGITS,
        decimal_places=const.PAYMENT_DECIMAL_PLACES,
        validators=[MinValueValidator(const.PAYMENT_MIN_VALUE, message=const.ERROR_MSG_PAYMENT_NEGATIVE)]
    )

    class Meta(BaseShipmentSerializer.Meta):
        model = Parcel
        fields = BaseShipmentSerializer.Meta.fields + ['notification_phone', 'parcel_type', 'parcel_type_display', 'payment_amount']