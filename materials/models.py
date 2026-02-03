from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="courses/", verbose_name="Превью", null=True, blank=True
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name="Владелец")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lessons/", verbose_name="Превью", null=True, blank=True
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name="Владелец")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
