from django.shortcuts import render
from brands.models import Brand
from cars.models import Car

def home(request):
    cars = Car.objects.all()
    brands = Brand.objects.all()

    return render(request, 'home.html', {'cars': cars, 'brands': brands})