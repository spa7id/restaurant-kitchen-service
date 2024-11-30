from django.urls import path
from .views import (
    DishCreateView,
    DishListView,
    DishDetailView,
    DishUpdateView,
    DishDeleteView,
)

urlpatterns = [
    path("dish/create/", DishCreateView.as_view(), name="dish_create"),
    path("dish/", DishListView.as_view(), name="dish_list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish_detail"),
    path("dish/<int:pk>/edit/", DishUpdateView.as_view(), name="dish_update"),
    path("dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish_delete"),
]
