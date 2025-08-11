from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from django.shortcuts import get_object_or_404
from .models import Letter, Parcel
from .serializers import LetterSerializer, ParcelSerializer

class LetterViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обработки CRUD-операций (Create, Retrieve, Update, Delete) с письмами.
    ModelViewSet автоматически предоставляет реализацию всех этих действий.
    """
    # queryset - это набор объектов, с которыми будет работать ViewSet.
    queryset = Letter.objects.all()
    # serializer_class - сериализатор, который будет использоваться для валидации и преобразования данных.
    serializer_class = LetterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            # is_valid(raise_exception=True) - если данные невалидны,
            # метод выбросит исключение ValidationError, которое мы ловим ниже.
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # Возвращаем успешный ответ со статусом 201 CREATED.
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            # Ловим ошибку валидации и возвращаем кастомный ответ
            # со статусом 400 BAD REQUEST и деталями ошибки.
            print(f"Ошибка валидации при создании письма: {e.detail}")
            return Response({"error": "Неверные данные", "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределяем метод получения одного объекта (GET-запрос по ID).
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            return Response({"error": "Письмо с таким ID не найдено."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Переопределяем метод удаления объекта (DELETE-запрос).
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            # При успешном удалении возвращаем статус 204 NO CONTENT,
            return Response({"message": "Письмо успешно удалено."}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"error": "Не удалось удалить. Письмо не найдено."}, status=status.HTTP_404_NOT_FOUND)


class ParcelViewSet(viewsets.ModelViewSet):
    """
    ViewSet для посылок
    """
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({"error": "Не удалось создать посылку. Неверные данные.", "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        # пытается получить объект, и если не находит, сразу возвращает ответ 404.
        instance = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Переопределяем метод обновления (PUT/PATCH-запросы).
        """
        # partial=True разрешает частичное обновление (метод PATCH).
        # Если partial=False, то для обновления нужно передать все поля (метод PUT).
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": "Не удалось обновить. Ошибки валидации.", "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)