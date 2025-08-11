from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Letter, Parcel

class LetterSerializer(serializers.ModelSerializer):
    # Добавляем валидаторы прямо к полям.
    # MinValueValidator проверяет, что значение не меньше указанного.
    origin_postcode = serializers.IntegerField(
        validators=[MinValueValidator(100000, message="Индекс должен состоять из 6 цифр")],
    )
    destination_postcode = serializers.IntegerField(
        validators=[MinValueValidator(100000, message="Индекс должен состоять из 6 цифр")],
    )
    
    class Meta:
        model = Letter  # Указываем, с какой моделью работает сериализатор.
        # Явно перечисляем поля, которые будут включены в API.
        fields = [
            'id', 'sender_full_name', 'recipient_full_name', 'origin_location', 
            'destination_location', 'origin_postcode', 'destination_postcode', 
            'letter_type', 'weight_kg', 'created_at', 'updated_at',
        ]
        # Поля только для чтения. Их нельзя будет изменить через API.
        read_only_fields = ('created_at', 'updated_at')
    
    def validate(self, data):
        """
        Кастомный метод валидации для всего объекта.
        Вызывается после валидации каждого отдельного поля.
        """
        if data['origin_postcode'] == data['destination_postcode']:
            raise serializers.ValidationError("Индекс отправки и назначения не должны совпадать.")
        if data['origin_location'].lower() == data['destination_location'].lower():
            raise serializers.ValidationError("Пункт отправки и назначения не должны совпадать.")
        return data

    def to_representation(self, instance):
        """
        Метод для кастомизации вывода данных (представления объекта).
        Позволяет изменить то, как объект будет выглядеть в JSON.
        """
        ret = super().to_representation(instance)
        # Заменяем числовой ID типа письма на его строковое представление (например, 1 -> 'письмо').
        ret['letter_type'] = instance.get_letter_type_display()
        return ret


class ParcelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Parcel. Логика аналогична LetterSerializer.
    """
    origin_postcode = serializers.IntegerField(
        validators=[MinValueValidator(100000, message="Индекс должен состоять из 6 цифр")],
    )
    destination_postcode = serializers.IntegerField(
        validators=[MinValueValidator(100000, message="Индекс должен состоять из 6 цифр")],
    )

    class Meta:
        model = Parcel
        fields = [
            'id', 'sender_full_name', 'recipient_full_name', 'origin_location', 
            'destination_location', 'origin_postcode', 'destination_postcode', 
            'notification_phone', 'parcel_type', 'payment_amount', 'created_at', 'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at')
        
    def validate(self, data):
        if data['origin_postcode'] == data['destination_postcode']:
            raise serializers.ValidationError("Индекс отправки и назначения не должны совпадать.")
        if data['origin_location'].lower() == data['destination_location'].lower():
            raise serializers.ValidationError("Пункт отправки и назначения не должны совпадать.")
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['parcel_type'] = instance.get_parcel_type_display()
        return ret