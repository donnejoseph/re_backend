import logging
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from api.serializers import PropertyListSerializer, PropertyDetailSerializer
from api.models import Property

logger = logging.getLogger(__name__)


class PropertyList(ListAPIView):
    """
    List all properties.
    """
    serializer_class = PropertyListSerializer

    def get_queryset(self):
        return Property.objects.filter(is_published=True).order_by('-object_id')

    @swagger_auto_schema(
        operation_summary="List all properties",
        operation_description="List all properties",
        responses={
            200: PropertyListSerializer(many=True),
            400: "Bad Request",
            500: "Error communicating with the server. Please try again later."
        }
    )
    def list(self, request, *args, **kwargs):
        filters = {
            'address': 'address__icontains',
            'city': 'city__name__icontains',
            'state': 'state__icontains',
            'area': 'area__name__icontains',
            'sale_type': 'sale_type__icontains',
            'price_min': 'price__gte',
            'price_max': 'price__lte',
            'bedrooms': 'bedrooms__gte',
            'bathrooms': 'bathrooms__gte',
            'home_type': 'home_type__icontains',
            'square_fit_min': 'square_fit__gte',
            'square_fit_max': 'square_fit__lte',
            'object_id': 'object_id__icontains'
        }

        queryset = self.get_queryset()

        for param, filter_expr in filters.items():
            value = request.query_params.get(param)
            if value is not None:
                queryset = queryset.filter(**{filter_expr: value})

        serializer = self.serializer_class(queryset, many=True)
        try:
            return Response(serializer.data)
        except Exception as e:
            logger.error("Error while fetching properties: %s", str(e))
            return Response({"detail": "Error communicating with the server. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyDetail(APIView):
    """
    Retrieve a property instance.
    """
    queryset = Property.objects.filter(is_published=True)
    serializer_class = PropertyDetailSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve a property instance",
        operation_description="Retrieve a property instance",
        responses={
            200: PropertyDetailSerializer(),
            400: "Bad Request",
            500: "Error communicating with the server. Please try again later."
        }
    )
    def get(self, request, pk, format=None):
        try:
            property = self.queryset.get(pk=pk)
            serializer = self.serializer_class(property)
            return Response(serializer.data)
        except Property.DoesNotExist:
            raise NotFound(detail="Property not found")
        except Exception as e:
            logger.error("Error while fetching property: %s", str(e))
            return Response({"detail": "Error communicating with the server. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
