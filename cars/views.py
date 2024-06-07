from django.shortcuts import render,redirect
from django.views.generic import DetailView
from .models import Car
from .models import Comment
from brands.models import Brand
from . import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def cars_by_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    brands = Brand.objects.all()
    cars = Car.objects.filter(brand=brand)
    return render(request, 'home.html', {'filtered_brand': brand, 'cars': cars, 'brands': brands})

class CarDetailView(DetailView):
    model = Car
    pk_url_kwarg = 'id'
    template_name = 'car_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = forms.CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = self.object
            new_comment.user = request.user
            new_comment.save()
            return redirect('details', id=self.object.id)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.all()
        comment_form = forms.CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context