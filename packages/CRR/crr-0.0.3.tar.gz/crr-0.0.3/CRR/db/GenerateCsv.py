from CRR.db.data_generator import generate_customer, generate_product, generate_order
import pandas as pd
import random
from faker import Faker
from typing import Tuple

fake = Faker()


def modify_order_dates(customer_id: int, num_customers: int) -> Tuple[str, str]:
    """
    Modify order dates to introduce variation based on customer segments, simulating different
    levels of customer engagement over time.

    Parameters:
        customer_id (int): Unique identifier for the customer.
        num_customers (int): Total number of customers in the dataset.

    Returns:
        Tuple[str, str]: Start and end dates for generating random order dates, with more recent
                         dates for more engaged customer segments.
    """
    if customer_id <= num_customers // 3:
        return '-30d', 'today'
    elif customer_id <= 2 * num_customers // 3:
        return '-90d', 'today'
    else:
        return '-1y', 'today'

def adjust_order_quantity(customer_id: int, num_customers: int) -> int:
    """
    Adjust order quantities based on customer segmentation to simulate different purchasing behaviors.

    Parameters:
        customer_id (int): Unique identifier for the customer.
        num_customers (int): Total number of customers in the dataset.

    Returns:
        int: The quantity of the product ordered, with higher quantities for less frequent customers
             to simulate bulk buying behavior.
    """
    return random.randint(1, 5) if customer_id <= num_customers // 2 else random.randint(5, 10)

def generate_customers(num_customers: int) -> pd.DataFrame:
    """
    Generate a DataFrame of customers with detailed personal and contact information.

    Parameters:
        num_customers (int): The number of customers to generate.

    Returns:
        pd.DataFrame: A DataFrame containing detailed information for each customer, including
                      unique identifiers and personal attributes.
    """
    customers = [generate_customer(i) for i in range(1, num_customers + 1)]
    pd.DataFrame(customers).to_csv("data/customers.csv")
    return pd.DataFrame(customers)

def generate_products(num_products: int) -> pd.DataFrame:
    """
    Generate a DataFrame of products with variable pricing and naming.

    Parameters:
        num_products (int): The number of products to generate.

    Returns:
        pd.DataFrame: A DataFrame containing product details such as product ID, name, and price.
    """
    products = [generate_product(i) for i in range(1, num_products + 1)]
    pd.DataFrame(products).to_csv("data/products.csv")
    return pd.DataFrame(products)

def generate_orders(num_customers: int, num_products: int, num_orders: int) -> pd.DataFrame:
    """
    Generate a DataFrame of orders, linking customers and products with additional details like order dates and quantities.

    Parameters:
        num_customers (int): Total number of customers in the dataset.
        num_products (int): Total number of products available for order.
        num_orders (int): Number of orders to generate.

    Returns:
        pd.DataFrame: A DataFrame containing order details, linking customer IDs with product IDs and including
                      the date and quantity of each order.
    """
    orders = []
    for i in range(1, num_orders + 1):
        customer_id = random.choice(range(1, num_customers + 1))
        product_id = random.choice(range(1, num_products + 1))
        start_date, end_date = modify_order_dates(customer_id, num_customers)
        order_date = fake.date_between(start_date=start_date, end_date=end_date)
        quantity = adjust_order_quantity(customer_id, num_customers)
        orders.append(generate_order(i, customer_id, product_id, order_date, quantity))
        pd.DataFrame(orders).to_csv("data/orders.csv")
    return pd.DataFrame(orders)

def save_to_csv(df: pd.DataFrame, filename: str):
    """
    Save a DataFrame to a CSV file.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        filename (str): The path or filename to which the DataFrame should be saved.

    Returns:
        None
    """
    df.to_csv(f'data/{filename}', index=False)