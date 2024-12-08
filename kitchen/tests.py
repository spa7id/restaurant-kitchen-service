from django.test import Client, TestCase
from django.urls import reverse

from .forms import (CookCreationForm, CookForm, DishForm, DishTypeForm,
                    OrderForm)
from .models import (Cook, Dish, DishType,
                     Order)


class DishViewTests(TestCase):

    def setUp(self):
        self.user = Cook.objects.create_user(
            username="testuser", password="testpass"
        )
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Pasta", price=10.5, dish_type=self.dish_type
        )

    def test_dish_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("dish_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")

    def test_dish_detail_view(self):
        response = self.client.get(reverse("dish_detail", args=[self.dish.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")

    def test_dish_delete_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("dish_delete", args=[self.dish.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())


class MenuCartTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Pasta", price=10.5, dish_type=self.dish_type
        )

    def test_menu_view(self):
        response = self.client.get(reverse("menu"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")

    def test_add_to_cart(self):
        response = self.client.get(reverse("add_to_cart", args=[self.dish.id]))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session["cart"]
        self.assertEqual(cart[str(self.dish.id)], 1)

    def test_view_cart(self):
        session = self.client.session
        session["cart"] = {str(self.dish.id): 2}
        session.save()
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")
        self.assertContains(response, "2")


class CheckoutTests(TestCase):

    def setUp(self):
        self.user = Cook.objects.create_user(
            username="testuser", password="testpass"
        )
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Pasta", price=10.5, dish_type=self.dish_type
        )
        self.client.login(username="testuser", password="testpass")

    def test_checkout_empty_cart(self):
        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("menu"))

    def test_checkout_with_items(self):
        session = self.client.session
        session["cart"] = {str(self.dish.id): 2}
        session.save()
        response = self.client.post(
            reverse("checkout"),
            {
                "address": "123 Street",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())


class OrderHistoryTests(TestCase):

    def setUp(self):
        self.user = Cook.objects.create_user(
            username="testuser", password="testpass"
        )
        self.order = Order.objects.create(
            user=self.user,
            address="123 Street",
        )

    def test_order_history_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("order_history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.address)


###########


class DishTypeFormTests(TestCase):

    def test_valid_form(self):
        form_data = {"name": "Dessert"}
        form = DishTypeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_name(self):
        form_data = {"name": ""}
        form = DishTypeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_save_form(self):
        form_data = {"name": "Appetizer"}
        form = DishTypeForm(data=form_data)
        self.assertTrue(form.is_valid())
        dish_type = form.save()
        self.assertEqual(dish_type.name, "Appetizer")


class DishFormTests(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")
        self.cook = Cook.objects.create_user(
            username="testcook", password="password123"
        )

    def test_valid_form(self):
        form_data = {
            "name": "Pizza",
            "description": "Delicious pizza",
            "price": 15.0,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_name(self):
        form_data = {
            "name": "",
            "description": "Delicious pizza",
            "price": 15.0,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id],
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_save_form(self):
        form_data = {
            "name": "Pasta",
            "description": "Italian pasta",
            "price": 12.5,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())
        dish = form.save()
        self.assertEqual(dish.name, "Pasta")
        self.assertEqual(dish.price, 12.5)
        self.assertEqual(dish.dish_type, self.dish_type)
        self.assertIn(self.cook, dish.cooks.all())


class CookFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            "username": "testcook",
            "first_name": "Test",
            "last_name": "Cook",
            "email": "testcook@example.com",
            "years_of_experience": 5,
            "password": "password123",
        }
        form = CookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_existing_username(self):
        Cook.objects.create_user(username="testcook", password="password123")
        form_data = {
            "username": "testcook",
            "first_name": "Test",
            "last_name": "Cook",
            "email": "testcook2@example.com",
            "years_of_experience": 5,
            "password": "password123",
        }
        form = CookForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_invalid_form_short_password(self):
        form_data = {
            "username": "newcook",
            "first_name": "New",
            "last_name": "Cook",
            "email": "newcook@example.com",
            "years_of_experience": 3,
            "password": "short",
        }
        form = CookForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_save_form(self):
        form_data = {
            "username": "cook123",
            "first_name": "Cook",
            "last_name": "Test",
            "email": "cook123@example.com",
            "years_of_experience": 3,
            "password": "password123",
        }
        form = CookForm(data=form_data)
        self.assertTrue(form.is_valid())
        cook = form.save()
        self.assertEqual(cook.username, "cook123")
        self.assertTrue(cook.check_password("password123"))


class CookCreationFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            "first_name": "Cook",
            "last_name": "Test",
            "email": "cooktest@example.com",
            "years_of_experience": 3,
            "password": "password123",
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_save_form(self):
        form_data = {
            "first_name": "Cook",
            "last_name": "Test",
            "email": "cooktest@example.com",
            "years_of_experience": 3,
            "password": "password123",
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        cook = form.save()
        self.assertEqual(cook.first_name, "Cook")
        self.assertTrue(cook.check_password("password123"))


class OrderFormTests(TestCase):

    def setUp(self):
        self.user = Cook.objects.create_user(
            username="testuser", password="password123"
        )

    def test_valid_form(self):
        form_data = {"address": "123 Street", "comment": "Test order"}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_address(self):
        form_data = {"address": "", "comment": "Test order"}
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("address", form.errors)

    def test_save_form(self):
        form_data = {"address": "123 Street", "comment": "Test order"}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        order = form.save(commit=False)
        order.user = self.user
        order.save()
        self.assertEqual(order.address, "123 Street")
        self.assertEqual(order.comment, "Test order")
