from django.contrib import admin
from .models import Dish, DishType, Cook

admin.site.register(Dish)
admin.site.register(DishType)
admin.site.register(Cook)
