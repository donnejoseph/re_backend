from django.test import TestCase

from api.models import City, Area, Property, Image


class PropertyModelTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Test City", population=100000)
        self.area = Area.objects.create(name="Test Area", city=self.city)
        self.property = Property.objects.create(
            title="Test Property",
            address="123 Test St",
            state="Test State",
            area=self.area,
            description="Test Description",
            sale_type=Property.SaleType.FOR_SALE,
            price=100000,
            bedrooms=3,
            bathrooms=2,
            home_type=Property.HomeType.APARTMENT,
            square_fit=1500,
            object_id="12345",
            best_offer=False,
            modx_id="54321",
        )
        self.image = Image.objects.create(title="Test Image", property=self.property)

    def test_property_model(self):
        property = Property.objects.get(title="Test Property")
        self.assertEqual(property.title, "Test Property")
        self.assertEqual(property.city.count(), 1)
        self.assertEqual(property.city.first().name, "Test City")
        self.assertEqual(property.area.name, "Test Area")
        self.assertEqual(property.images.count(), 1)

    def test_image_model(self):
        image = Image.objects.get(title="Test Image")
        self.assertEqual(image.title, "Test Image")
        self.assertEqual(image.property.title, "Test Property")

class CityModelTestCase(TestCase):
    def test_city_model(self):
        city = City.objects.create(name="Test City", population=100000)
        self.assertEqual(city.name, "Test City")
        self.assertEqual(city.population, "100000")

class AreaModelTestCase(TestCase):
    def test_area_model(self):
        city = City.objects.create(name="Test City", population=100000)
        area = Area.objects.create(name="Test Area", city=city)
        self.assertEqual(area.name, "Test Area")
        self.assertEqual(area.city.name, "Test City")
