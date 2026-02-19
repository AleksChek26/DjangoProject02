import re

from rest_framework.serializers import ValidationError


class YoutubeOnlyValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        # Проверка: если ссылка есть, она должна содержать youtube.com
        if url and not re.match(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/", url):
            raise ValidationError(
                {self.field: "Разрешены ссылки только на youtube.com."}
            )
