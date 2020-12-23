from rest_framework import serializers
from app.models import Type, Size, Topping


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("id", "type")


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id", "size")


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ("id", "topping")
