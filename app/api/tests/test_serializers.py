from django.test import TestCase
from api.models import City, Area, Property, Image
from api.serializers import CitySerializer, AreaSerializer, PropertySerializer, ImageSerializer


class CitySerializerTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="New York", population="8000000")
        self.serializer = CitySerializer(instance=self.city)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'population'])

    def test_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.city.name)
        self.assertEqual(data['population'], self.city.population)


class AreaSerializerTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="New York", population="8000000")
        self.area = Area.objects.create(name="Manhattan", city=self.city)
        self.serializer = AreaSerializer(instance=self.area)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'city'])


class PropertySerializerTestCase(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            title="Test Property",
            sale_type=Property.SaleType.FOR_SALE,
            price=1000000,
            # Add other necessary fields here or update model to have sensible defaults/null as valid
        )
        self.serializer = PropertySerializer(instance=self.property)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'title', 'address', 'city', 'state', 'area', 'description',
                                            'sale_type', 'price', 'bedrooms', 'bathrooms', 'home_type',
                                            'square_fit', 'object_id', 'is_published', 'building_year',
                                            'best_offer', 'modx_id'])


class ImageSerializerTestCase(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            title="Test Property",
            sale_type=Property.SaleType.FOR_SALE,
            price=1000000,
            # Add other necessary fields here or update model to have sensible defaults/null as valid
        )
        self.image = Image.objects.create(
            property=self.property,
            # assuming you have some valid image file or object for testing, or use mocking for image file
        )
        self.serializer = ImageSerializer(instance=self.image)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'property', 'image'])
