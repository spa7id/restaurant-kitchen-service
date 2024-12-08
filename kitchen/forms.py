from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from .models import Cook, Dish, DishType, Order


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = ["name"]


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=Cook.objects.all(), widget=forms.CheckboxSelectMultiple, required=True
    )

    class Meta:
        model = Dish
        fields = ["name", "description", "price", "dish_type", "cooks"]


class CookForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        help_text="Унікальний ідентифікатор для входу в систему.",
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        required=True,
        help_text="Пароль має бути не менше 8 символів.",
    )

    class Meta:
        model = Cook
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "password",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Cook.objects.filter(username=username).exists():
            raise ValidationError(
                "Цей username вже зайнятий. Будь ласка, виберіть інший."
            )
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Пароль має бути не менше 8 символів.")
        return password

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance


class CookCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        required=True,
        help_text="Пароль має бути не менше 8 символів",
    )

    class Meta:
        model = Cook
        fields = ["first_name", "last_name", "email", "years_of_experience", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password"])
            user.save()
        return user


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address", "comment"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "comment": forms.Textarea(attrs={"rows": 2}),
        }
