from django.test import TestCase, Client
from django.urls import reverse
from .models import Dish, DishType, Cook, Order, OrderItem

class DishViewTests(TestCase):

    def setUp(self):
        self.user = Cook.objects.create_user(username='testuser', password='testpass')
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(name="Pasta", price=10.5, dish_type=self.dish_type)

    def test_dish_list_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dish_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")

    def test_dish_detail_view(self):
        response = self.client.get(reverse('dish_detail', args=[self.dish.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")

    def test_dish_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('dish_delete', args=[self.dish.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())


class MenuCartTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(name="Pasta", price=10.5, dish_type=self.dish_type)

    def test_menu_view(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")

    def test_add_to_cart(self):
        response = self.client.get(reverse('add_to_cart', args=[self.dish.id]))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session['cart']
        self.assertEqual(cart[str(self.dish.id)], 1)

    def test_view_cart(self):
        session = self.client.session
        session['cart'] = {str(self.dish.id): 2}
        session.save()
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")
        self.assertContains(response, "2")


class CheckoutTests(TestCase):

    def setUp(self):
        self.user = Cook.objects.create_user(username='testuser', password='testpass')
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(name="Pasta", price=10.5, dish_type=self.dish_type)
        self.client.login(username='testuser', password='testpass')

    def test_checkout_empty_cart(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('menu'))

    def test_checkout_with_items(self):
        session = self.client.session
        session['cart'] = {str(self.dish.id): 2}
        session.save()
        response = self.client.post(reverse('checkout'), {
            'address': '123 Street',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())


class OrderHistoryTests(TestCase):

    def setUp(self):
        self.user = Cook.objects.create_user(username='testuser', password='testpass')
        self.order = Order.objects.create(user=self.user, address='123 Street',)

    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.address)
