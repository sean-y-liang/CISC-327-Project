import pytest
from main import Account, Restaurant, RestaurantView, MenuItem, Order
from datetime import datetime

# Account Tests


def test_account_creation():
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com",
                             "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")
    assert account.user_name == "John Doe"
    assert account.user_email == "johndoe@example.com"


def test_account_login():
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com",
                             "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")
    assert account.login("john_doe_123", "pass123") == True
    assert account.login("john_doe_123", "wrongpassword") == False


def test_account_management():
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com",
                             "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")
    account.account_management(
        "newpass123", "456 Oak Avenue", "555-5678", "Debit Card", "Side Gate")
    assert account.user_password == "newpass123"
    assert account.user_address == "456 Oak Avenue"


# RestaurantView Tests
def test_find_restaurant():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    popeyes = Restaurant("Popeyes", "American", "4.3")
    restaurants = RestaurantView([osmows, popeyes])
    found_restaurant = restaurants.find_restaurant(
        "Osmow's", "4.8", "Mediterranean")
    assert found_restaurant is not []
    assert found_restaurant[0] == "Osmow's"


# MenuItem Tests
def test_menu_item_initialization():
    fries = MenuItem("Fries", 2.99, {"Size": "Medium", "Extras": "Cheese"})
    assert fries.name == "Fries"
    assert fries.price == 2.99
    assert fries.options == {"Size": "Medium", "Extras": "Cheese"}


# Order Tests
def test_add_menu_item():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    fries = MenuItem("Fries", 2.99, {"Size": "Medium", "Extras": "Cheese"})
    brownie = MenuItem("Brownie", 3.99, None)
    order = Order(osmows.name, [fries, brownie], [])
    order.add_menu_item(fries, 2)
    assert len(order.cart) == 1
    assert order.cart[0].name == "Fries"
    assert order.cart[0].quantity == 2


def test_change_item_quantity():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    fries = MenuItem("Fries", 2.99, {"Size": "Medium", "Extras": "Cheese"})
    order = Order(osmows.name, [fries], [])
    order.add_menu_item(fries, 2)
    order.change_item_quantity("Fries", 3)
    assert order.cart[0].quantity == 3


def test_track_order_progress():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    order = Order(osmows.name, [], [])
    order.track_order_progress("Order123", "30 mins", "Preparing")
    assert order.order_details["order_id"] == "Order123"
    assert order.order_details["estimated_time"] == "30 mins"
    assert order.progress == "Preparing"


def test_restaurant_reviews():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    order = Order(osmows.name, [], [])
    order.progress = "Delivered"
    order.restaurant_reviews("Great!")
    assert order.review == "Great!"
    assert order.reviewed is True


def test_checkout_payment():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    fries = MenuItem("Fries", 2.99, {"Size": "Medium", "Extras": "Cheese"})
    payment = Order(osmows.name, [fries], [])
    payment.add_menu_item(fries, 1)
    payment.view_cart()  # This should initialize the 'total' in order_details
    payment.checkout("123 Elm Street", "Front Door", "Credit Card", 0, 5)
    assert payment.order_details["payment_method"] == "Credit Card"
