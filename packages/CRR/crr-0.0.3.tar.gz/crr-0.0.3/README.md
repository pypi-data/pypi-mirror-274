# Mkdocs Weblink: https://areg-hovakimyan.github.io/CRR/


# API Documentation

This API is designed to manage customers, products, orders, modeling, and churn rates for a retail business application.

## Setup

Follow these steps to get your API up and running on your local machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/areg-hovakimyan/CRR
    ```
2. **Move to project directory**
   ```bash
   cd CRR
    ```
3. **Install required libraries**
   ```bash
   pip install -r requirements.txt
    ```    

3. **Run the Application**
   ```bash
   uvicorn run:app 
    ```       



### Base URL

All URLs referenced in the documentation have the following base:

http://127.0.0.1:8000/docs

### Customer Endpoints

- **Get Customer Emails by Cluster**
  - `Get /emails/`
  - Creates a new customer record.
  - Swagger UI: [Get Emails by Cluster](http://127.0.0.1:8000/docs#/default/get_customer_emails_by_cluster_customers_cluster__cluster_id__emails_get)

- **Create a Customer**
  - `POST /customers/`
  - Creates a new customer record.
  - Swagger UI: [Create Customer](http://127.0.0.1:8000/docs#/default/create_customer_customers__post)

- **Get a Customer**
  - `GET /customers/{customer_id}`
  - Retrieves a customer by ID.
  - Swagger UI: [Get Customer](http://127.0.0.1:8000/docs#/default/get_customer_customers__customer_id__get)

- **Delete a Customer**
  - `DELETE /customers/{customer_id}`
  - Deletes a customer by ID.
  - Swagger UI: [Delete Customer](http://127.0.0.1:8000/docs#/default/delete_customer_customers__customer_id__delete)

- **Update a Customer**
  - `PATCH /customers/{customer_id}`
  - Updates an existing customer.
  - Swagger UI: [Update Customer](http://127.0.0.1:8000/docs#/default/update_customer_customers__customer_id__patch)

### Product Endpoints

- **Create a Product**
  - `POST /products/`
  - Creates a new product record.
  - Swagger UI: [Create Product](http://127.0.0.1:8000/docs#/default/create_product_products__post)

- **Get a Product**
  - `GET /products/{product_id}`
  - Retrieves a product by ID.
  - Swagger UI: [Get Product](http://127.0.0.1:8000/docs#/default/get_product_products__product_id__get)

- **Delete a Product**
  - `DELETE /products/{product_id}`
  - Deletes a product by ID.
  - Swagger UI: [Delete Product](http://127.0.0.1:8000/docs#/default/delete_product_products__product_id__delete)

- **Update a Product**
  - `PATCH /products/{product_id}`
  - Updates an existing product.
  - Swagger UI: [Update Product](http://127.0.0.1:8000/docs#/default/update_product_products__product_id__patch)

### Order Endpoints

- **Create an Order**
  - `POST /orders/`
  - Creates a new order.
  - Swagger UI: [Create Order](http://127.0.0.1:8000/docs#/default/create_order_orders__post)

- **Get an Order**
  - `GET /orders/{order_id}`
  - Retrieves an order by ID.
  - Swagger UI: [Get Order](http://127.0.0.1:8000/docs#/default/get_order_orders__order_id__get)

- **Delete an Order**
  - `DELETE /orders/{order_id}`
  - Deletes an order by ID.
  - Swagger UI: [Delete Order](http://127.0.0.1:8000/docs#/default/delete_order_orders__order_id__delete)

- **Update an Order**
  - `PATCH /orders/{order_id}`
  - Updates an existing order.
  - Swagger UI: [Update Order](http://127.0.0.1:8000/docs#/default/update_order_orders__order_id__patch)

### Modeling Endpoints

- **Create a Modeling Record**
  - `POST /modeling/`
  - Creates a new modeling record for a customer.
  - Swagger UI: [Create Modeling](http://127.0.0.1:8000/docs#/default/create_modeling_modeling__post)

- **Get a Modeling Record**
  - `GET /modeling/{customer_id}`
  - Retrieves a modeling record by customer ID.
  - Swagger UI: [Get Modeling](http://127.0.0.1:8000/docs#/default/get_modeling_modeling__customer_id__get)

- **Delete a Modeling Record**
  - `DELETE /modeling/{customer_id}`
  - Deletes a modeling record by customer ID.
  - Swagger UI: [Delete Modeling](http://127.0.0.1:8000/docs#/default/delete_modeling_modeling__customer_id__delete)

- **Update a Modeling Record**
  - `PATCH /modeling/{customer_id}`
  - Updates an existing modeling record.
  - Swagger UI: [Update Modeling](http://127.0.0.1:8000/docs#/default/update_modeling_modeling__customer_id__patch)

### Churn Rate Endpoints

- **Create a Churn Rate Record**
  - `POST /churnrate/`
  - Creates a new churn rate record.
  - Swagger UI: [Create Churn Rate](http://127.0.0.1:8000/docs#/default/create_churnrate_churnrate__post)

- **Get a Churn Rate Record**
  - `GET /churnrate/{risk_level}`
  - Retrieves a churn rate record by risk level.
  - Swagger UI: [Get Churn Rate](http://127.0.0.1:8000/docs#/default/get_churnrate_churnrate__risk_level__get)

- **Delete a Churn Rate Record**
  - `DELETE /churnrate/{risk_level}`
  - Deletes a churn rate record by risk level.
  - Swagger UI: [Delete Churn Rate](http://127.0.0.1:8000/docs#/default/delete_churnrate_churnrate__risk_level__delete)

- **Update a Churn Rate Record**
  - `PATCH /churnrate/{risk_level}`
  - Updates an existing churn rate record.
  - Swagger UI: [Update Churn Rate](http://127.0.0.1:8000/docs#/default/update_churnrate_churnrate__risk_level__patch)
