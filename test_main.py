import pytest
from main import Account, Restaurant, RestaurantView, MenuItem, Order
from datetime import datetime

# Account Tests
def test_account_creation():
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com", "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")
    assert account.user_name == "John Doe"
    assert account.user_email == "johndoe@example.com"

def test_account_login():
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com", "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")
    assert account.login("john_doe_123", "pass123") == True
    assert account.login("john_doe_123", "wrongpassword") == False

def test_account_management():
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com", "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")
    account.account_management("newpass123", "456 Oak Avenue", "555-5678", "Debit Card", "Side Gate")
    assert account.user_password == "newpass123"
    assert account.user_address == "456 Oak Avenue"


# RestaurantView Tests
def test_find_restaurant():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    popeyes = Restaurant("Popeyes", "American", "4.3")
    restaurants = RestaurantView([osmows, popeyes])
    found_restaurant = restaurants.find_restaurant("Osmow's", "4.8", "Mediterranean")
    assert found_restaurant is not None
    assert found_restaurant.name == "Osmow's"


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