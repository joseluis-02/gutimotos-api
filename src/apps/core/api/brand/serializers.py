# Django rest framework
from rest_framework import serializers
# Models
from ...models.brand import Brand

class BrandSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]