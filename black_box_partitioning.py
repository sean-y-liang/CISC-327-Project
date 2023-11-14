import pytest
from main import Account, Restaurant, RestaurantView

# Black box partitioning testing for the functionality of logging in


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
