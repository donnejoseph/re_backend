from api.views import PropertyList, PropertyDetail
from django.urls import path

urlpatterns = [
    path('properties/', PropertyList.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetail.as_view(), name='property-detail'),
]
