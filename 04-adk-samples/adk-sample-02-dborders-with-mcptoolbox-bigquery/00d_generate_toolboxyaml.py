import os
from dotenv import load_dotenv

# 1. --- Configuration ---
# Load environment variables from your .env file
load_dotenv()

BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
BIGQUERY_DATASET_ID = os.getenv("BIGQUERY_DATASET_ID")
BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME = os.getenv("BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME")
BIGQUERY_REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "US") # Default to US if not set

if not BIGQUERY_PROJECT_ID:
    raise ValueError("Environment variable BIGQUERY_PROJECT_ID is not set.")
if not BIGQUERY_DATASET_ID:
    raise ValueError("Environment variable BIGQUERY_DATASET_ID is not set.")
if not BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME:
    raise ValueError("Environment variable BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME is not set.")

# Construct the full dataset and model references for use in SQL
FULL_DATASET_PATH = f"`{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}`"
FULL_MODEL_PATH = f"`{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME}`"


# --- YAML Content Template ---
# Using f-strings to inject environment variable values directly into the YAML string
TOOLBOX_YAML_CONTENT = f"""
sources:
  bigquery-ecommerce:
    kind: "bigquery"
    project: "{BIGQUERY_PROJECT_ID}"
tools:
  get-order-by-id:
    kind: bigquery-sql
    source: bigquery-ecommerce
    description: Retrieve details of a specific order by its unique order ID, including all purchased products.
    parameters:
      - name: order_id
        type: string
        description: The unique identifier (STRING) of the order.
    statement: |
      SELECT
          o.order_id,
          o.customer_email,
          o.order_date,
          o.total_amount,
          o.status,
          TO_JSON_STRING(ARRAY_AGG(STRUCT(
              p.product_id,
              p.product_name,
              p.description,
              op.unit_price,
              op.quantity
          ))) AS products
      FROM
          {FULL_DATASET_PATH}.orders AS o
      JOIN
          {FULL_DATASET_PATH}.order_products AS op ON o.order_id = op.order_id
      JOIN
          {FULL_DATASET_PATH}.products AS p ON op.product_id = p.product_id
      WHERE
          o.order_id = @order_id
      GROUP BY
          o.order_id, o.customer_email, o.order_date, o.total_amount, o.status;
  list-orders-by-customer-email:
    kind: bigquery-sql
    source: bigquery-ecommerce
    description: List all orders placed by a specific customer, identified by their email address.
    parameters:
      - name: customer_email
        type: string
        description: The email address of the customer.
    statement: |
      SELECT
          o.order_id,
          o.customer_email,
          o.order_date,
          o.total_amount,
          o.status,
          TO_JSON_STRING(ARRAY_AGG(STRUCT(
              p.product_id,
              p.product_name,
              p.description,
              op.unit_price,
              op.quantity
          ))) AS products
      FROM
          {FULL_DATASET_PATH}.orders AS o
      JOIN
          {FULL_DATASET_PATH}.order_products AS op ON o.order_id = op.order_id
      JOIN
          {FULL_DATASET_PATH}.products AS p ON op.product_id = p.product_id
      WHERE
          o.customer_email = @customer_email
      GROUP BY
          o.order_id, o.customer_email, o.order_date, o.total_amount, o.status
      ORDER BY
          o.order_date DESC;
  list-orders-by-email-and-product:
    kind: bigquery-sql
    source: bigquery-ecommerce
    description: Find orders made by a specific customer that include a particular product.
    parameters:
      - name: customer_email
        type: string
        description: The email address of the customer.
      - name: product_name
        type: string
        description: The name of the product purchased (case-insensitive partial match).
    statement: |
      SELECT
          o.order_id,
          o.customer_email,
          o.order_date,
          o.total_amount,
          o.status,
          TO_JSON_STRING(ARRAY_AGG(STRUCT(
              p.product_id,
              p.product_name,
              p.description,
              op.unit_price,
              op.quantity
          ))) AS products
      FROM
          {FULL_DATASET_PATH}.orders AS o
      JOIN
          {FULL_DATASET_PATH}.order_products AS op ON o.order_id = op.order_id
      JOIN
          {FULL_DATASET_PATH}.products AS p ON op.product_id = p.product_id
      WHERE
          o.customer_email = @customer_email AND LOWER(p.product_name) LIKE LOWER(CONCAT('%', @product_name, '%'))
      GROUP BY
          o.order_id, o.customer_email, o.order_date, o.total_amount, o.status
      ORDER BY
          o.order_date DESC;
  find-similar-products:
    kind: bigquery-sql
    source: bigquery-ecommerce
    description: Find products with descriptions semantically similar to a given query string. The query will be automatically converted into an embedding.
    parameters:
      - name: query_text
        type: string
        description: The text description or query for semantic search.
    statement: |
      SELECT
          base.product_id,
          base.product_name,
          base.description,
          base.price,
          base.stock_quantity
        FROM VECTOR_SEARCH(
        (SELECT embedding,
         product_id, 
         product_name, 
         description, 
         price, 
         stock_quantity FROM {FULL_DATASET_PATH}.products), 
        'embedding',
        (
        SELECT ml_generate_embedding_result, content AS query
        FROM ML.GENERATE_EMBEDDING(
            MODEL {FULL_MODEL_PATH},
            (SELECT @query_text AS content)
        )
        ),
        top_k => 10
        );
  find-product-by-name:
    kind: bigquery-sql
    source: bigquery-ecommerce
    description: Search for a product by its name.
    parameters:
      - name: product_name_query
        type: string
        description: The name of the product to search for (case-insensitive partial match).
    statement: |
      SELECT
          product_id,
          product_name,
          description,
          price,
          stock_quantity
      FROM
          {FULL_DATASET_PATH}.products
      WHERE
          LOWER(product_name) LIKE LOWER(CONCAT('%', @product_name_query, '%'));
  create-order-header:
    kind: bigquery-sql
    source: bigquery-ecommerce
    description: Create a new order header. The total_amount is initialized to 0.00 and status to 'pending'. Product details must be added separately using 'add-order-product-item'.
    parameters:
      - name: customer_email
        type: string
        description: The email address of the customer placing the order.
    statement: |
      INSERT INTO {FULL_DATASET_PATH}.orders (order_id, customer_email, total_amount, status, order_date)
      VALUES (GENERATE_UUID(), @customer_email, 0.00, 'pending', CURRENT_TIMESTAMP());
  add-order-product-item:
    kind: bigquery-sql
    source: bigquery-ecommerce
    description: Add a single product item to an existing order. The unit_price should be the product's price at the time of purchase.
    parameters:
      - name: order_id
        type: string
        description: The ID of the existing order to add the product to.
      - name: product_id
        type: string
        description: The ID of the product to add.
      - name: quantity
        type: integer
        description: The quantity of the product. Must be greater than 0.
      - name: unit_price
        type: string
        description: The price of the product at the time of purchase (NUMERIC/BIGNUMERIC equivalent in BigQuery).
    statement: |
      INSERT INTO {FULL_DATASET_PATH}.order_products (order_product_id, order_id, product_id, quantity, unit_price)
      VALUES (GENERATE_UUID(), @order_id, @product_id, @quantity, CAST(@unit_price AS FLOAT64));
toolsets:
   my_first_toolset:
     - get-order-by-id
     - list-orders-by-customer-email
     - list-orders-by-email-and-product
     - find-similar-products
     - find-product-by-name
     - create-order-header
     - add-order-product-item
"""

# --- Main script execution ---
def main():
    """Generates the toolbox.yaml file with environment variable injection."""
    output_filename = "toolbox.yaml"
    try:
        with open(output_filename, "w") as f:
            f.write(TOOLBOX_YAML_CONTENT)
        print(f"Successfully generated {output_filename}")
        print(f"  Project ID: {BIGQUERY_PROJECT_ID}")
        print(f"  Dataset ID: {BIGQUERY_DATASET_ID}")
        print(f"  Embedding Model: {BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME}")
        print(f"  BigQuery Region: {BIGQUERY_REGION}")
    except IOError as e:
        print(f"Error writing to file {output_filename}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()