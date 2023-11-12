import pyodbc
import database_initialization
from datetime import datetime

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:cisc327-server.database.windows.net,1433;Database=db;Uid=CloudSAe60b9174;Pwd=Password123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

try:
    # Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Check if the connection was successful
    print("Connected to the database!")

    # Close the cursor and connection
    cursor.close()
    conn.close()

except pyodbc.Error as e:
    print("Error:", str(e))

"""
This class is used to define the methods that will information regarding the user and
their order(s) into the database.
"""


class DatabaseManager:
    # Creates connection to database
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = pyodbc.connect(connection_string)
        self.cursor = conn.cursor()

    # Saves user details in the database during account creation
    def save_user_details(self, user_id, user_name, user_email, user_password, user_address, user_phone, user_dropoff):
        insert_sql = "INSERT INTO Users (user_id, user_name, user_email, user_password, user_address, user_phone, user_dropoff) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(insert_sql, user_id, user_name, user_email,
                            user_password, user_address, user_phone, user_dropoff)
        self.conn.commit()

    # Allows user to update the user details in the database
    def update_user_details(self, user_id, user_name, user_email, user_password, user_address, user_phone, user_dropoff):
        update_sql = """
    UPDATE Users 
    SET user_name = ?, 
        user_email = ?,
        user_password = ?, 
        user_address = ?,
        user_phone = ?,
        user_dropoff= ? 
    WHERE user_id = ?
    """
        self.cursor.execute(update_sql, user_name, user_email, user_password,
                            user_address, user_phone, user_dropoff, user_id)
        self.conn.commit()

    # Allows the deletion of an account off the database
    def delete_user_details(self, user_id):
        delete_sql = "DELETE FROM Users WHERE user_id = ?"
        self.cursor.execute(delete_sql, user_id)
        self.conn.commit()

    # Saves payment method into database for a user
    def save_payment(self, payment_id, user_id, payment_method):
        insert_sql = "INSERT INTO PaymentMethods (payment_id, user_id, payment_method) VALUES (?, ?, ?)"
        self.cursor.execute(insert_sql, payment_id, user_id, payment_method)
        self.conn.commit()

    # Allows user to update payment information in the database
    def update_payment_details(self, payment_id, payment_method):
        update_sql = """
    UPDATE PaymentMethods 
    SET payment_method = ?
    WHERE payment_id = ?
    """
        self.cursor.execute(update_sql, payment_method, payment_id)
        self.conn.commit()

    # Allows the deletion of payment methods in the database
    def delete_payment(self, payment_id):
        delete_sql = "DELETE FROM PaymentMethods WHERE payment_id = ?"
        self.cursor.execute(delete_sql, payment_id)
        self.conn.commit()

    # Adds restaurant to database
    def add_restaurant(self, restaurant_id, name, cuisine, rating):
        insert_sql = "INSERT INTO Restaurants (restaurant_id, name, cuisine, rating) VALUES (?, ?, ?, ?)"
        self.cursor.execute(insert_sql, restaurant_id, name, cuisine, rating)
        self.conn.commit()

    # Updates restaurant information in database
    def update_restaurant_details(self, restaurant_id, name, cuisine, rating):
        update_sql = """
    UPDATE Restaurants
    SET name = ?,
        cuisine = ?,
        rating = ?
    WHERE restaurant_id = ?
    """
        self.cursor.execute(update_sql, name, cuisine, rating, restaurant_id)
        self.conn.commit()

    # Deletes a restaurant off the database
    def delete_restaurant(self, restaurant_id):
        delete_sql = "DELETE FROM Restaurants WHERE restaurant_id = ?"
        self.cursor.execute(delete_sql, restaurant_id)
        self.conn.commit()

    # Adds an item to a restaurant's menu in the database
    def add_menu_items(self, item_id, restaurant_id, name, price, options):
        insert_sql = "INSERT INTO MenuItems (item_id, restaurant_id, name, price, options) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(insert_sql, item_id,
                            restaurant_id, name, price, options)
        self.conn.commit()

    # Updates an item to a restaurant's menu in the database
    def update_menu_items(self, item_id, name, price, options):
        update_sql = """
    UPDATE MenuItems
    SET name = ?,
        price = ?,
        options = ?
    WHERE item_id = ?
    """
        self.cursor.execute(update_sql, name, price, options, item_id)
        self.conn.commit()

    # Deletes an item to a restaurant's menu in the database
    def delete_menu_items(self, item_id):
        delete_sql = "DELETE FROM MenuItems WHERE item_id = ?"
        self.cursor.execute(delete_sql, item_id)
        self.conn.commit()

    # Saves order details to the database
    def save_order(self, order_id, user_id, restaurant_id, total, status, order_time, order_details_id, item_id, quantity):
        insert_sql = "INSERT INTO Orders (order_id, user_id, restaurant_id, total, status, order_time) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(insert_sql, order_id, user_id,
                            restaurant_id, total, status, order_time)
        self.conn.commit()

        insert_sql = "INSERT INTO OrderDetails (order_details_id, order_id, item_id, quantity) VALUES (?, ?, ?, ?)"
        self.cursor.execute(insert_sql, order_details_id,
                            order_id, item_id, quantity)
        self.conn.commit()

    # Updates order status within the database
    def update_order(self, order_id, status):
        update_sql = """
    UPDATE Orders
    SET status = ?,
    WHERE order_id = ?
    """
        self.cursor.execute(update_sql, status, order_id)
        self.conn.commit()

    # Allows the deletion/cancellation of an order off the database
    def cancel_order(self, order_id):
        delete_sql = "DELETE FROM Orders WHERE order_id = ?"
        self.cursor.execute(delete_sql, order_id)
        self.conn.commit()

        delete_sql = "DELETE FROM OrderDEtails WHERE order_id = ?"
        self.cursor.execute(delete_sql, order_id)
        self.conn.commit()

    def save_review(self, review_id, order_id, user_id, review, rating, review_time):
        insert_sql = "INSERT INTO Reviews (review_id, order_id, user_id, review, rating, review_time) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(insert_sql, review_id, order_id,
                            user_id, review, rating, review_time)
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()


"""
This class is used to define a user's account details and allows them to login to their 
account, and potentially change account details.
"""


class Account:
    # The account is initialized as blank
    def __init__(self):
        self.user_name = None
        self.user_email = None
        self.user_id = None
        self.user_password = None
        self.user_address = None
        self.user_phone = None
        self.user_dropoff = None
        self.user_main_payment = None
        self.user_payment_methods = []

    def account_creation(self, user_name, user_id, user_email, user_password, user_address, user_phone, user_main_payment, user_dropoff):
        """
        Function that creates a new account for users with information such as their name, 
        user ID, email, address, phone number, password, payment method, and dropoff 
        location.
        """
        self.user_name = user_name
        self.user_id = user_id
        self.user_email = user_email
        self.user_password = user_password
        self.user_address = user_address
        self.user_phone = user_phone
        self.user_main_payment = user_main_payment
        self.user_payment_methods.append(self.user_main_payment)
        self.user_dropoff = user_dropoff

    def login(self, user_id, user_password):
        """
        Function that allows users to enter their user ID and password to be able to access 
        their account. 
        """
        if user_id == self.user_id and user_password == self.user_password:
            print("Successful Login!")
            return True
        else:
            print("Login Failed. Please Try Again.")
            return False

    def account_management(self, user_password, user_address, user_phone, user_main_payment, user_dropoff):
        """
        Function that allows users to edit account details such as their address, 
        phone number, password, payment method(s), and preferred drop off method. 
        """
        self.user_password = user_password
        self.user_address = user_address
        self.user_phone = user_phone
        self.user_main_payment = user_main_payment
        if self.user_main_payment not in self.user_payment_methods:
            self.user_payment_methods.append(self.user_main_payment)
        self.user_dropoff = user_dropoff
        print("All changes successful!")


"""
This class defines a restaurant object with important details regarding a restaurant like 
the name, cuisine and rating.
"""


class Restaurant:
    # Constructor to make a restaurant
    def __init__(self, name, cuisine, rating):
        self.name = name
        self.cuisine = cuisine
        self.rating = rating


"""
This class defines how users search for a restaurant from a list.
"""


class RestaurantView:
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def find_restaurant(self, search_term, rating_filter, cuisine_filter):
        """
        Function that allows users to search for a restaurant by name, cuisine, and/or 
        rating.
        """
        search_term = search_term.lower()
        cuisine_filter = cuisine_filter.lower()
        rating_filter = float(rating_filter)  # Ensure rating_filter is a float

        for restaurant in self.restaurants:
            if search_term == restaurant.name.lower() and \
               cuisine_filter == restaurant.cuisine.lower() and \
               rating_filter <= float(restaurant.rating):  # Convert restaurant rating to float

                print(f"{restaurant.name}\n {restaurant.cuisine} cuisine\n {restaurant.rating} stars")
                return restaurant

        print("No Results Found")
        return None



"""
This class defines an item in a restaurant's menu with important details such as name, 
price, and options. 
"""


class MenuItem:
    def __init__(self, name, price, options):
        self.name = name
        self.price = price
        self.quantity = 0
        self.options = options


"""
This class defines the mechanism to search through a restaurant's menu and select items 
to add to the cart, order, keep track of the order, rate it after it's delivered, and 
review any orders made in the past.
"""


class Order:
    def __init__(self, restaurant, items, past_orders):
        self.items = items
        self.cart = []
        self.order_details = {"restaurant": restaurant}
        self.progress = None
        self.past_orders = past_orders
        self.reviewed = False

    def add_menu_item(self, menu_item, quantity):
        """
        Function that allows users to add items to their cart.
        """
        menu_item.quantity = quantity
        self.cart.append(menu_item)
        print(f"{menu_item.name} added to cart")

    def view_cart(self):
        """
        Function that allows users to view their cart including items and the price.
        """

        sub_total = 0
        for item in self.cart:
            print(f"{item.name}\n Options: {item.options}\n Price: {item.price}\n \
        Quantity: {item.quantity}")
            sub_total += item.price * item.quantity

        total = sub_total * 1.23  # Assuming a fixed tax and delivery rate for simplicity
        print(f"Subtotal: ${sub_total}\n Total: ${total}")
        self.order_details["total"] = total

    def change_item_quantity(self, item_name, quantity):
        """
        Function that allows users to change the quantity of an item in their cart.
        """
        for item in self.cart:
            if item_name.lower() == item.name.lower():
                item.quantity = quantity
                print(f"{item.name} quantity changed to {quantity}")
                break

    def checkout(self, address, dropoff_location, payment_method, promotions, tips):
        """
        Function that allows users to change details regarding their order and checkout.
        """
        if address != "":
            self.order_details["address"] = address
            print(f"Address changed to {address}")
        if dropoff_location != "":
            self.order_details["dropoff_location"] = dropoff_location
            print(f"Dropoff location changed to {dropoff_location}")
        if payment_method != "":
            self.order_details["payment_method"] = payment_method
            print(f"Payment method changed to {payment_method}")

        self.order_details["total"] = self.order_details["total"] - promotions + tips
        print(f"Your order total is: ${self.order_details['total']}")
        print("Please confirm all details before proceeding.")

    def track_order_progress(self, order_id, estimated_time, progress):
        """
        Function to track the progress of an order, where an order_id is created for 
        reference. Currently, it simulates tracking by printing the order's status.
        """

        self.order_details["order_id"] = order_id
        self.order_details["estimated_time"] = estimated_time
        self.progress = progress
        print(f"Tracking progress of order {order_id} from \
    {self.order_details['restaurant']}")
        print(f"Estimated time until delivery: {estimated_time}")
        print(f"Status of delivery: {progress}")

    def restaurant_reviews(self, review):
        """
        Function to review orders made by the user.
        """
        
        if self.progress == "Delivered" and not self.reviewed:
            print("Thank you for ordering from us!")
            self.review = review
            self.reviewed = True
            print("Thank you for your review!")

    def order_history(self, order_id):
        """
        Function to display a user's order history.
        """

        for order in self.past_orders:
            if order_id == order.order_details["order_id"]:
                print(f"Order ID: {order.order_details['order_id']}\n \
        Restaurant: {order.order_details['restaurant']}\n \
        Date and Time: {order.order_details['date and time']}\n \
        Items Ordered: {order.cart}\n Total Cost: ${order.order_details['total']}\n")


"""
The main program creates instances of each of the classes in the rest of the program 
and tests that each of them, when given correct input, give the correct output, and 
that the objects work together to create a cohesive delivery app. The input info would 
be account details, restaurants, menu items for a restaurants, and information required 
to make an order and track it, these are all stored within a database.
"""
if __name__ == "__main__":
    # Initialize tables in the database and allow management
    database_initialization.main()
    database = DatabaseManager()

    # Creating, logging into, and changing details about user account
    account = Account()
    account.account_creation("John Doe", "john_doe_123", "johndoe@example.com", "pass123", "123 Elm Street", "555-1234", "Credit Card", "Front Door")
    # Inserting user into database
    database.save_user_details(account.user_id, account.user_name, account.user_email, account.user_password, account.user_address, account.user_phone, account.user_dropoff)
    database.save_payment("CC123456", account.user_id, account.user_main_payment)

    # Login and manage account details
    account.login("john_doe_123", "pass123")
    account.account_management("newpass123", "456 Oak Avenue", "555-5678", "Debit Card", "Side Gate")

    # Updating user details in database
    database.update_user_details(account.user_id, account.user_name, account.user_email, account.user_password, account.user_address, account.user_phone, account.user_dropoff)
    database.update_payment_details("CC123456", "Debit Card")

    # Creating restaurant examples
    osmows = Restaurant("Osmow's", "Mediterranean", "4.8")
    popeyes = Restaurant("Popeyes", "American", "4.3")

    # Adding restaurants to database
    database.add_restaurant("LocA_Osmows", osmows.name, osmows.cuisine, osmows.rating)
    database.add_restaurant("LocE_Popeyes", popeyes.name, popeyes.cuisine, popeyes.rating)

    # Creating a list of restaurants and searching
    restaurants = RestaurantView([osmows, popeyes])
    found_restaurant = restaurants.find_restaurant("Osmow's", "4.8", "Mediterranean")

    # Creating menu items for Osmow's
    fries = MenuItem("STIX", 3.38, {"Size": "Medium", "Extra Sauce": None})
    brownie = MenuItem("Brownie", 3.99, None)

    # Adding items to restaurant's menu in the database
    database.add_menu_items("Fries_Osmows", "STIX", 3.38, {"Size": "Medium", "Extra Sauce": "None"})
    database.add_menu_items("ChocBrownie_Osmows", "Brownie", 3.99, "None")

    # Creating an order from Osmow's and playing with the functionality of the cart,
    # tracking the order, and giving a review at the end
    order = Order("Osmow's", [fries, brownie], [])
    order.add_menu_item(fries, 2)
    order.add_menu_item(brownie, 1)
    order.view_cart()
    order.change_item_quantity("STIX", 3)
    order.checkout("789 Pine Road", "Back Door", "Credit Card", 0, 5)

    # Creating order within database
    database.save_order("#1Osmows", account.user_id, "LocA_Osmows", order.order_details["total"], "Order Confirmed", datetime.now(), "OrderDetail01", "Fries_Osmows", 3)

    # Tracking order progress
    order.track_order_progress("#1Osmows", "1 hour", "Order Confirmed")
    order.track_order_progress("#1Osmows", "10 mins", "Out for Delivery")
    order.track_order_progress("#1Osmows", "0 mins", "Delivered")

    # Updating delivery status in the database
    database.update_order("#1Osmows", "Delivered")

    # Adding a review for the order
    order.restaurant_reviews("Great food and fast delivery!")
    database.save_review("#1RevOsmows", "#1Osmows", account.user_id, "Great food and fast delivery!", 5, datetime.now())

    # Viewing order history
    order.order_history("#1Osmows")