import pytest
from main import Account, Order, MenuItem, Restaurant, RestaurantView


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


def test_account_login():
    # Account creation
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com",
                             "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")

    # Neither the given user ID or password match account credentials
    assert account.login("wrongID", "wrongpassword") == False

    # Only given user ID does not match account user ID
    assert account.login("wrongID", "pass123") == False

    # Only given password does not match account password
    assert account.login("john_doe_123", "wrongpassword") == False

    # Given user ID and password match account credentials
    assert account.login("john_doe_123", "pass123") == True

# Black box partitioning testing for the functionality of viewing of restaurants


def test_find_restaurant():
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    popeyes = Restaurant("Popeyes", "American", "4.3")
    restaurants = RestaurantView([osmows, popeyes])

    # No input given for searching (0 is default rating filter)
    found_restaurant = restaurants.find_restaurant(
        "", "0", "")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"
    assert found_restaurant[1] == "Popeyes"
    assert len(found_restaurant) == 2

    # Only partial search term given
    found_restaurant = restaurants.find_restaurant(
        "Osm", "0", "")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"
    assert len(found_restaurant) == 1

    # Only search term given
    found_restaurant = restaurants.find_restaurant(
        "Osmow's", "0", "")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"
    assert len(found_restaurant) == 1

    # Only non-existant restaurant given as search term
    found_restaurant = restaurants.find_restaurant(
        "John's Pizzeria", "0", "")
    assert found_restaurant == []

    # Only cuisine filter given
    found_restaurant = restaurants.find_restaurant(
        "", "0", "American")
    assert found_restaurant != []
    assert found_restaurant[0] == "Popeyes"
    assert len(found_restaurant) == 1

    # Only non-existant cuisine filter given
    found_restaurant = restaurants.find_restaurant(
        "", "0", "Canadian")
    assert found_restaurant == []

    # Only rating filter given
    found_restaurant = restaurants.find_restaurant(
        "", "4.0", "")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"
    assert found_restaurant[1] == "Popeyes"
    assert len(found_restaurant) == 2

    # Only non-existant rating filter given
    found_restaurant = restaurants.find_restaurant(
        "", "-1", "")
    assert found_restaurant == []

    # Search term and cuisine filter given
    found_restaurant = restaurants.find_restaurant(
        "Os", "0", "Mediterranean")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"
    assert len(found_restaurant) == 1

    # Search term and rating filter given
    found_restaurant = restaurants.find_restaurant(
        "Os", "4.5", "")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"
    assert len(found_restaurant) == 1

    # Cuisine and rating filter given
    found_restaurant = restaurants.find_restaurant(
        "", "4.3", "Mediterranean")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"
    assert len(found_restaurant) == 1

    # Search term, cuisine filter, and rating filter given
    found_restaurant = restaurants.find_restaurant(
        "Osmow's", "4.8", "Mediterranean")
    assert found_restaurant != []
    assert found_restaurant[0] == "Osmow's"


