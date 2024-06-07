from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from . import forms
from django.contrib.auth.decorators import login_required
from cars.models import Car
from user.models import Purchase
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import DetailView
from cars.models import Comment



class RegisterView(FormView):
    template_name = 'register.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'You have logged in successfully!')
        return super().form_valid(form)
    

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def buy_car(request, car_id):
    car = Car.objects.get(pk=car_id)

    if car.quantity > 0:  
        if request.method == 'POST':
            purchase = Purchase(user=request.user, car=car)
            purchase.save()

            car.quantity -= 1
            car.save()

            messages.success(request, f'You have successfully purchased {car.name}!')

            return redirect('home')
        
        return render(request, 'home', {'car': car})
    else:
        messages.error(request, f'Sorry, {car.name} is no longer available.')
        return redirect('home')

@login_required
def profile(request):
    user = request.user
    cars = Car.objects.filter(purchase__user=user)
    return render(request, 'profile.html', {'cars': cars})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserData(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserData(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': profile_form})

@login_required
def pass_change(request):
    if request.method == 'POST':
            form = PasswordChangeForm(request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password updated successfully!')
                update_session_auth_hash(request, form.user)
                return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
            
    return render(request, 'pass_change.html', {'form': form})



