import pytest
from main import Order, MenuItem, Restaurant, RestaurantView

# Fixture for Order tests
@pytest.fixture
def sample_order():
    item = MenuItem("Burger", 10.00, None)
    return Order("Testaurant", [item], [])

# Fixture for RestaurantView tests
@pytest.fixture
def sample_restaurant_view():
    restaurants = [
        Restaurant("Osmow's", "Mediterranean", "4.8"),
        Restaurant("Popeyes", "American", "4.3")
    ]
    return RestaurantView(restaurants)


# Path Testing for Order.checkout
def test_checkout_path_1(sample_order):
    sample_order.add_menu_item(sample_order.items[0], 1)
    sample_order.view_cart()  
    sample_order.checkout("123 St", "Front Door", "Credit Card", 0, 5)
    assert sample_order.order_details["total"] == 17.3  

def test_checkout_path_2(sample_order):
    sample_order.add_menu_item(sample_order.items[0], 1)
    sample_order.view_cart()  
    sample_order.checkout("", "", "Debit Card", 10, 0)
    assert round(sample_order.order_details["total"], 1) == 2.3  # Rounding to one decimal place to avoid Python's floating-point precision issue


# Decision Coverage Testing for RestaurantView.find_restaurant
def test_find_restaurant_decision_1(sample_restaurant_view):
    result = sample_restaurant_view.find_restaurant("Osmow's", "4.8", "Mediterranean")
    assert result == ["Osmow's"]

def test_find_restaurant_decision_2(sample_restaurant_view):
    result = sample_restaurant_view.find_restaurant("Nonexistent", "5.0", "Italian")
    assert result == []
