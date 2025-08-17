"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        equal_quantity = product.quantity
        assert product.check_quantity(
            equal_quantity)

        less_quantity = product.quantity - 1
        assert product.check_quantity(
            less_quantity)

        more_quantity = product.quantity + 1
        assert not product.check_quantity(
            more_quantity)


    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        equal_quantity = product.quantity
        product.buy(equal_quantity)
        assert product.quantity == 0

        less_quantity = product.quantity - 1
        product.buy(less_quantity)
        assert product.quantity == 1

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        more_quantity = product.quantity + 1
        with pytest.raises(ValueError):
            assert product.buy(more_quantity) is ValueError



class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        cart.add_product(product)
        assert product in cart.products
        assert cart.products[product] == 1

    def test_add_product_increment_if_exists(self, cart, product):
        cart.add_product(product, 2)
        cart.add_product(product, 3)
        assert cart.products[product] == 5

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_product_partial(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product_same_in_cart(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 5)
        assert cart.products[product] == 0

    def test_remove_all_product(self, cart, product):
        cart.add_product(product, 7)
        cart.remove_product(product, )
        assert product not in cart.products

    def test_remove_product_more_than_in_cart(self, product):
        cart = Cart()
        cart.add_product(product, 7)
        cart.remove_product(product, 10)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 800)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 5)
        assert cart.get_total_price() == product.price * 5

    def test_buy_success(self, cart, product):
        initial_quantity = product.quantity
        cart.add_product(product, 100)
        cart.buy()
        assert product.quantity == initial_quantity - 100
        assert len(cart.products) == 0

    def test_buy(self, cart, product):
        initial_quantity = product.quantity
        cart.add_product(product, initial_quantity + 1)
        with pytest.raises(ValueError):
            cart.buy()
        assert product.quantity == initial_quantity
        assert cart.products[product] == initial_quantity + 1

    def test_buy_not_enough_raises_and_keeps_state(self, cart, product):
        initial_quantity = product.quantity
        cart.add_product(product, initial_quantity + 1)
        with pytest.raises(ValueError):
            cart.buy()
        # состояние не меняется
        assert product.quantity == initial_quantity
        # корзина остаётся нетронутой
        assert cart.products[product] == initial_quantity + 1