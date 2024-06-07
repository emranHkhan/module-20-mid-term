from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:id>/', views.CarDetailView.as_view(), name='details'),
    path('brand/<int:brand_id>/', views.cars_by_brand, name='cars_by_brand'),
]
