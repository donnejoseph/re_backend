from api.models import City, Area, Property, Image
from rest_framework import serializers


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'population')


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name', 'city')


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'title', 'address', 'city', 'state', 'area', 'description', 'sale_type', 'price', 'bedrooms',
                  'bathrooms', 'home_type', 'square_fit', 'object_id', 'is_published', 'building_year', 'best_offer',
                  'modx_id')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'property', 'image')
