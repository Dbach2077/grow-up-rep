from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from django.shortcuts import get_object_or_404
from .models import Letter, Parcel
from .serializers import LetterSerializer, ParcelSerializer
from .filters import LetterFilter, ParcelFilter
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend

class BaseShipmentViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet для общей логики.
    """
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ['sender_full_name', 'recipient_full_name', 'origin_location', 'destination_location']
    ordering_fields = ['created_at', 'updated_at', 'sender_full_name']
    ordering = ['-created_at'] # standard ordering by creation date

    def create(self, request, *args, **kwargs): # Custom create method with error handling
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            error_message = f"Ошибка валидации при создании: {e.detail}"
            print(error_message)
            return Response({"error": "Неверные данные", "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": "Не удалось обновить. Ошибки валидации.", "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class LetterViewSet(BaseShipmentViewSet):
    """
    ViewSet для CRUD-операций с письмами.
    Наследует всю логику фильтрации, поиска и сортировки от BaseShipmentViewSet.
    """
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    filterset_class = LetterFilter

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            return Response({"error": "Письмо с таким ID не найдено."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"error": "Не удалось удалить. Письмо не найдено."}, status=status.HTTP_404_NOT_FOUND)


class ParcelViewSet(BaseShipmentViewSet):
    """
    ViewSet для CRUD-операций с посылками.
    """
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    filterset_class = ParcelFilter
    
    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class IndexView(TemplateView):
    template_name = "index.html"