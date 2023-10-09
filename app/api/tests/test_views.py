from django.urls import reverse
from rest_framework.test import APITestCase
from api.models import Property
from api.serializers import PropertyListSerializer, PropertyDetailSerializer


class PropertyListTests(APITestCase):
    def setUp(self):
        Property.objects.create(title='Prop1', is_published=True)
        Property.objects.create(title='Prop2', is_published=True)

    def test_list_properties_valid_request(self):
        response = self.client.get(reverse('property-list'))
        properties = Property.objects.filter(is_published=True).order_by('-object_id')
        serializer = PropertyListSerializer(properties, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_list_properties_with_params(self):
        response = self.client.get(reverse('property-list'), {'city': 'city1'})
        properties = Property.objects.filter(is_published=True, city__name__icontains='city1').order_by('-object_id')
        serializer = PropertyListSerializer(properties, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)


class PropertyDetailTests(APITestCase):
    def setUp(self):
        self.prop1 = Property.objects.create(title='Prop1', is_published=True)
        self.prop2 = Property.objects.create(title='Prop2', is_published=True)

    def test_get_property_valid_request(self):
        response = self.client.get(reverse('property-detail', kwargs={'pk': self.prop1.pk}))
        serializer = PropertyDetailSerializer(self.prop1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_get_property_invalid_request(self):
        response = self.client.get(reverse('property-detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 404)
