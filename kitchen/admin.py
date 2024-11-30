from django.contrib import admin
from .models import Dish, DishType, Cook
from .forms import DishForm, DishTypeForm, CookForm


class DishAdmin(admin.ModelAdmin):
    form = DishForm
    list_display = ["name", "dish_type", "price"]
    search_fields = ["name"]
    list_filter = ["dish_type"]


class DishTypeAdmin(admin.ModelAdmin):
    form = DishTypeForm
    list_display = ["name"]
    search_fields = ["name"]


class CookAdmin(admin.ModelAdmin):
    form = CookForm
    list_display = ["first_name", "last_name", "years_of_experience"]
    search_fields = ["first_name", "last_name"]


admin.site.register(Dish, DishAdmin)
admin.site.register(DishType, DishTypeAdmin)
admin.site.register(Cook, CookAdmin)
