from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeOnlyValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YoutubeOnlyValidator(field='video_url')]

class CourseSerializer(ModelSerializer):
    # Поле вывода количества уроков
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class CourseDetailSerializer(ModelSerializer):
    count_lessons_in_course = SerializerMethodField()

    def get_count_lessons_in_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Course
        fields = ("title", "description", "count_lessons_in_course")
