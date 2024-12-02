from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)
from .models import Dish, DishType, Cook
from .forms import DishForm, DishTypeForm, CookForm
from django.contrib.auth.hashers import make_password



class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = "dish_create.html"
    success_url = reverse_lazy("dish_list")


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    template_name = "dish_list.html"
    context_object_name = "dishes"


class DishDetailView(DetailView):
    model = Dish
    template_name = "dish_detail.html"
    context_object_name = "dish"


class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "dish_update.html"
    success_url = reverse_lazy("dish_list")


class DishDeleteView(DeleteView):
    model = Dish
    template_name = "dish_confirm_delete.html"
    success_url = reverse_lazy("dish_list")

class DishTypeCreateView(CreateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "dish_type_create.html"
    success_url = reverse_lazy("dish_list")

class CookerCreateView(CreateView):
    model = Cook
    form_class = CookForm
    template_name = "cook_create.html"
    success_url = reverse_lazy("dish_list")

    def form_valid(self, form):
        if not form.instance.username:
            form.instance.username = f"{form.instance.first_name.lower()}.{form.instance.last_name.lower()}{get_random_string(4)}"
        form.instance.password = make_password(form.cleaned_data["password"])
        return super().form_valid(form)

def home(request):
    num_dish_types = DishType.objects.count()
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()


    return render(request, 'index.html', {
        'num_dish_types': num_dish_types,
        'num_cooks': num_cooks,
        'num_dishes': num_dishes,
    })


class DishTypeCreateView(CreateView):
    model = DishType
    form_class = DishTypeForm
    template_name = 'dish_type_create.html'
    success_url = '/'  # або інший URL після успішного створення

    def form_valid(self, form):
        return super().form_valid(form)

class DishTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "dish_type_update.html"
    success_url = reverse_lazy("dish_list")

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("login")