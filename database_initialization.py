def main():
    import pyodbc

    connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:cisc327-server.database.windows.net,1433;Database=db;Uid=CloudSAe60b9174;Pwd=Password123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Define table creation queries with checks
    table_creation_queries = {
        "Users": """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users')
            BEGIN
                CREATE TABLE Users (
                    user_id INT IDENTITY PRIMARY KEY,
                    user_name NVARCHAR(255) NOT NULL,
                    user_email NVARCHAR(255) NOT NULL UNIQUE,
                    user_password NVARCHAR(255) NOT NULL,
                    user_address NVARCHAR(MAX),
                    user_phone NVARCHAR(20),
                    user_dropoff NVARCHAR(MAX)
                )
            END
        """,
        "PaymentMethods": """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PaymentMethods')
            BEGIN
                CREATE TABLE PaymentMethods (
                    payment_id INT IDENTITY PRIMARY KEY,
                    user_id INT,
                    payment_method NVARCHAR(50),
                    FOREIGN KEY (user_id) REFERENCES Users(user_id)
                )
            END
        """,
        "Restaurants": """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Restaurants')
            BEGIN
                CREATE TABLE Restaurants (
                    restaurant_id INT IDENTITY PRIMARY KEY,
                    name NVARCHAR(255) NOT NULL,
                    cuisine NVARCHAR(100),
                    rating DECIMAL(2,1)
                )
            END
        """,
        "MenuItems": """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'MenuItems')
            BEGIN
                CREATE TABLE MenuItems (
                    item_id INT IDENTITY PRIMARY KEY,
                    restaurant_id INT,
                    name NVARCHAR(255) NOT NULL,
                    price MONEY NOT NULL,
                    options NVARCHAR(MAX),
                    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
                )
            END
        """,
        "Orders": """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Orders')
            BEGIN
                CREATE TABLE Orders (
                    order_id INT IDENTITY PRIMARY KEY,
                    user_id INT,
                    restaurant_id INT,
                    total MONEY NOT NULL,
                    status NVARCHAR(50),
                    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),
                    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
                )
            END
        """,
        "OrderDetails": """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'OrderDetails')
            BEGIN
                CREATE TABLE OrderDetails (
                    order_details_id INT IDENTITY PRIMARY KEY,
                    order_id INT,
                    item_id INT,
                    quantity INT,
                    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                    FOREIGN KEY (item_id) REFERENCES MenuItems(item_id)
                )
            END
        """,
        "Reviews": """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Reviews')
            BEGIN
                CREATE TABLE Reviews (
                    review_id INT IDENTITY PRIMARY KEY,
                    order_id INT,
                    user_id INT,
                    review NVARCHAR(MAX),
                    rating DECIMAL(2,1),
                    review_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                    FOREIGN KEY (user_id) REFERENCES Users(user_id)
                )
            END
        """
    }

    # Execute each table creation query if the table doesn't exist
    for table, query in table_creation_queries.items():
        cursor.execute(query)

    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
