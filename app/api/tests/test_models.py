from django.test import TestCase
from api.models import City, Area, Property, Image
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image as PILImage


class CityModelTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Test City", population="1000000")

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Test City")
        self.assertEqual(self.city.population, "1000000")
        self.assertEqual(self.city.__str__(), "Test City")


class AreaModelTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Test City", population="1000000")
        self.area = Area.objects.create(name="Test Area", city=self.city)

    def test_area_creation(self):
        self.assertEqual(self.area.name, "Test Area")
        self.assertEqual(self.area.city, self.city)
        self.assertEqual(self.area.__str__(), "Test Area")


class PropertyModelTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="New York", population="8000000")
        self.area = Area.objects.create(name="Manhattan", city=self.city)
        self.property = Property.objects.create(
            title="Test Property",
            address="123 Main St",
            state="NY",
            area=self.area,
            sale_type=Property.SaleType.FOR_SALE,
            price=Decimal('1000000'),
            bedrooms=3,
            bathrooms=2,
            home_type=Property.HomeType.APARTMENT,
            square_fit=1500,
            object_id="123456",
            is_published=True,
            building_year="2000",
            best_offer=False,
            modx_id="789012",
        )
        self.property.city.set([self.city])

    def test_property_creation(self):
        self.assertEqual(self.property.title, "Test Property")
        self.assertEqual(self.property.address, "123 Main St")
        self.assertEqual(self.property.state, "NY")
        self.assertEqual(self.property.area, self.area)
        self.assertEqual(self.property.sale_type, Property.SaleType.FOR_SALE)
        self.assertEqual(self.property.price, Decimal('1000000'))
        self.assertEqual(self.property.bedrooms, 3)
        self.assertEqual(self.property.bathrooms, 2)
        self.assertEqual(self.property.home_type, Property.HomeType.APARTMENT)
        self.assertEqual(self.property.square_fit, 1500)
        self.assertEqual(self.property.object_id, "123456")
        self.assertEqual(self.property.is_published, True)
        self.assertEqual(self.property.building_year, "2000")
        self.assertEqual(self.property.best_offer, False)

    def test_city_relation(self):
        """
        Test the relation between Property and City model.
        """
        self.assertEqual(self.property.city.first().name, self.city.name)

    def test_area_relation(self):
        """
        Test the relation between Property and Area model.
        """
        self.assertEqual(self.property.area.name, self.area.name)

    def test_string_representation(self):
        """
        Test the string representation of Property model instance.
        """
        self.assertEqual(str(self.property), "Test Property")


class ImageModelTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="New York", population="8000000")
        self.area = Area.objects.create(name="Manhattan", city=self.city)
        self.property = Property.objects.create(
            title="Test Property",
            address="123 Main St",
            state="NY",
            area=self.area,
            sale_type=Property.SaleType.FOR_SALE,
            price=1000000,
            bedrooms=3,
            bathrooms=2,
            home_type=Property.HomeType.APARTMENT,
            square_fit=1500,
            object_id="123456",
            is_published=True,
            building_year="2000",
            best_offer=False,
            modx_id="789012",
        )
        self.property.city.set([self.city])
        image = PILImage.new('RGB', (100, 100))
        file = io.BytesIO()
        image.save(file, 'JPEG')
        file.name = 'test.jpg'
        file.seek(0)
        uploaded_image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpeg')

        self.image = Image.objects.create(
            title="Test Image",
            image=uploaded_image,
            property=self.property
        )

    def test_image_creation(self):
        self.assertEqual(self.image.title, "Test Image")
        self.assertEqual(self.image.property, self.property)

    def test_property_relation(self):
        self.assertEqual(self.image.property.title, "Test Property")
