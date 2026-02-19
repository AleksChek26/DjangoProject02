from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Course, Lesson, Subscription


class StudyTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create(email="test@test.ru", is_active=True)
        self.user.set_password("testpassword")
        self.user.save()

        # Создаем курс и урок
        self.course = Course.objects.create(
            title="Основы Python", description="Курс про Python"
        )
        self.lesson = Lesson.objects.create(
            title="Переменные",
            description="Урок про переменные",
            course=self.course,
            owner=self.user,
        )

    def test_lesson_create(self):
        """Тестирование создания урока"""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Списки",
            "description": "Урок про списки",
            "course": self.course.id,
        }
        response = self.client.post(reverse("materials:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list(self):
        """Тестирование получения списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("materials:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка пагинации (результаты в ключе 'results')
        self.assertEqual(len(response.data.get("results")), 1)

    def test_lesson_update(self):
        """Тестирование изменения урока"""
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_update", args=[self.lesson.pk])
        data = {"title": "Новое название"}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "Новое название")

    def test_lesson_delete(self):
        """Тестирование удаления урока"""
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_delete", args=[self.lesson.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription_toggle(self):
        """Тестирование работы подписки (создание/удаление)"""
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course_subscribe")
        data = {"course": self.course.id}

        # 1. Создание подписки
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # 2. Удаление подписки (повторный запрос)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unauthorized_access(self):
        """Проверка доступа без авторизации"""
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
