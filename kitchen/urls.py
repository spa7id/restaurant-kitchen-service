from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DishCreateView,
    DishListView,
    DishDetailView,
    DishUpdateView,
    DishDeleteView,
    DishTypeCreateView,
    CookerCreateView,
    home,
    RegisterView,
)

urlpatterns = [
    path("dish/create/", DishCreateView.as_view(), name="dish_create"),
    path("dish/", DishListView.as_view(), name="dish_list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish_detail"),
    path("dish/<int:pk>/edit/", DishUpdateView.as_view(), name="dish_update"),
    path("dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish_delete"),
    path("dish-type/create/", DishTypeCreateView.as_view(), name="create_dish_type"),
    path("cook/create/", CookerCreateView.as_view(), name="create_cook"),
    path("", home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name="register")


]
