from faker import Faker
import random
from typing import Dict

fake = Faker()

def generate_age() -> int:
    """
    Generate a realistic age for a customer. The age is drawn from a normal distribution
    centered around 35 with a standard deviation of 10, but is then clamped to be within
    the range of 18 to 70.

    Returns:
        int: An integer representing the generated age, constrained between 18 and 70.
    """
    age = int(random.normalvariate(35, 10))
    return max(18, min(age, 70))  # Ensure age is within a realistic range

def generate_customer(customer_id: int) -> Dict[str, str or float]:
    """
    Generate a dictionary representing a customer with various personal details.

    Parameters:
        customer_id (int): The unique identifier for the customer.

    Returns:
        dict: A dictionary containing the customer's ID, full name, email address, age,
              phone number, address, and marital status.
    """
    return {
        "CustomerID": customer_id,
        "FullName": fake.name(),
        "EmailAddress": fake.email(),
        "Age": generate_age(),
        "PhoneNumber": fake.phone_number(),
        "Address": fake.address(),
        "Married": fake.random_element(elements=("Yes", "No"))
    }

def generate_product(product_id: int) -> Dict[str, str or float]:
    """
    Generate a dictionary representing a product with a name and price.
    The price range varies depending on the product ID.

    Parameters:
        product_id (int): The unique identifier for the product.

    Returns:
        dict: A dictionary containing the product's ID, name, and price. Price varies
              depending on whether the product ID modulo 3 equals 0, 1, or 2.
    """
    # Different price ranges for different types of products
    price_range = (20, 1000) if product_id % 3 == 0 else (5, 100) if product_id % 3 == 1 else (1, 50)
    return {
        "ProductID": product_id,
        "ProductName": fake.word().capitalize(),
        "Price": round(random.uniform(*price_range), 2)
    }

def generate_order(order_id: int, customer_id: int, product_id: int, order_date: str, quantity: int) -> Dict[str, str or float]:
    """
    Generate a dictionary representing an order, linking a customer to a product and including order details.

    Parameters:
        order_id (int): The unique identifier for the order.
        customer_id (int): The unique identifier of the customer placing the order.
        product_id (int): The unique identifier of the ordered product.
        order_date (str): The date the order was placed.
        quantity (int): The quantity of the product ordered.

    Returns:
        dict: A dictionary containing the order's ID, the customer's ID, the order date,
              the product's ID, and the quantity of the product ordered.
    """
    return {
        "OrderID": order_id,
        "CustomerID": customer_id,
        "OrderDate": order_date,
        "ProductID": product_id,
        "Quantity": quantity
    }
