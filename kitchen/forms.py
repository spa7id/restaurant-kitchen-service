from django import forms
from .models import Dish, DishType, Cook


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = ["name"]


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "description", "price", "dish_type", "cooks"]


class CookForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        required=True,
        help_text="Пароль має бути не менше 8 символів"
    )

    class Meta:
        model = Cook
        fields = ["first_name", "last_name", "email", "years_of_experience",
                  "password"]