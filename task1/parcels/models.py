from django.db import models

from .constants import (
    FULL_NAME_MAX_LENGTH,
    LOCATION_MAX_LENGTH,
    PHONE_MAX_LENGTH
)

class BaseShipment(models.Model):
    sender_full_name = models.CharField(
        max_length=FULL_NAME_MAX_LENGTH,
        verbose_name="ФИО отправителя"
    )
    recipient_full_name = models.CharField(
        max_length=FULL_NAME_MAX_LENGTH,
        verbose_name="ФИО получателя"
    )
    origin_location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        verbose_name="Пункт отправки"
    )
    destination_location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        verbose_name="Пункт получения"
    )
    origin_postcode = models.IntegerField(verbose_name="Индекс места отправки")
    destination_postcode = models.IntegerField(verbose_name="Индекс места получения")

    # auto_now_add=True устанавливает значение только при создании объекта.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # auto_now=True обновляет значение при каждом сохранении объекта.
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True # abstract = True - для модели не нужно создавать отдельную таблицу в БД.
        indexes = [ 
            models.Index(fields=['origin_postcode']),
            models.Index(fields=['destination_postcode']),
        ]


class Letter(BaseShipment):
    """
    Модель, представляющая письмо. Наследует все поля от BaseShipment.
    """
    class LetterType(models.IntegerChoices):
        REGULAR = 1, 'письмо'
        REGISTERED = 2, 'заказное письмо'
        VALUABLE = 3, 'ценное письмо'
        EXPRESS = 4, 'экспресс-письмо'

    letter_type = models.PositiveSmallIntegerField(
        choices=LetterType.choices,
        default=LetterType.REGULAR,
        verbose_name="Тип письма"
    )
    weight_kg = models.DecimalField(
        max_digits=7,        
        decimal_places=3,    
        verbose_name="Вес письма (кг)"
    )


class Parcel(BaseShipment):
    class ParcelType(models.IntegerChoices):
        SMALL_PACKET = 1, 'мелкий пакет'
        PARCEL = 2, 'посылка'
        FIRST_CLASS = 3, 'посылка 1 класса'
        VALUABLE = 4, 'ценная посылка'
        INTERNATIONAL = 5, 'посылка международная'
        EXPRESS = 6, 'экспресс-посылка'

    notification_phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        verbose_name="Телефон для извещения"
    )
    parcel_type = models.PositiveSmallIntegerField(
        choices=ParcelType.choices,
        default=ParcelType.PARCEL,
        verbose_name="Тип посылки"
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма платежа"
    )