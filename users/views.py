from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Настройка фильтрации по полям
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )

    # Настройка сортировки по дате
    ordering_fields = ("payment_date",)
