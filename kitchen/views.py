from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CookForm, DishForm, DishTypeForm, OrderForm
from .models import Cook, Dish, DishType, Order, OrderItem


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
    success_url = reverse_lazy('dish_list')

    def form_valid(self, form):
        return super().form_valid(form)


class DishTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "dish_type_update.html"
    success_url = reverse_lazy("dish_list")


class RegisterView(CreateView):
    form_class = CookForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request,
                         "Account created successfully. Please log in.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request,
                       "Registration failed. Please fix the errors below.")
        return self.render_to_response(self.get_context_data(form=form))


def menu_view(request):
    dishes = Dish.objects.all()
    return render(request, 'menu.html', {'dishes': dishes})


def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.session.get('cart', {})

    if str(dish.id) in cart:
        cart[str(dish.id)] += 1
    else:
        cart[str(dish.id)] = 1

    request.session['cart'] = cart

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(
            {'message': 'Страва додана в кошик!', 'dish_id': dish.id}
        )

    return redirect('menu')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for dish_id, quantity in cart.items():
        dish = get_object_or_404(Dish, id=dish_id)
        cart_items.append({'dish': dish, 'quantity': quantity,
                           'total_price': dish.price * quantity})
        total_price += dish.price * quantity
    return render(request, 'cart.html', {'cart_items': cart_items,
                                         'total_price': total_price})


def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})

    if str(dish_id) in cart:
        del cart[str(dish_id)]
        request.session['cart'] = cart

    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for dish_id, quantity in cart.items():
                dish = get_object_or_404(Dish, id=dish_id)
                OrderItem.objects.create(
                    order=order, dish=dish, quantity=quantity
                )
            request.session['cart'] = {}
            return redirect('order_history')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form})


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})
