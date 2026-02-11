from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentListAPIView(ListAPIView):
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

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentViewSet(viewsets.ViewSet):

    def create(self, request):
        # Допустим, мы передаем название курса и цену в теле запроса
        course_name = request.data.get("course_name")
        amount = request.data.get("amount")

        try:
            # Последовательный вызов сервисов
            product_id = create_stripe_product(course_name)
            price = create_stripe_price(amount, product_id)
            session = create_stripe_session(price.id)

            return Response(
                {"payment_url": session.url, "session_id": session.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
