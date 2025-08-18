from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Letter, Parcel

class ShipmentAPITests(APITestCase):
    """
    Набор тестов для API писем и посылок.
    """

    def setUp(self):
        """
        Предустановка начальных данных
        """
        self.letter_list_url = reverse('letter-list')
        self.parcel_list_url = reverse('parcel-list')

        self.letter_to_create_data = {
            "sender_full_name": "Бачурин Даниил Юрьевич",
            "recipient_full_name": "Дачурин Баниил Вучич",
            "origin_location": "Москва",
            "destination_location": "Биробиджан",
            "origin_postcode": 100001,
            "destination_postcode": 100002,
            "letter_type": Letter.LetterType.REGISTERED,
            "weight_kg": "1.000"
        }
        self.parcel_data = {
            "sender_full_name": "Коннор Сара Эдуардовна",
            "recipient_full_name": "Олегов Олег Олегович",
            "origin_location": "Екатеринбург",
            "destination_location": "Новосибирск",
            "origin_postcode": 620000,
            "destination_postcode": 630000,
            "notification_phone": "+79991234567",
            "parcel_type": Parcel.ParcelType.FIRST_CLASS,
            "payment_amount": "1500.00"
        }

        self.existing_letter = Letter.objects.create(
            sender_full_name="Иванов Иван Иванович",
            recipient_full_name="Сергеев Сергей Сергеевич",
            origin_location="Казань",
            destination_location="Уфа",
            origin_postcode=420000,
            destination_postcode=450000,
            letter_type=Letter.LetterType.REGULAR,
            weight_kg="0.100"
        )

        self.letter_detail_url = reverse('letter-detail', kwargs={'pk': self.existing_letter.pk})

    def test_create_letter_success(self):
        """
        Тест: Успешное создание письма (POST /api/v1/letters).
        """
        response = self.client.post(self.letter_list_url, self.letter_to_create_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Letter.objects.count(), 2)
        self.assertEqual(response.data['sender_full_name'], "Бачурин Даниил Юрьевич")
        self.assertEqual(response.data['letter_type'], Letter.LetterType.REGISTERED)


    def test_create_letter_invalid_data(self):
        """
        Тест: Неудачное создание письма с невалидными данными.
        """
        invalid_data = self.letter_to_create_data.copy()
        invalid_data['origin_postcode'] = invalid_data['destination_postcode']

        response = self.client.post(self.letter_list_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)


    def test_get_letter_list(self):
        """
        Тест: Получение списка всех писем (GET /api/v1/letters).
        """
        response = self.client.get(self.letter_list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['letter_type_display'], 'письмо')


    def test_get_single_letter(self):
        """
        Тест: Получение одного письма по ID (GET /api/v1/letters/{id}).
        """
        response = self.client.get(self.letter_detail_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.existing_letter.pk)


    def test_get_non_existent_letter(self):
        """
        Тест: Попытка получения несуществующего письма.
        """
        url = reverse('letter-detail', kwargs={'pk': 999})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)


    def test_delete_letter(self):
        """
        Тест: Удаление письма (DELETE /api/v1/letters/{id}).
        """
        response = self.client.delete(self.letter_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Letter.objects.count(), 0)

    def test_create_parcel_success(self):
        """
        Тест: Успешное создание посылки (POST /api/v1/parcels).
        """
        response = self.client.post(self.parcel_list_url, self.parcel_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Parcel.objects.count(), 1)
        self.assertEqual(response.data['notification_phone'], "+79991234567")
        self.assertEqual(response.data['parcel_type_display'], 'посылка 1 класса')


    def test_create_parcel_invalid_data(self):
        """
        Тест: Неудачное создание посылки с невалидными данными.
        """
        invalid_data = self.parcel_data.copy()
        invalid_data['destination_location'] = invalid_data['origin_location'].lower()

        response = self.client.post(self.parcel_list_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('details', response.data)