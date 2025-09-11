# Django rest framework
from rest_framework import serializers
# Models
from ...models.color import Color

class ColorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["id", "name", "code_hex"]