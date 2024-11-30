from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)
from .models import Dish
from .forms import DishForm


class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = "dish_create.html"
    success_url = reverse_lazy("dish_list")


class DishListView(ListView):
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
