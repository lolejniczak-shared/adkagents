import os
from google.cloud import bigquery
import time # Import time for potential delays
from dotenv import load_dotenv

# 1. --- Configuration ---
# Load environment variables from your .env file
load_dotenv()
# --- Configuration ---
# Get BigQuery Project ID and Dataset ID from environment variables
# Ensure these environment variables are set before running the script.
# For example:
# export BIGQUERY_PROJECT_ID="your-gcp-project-id"
# export BIGQUERY_DATASET_ID="your-bigquery-dataset-id"
# export BIGQUERY_REGION="us-central1" # Add your desired region for Vertex AI connection

BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
BIGQUERY_DATASET_ID = os.getenv("BIGQUERY_DATASET_ID")
BIGQUERY_REGION = os.getenv("BIGQUERY_REGION", "us-central1") # Default to us-central1 if not set
BIGQUERY_CONNECTION_NAME=os.getenv("BIGQUERY_CONNECTION_NAME")
BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME=os.getenv("BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME")

if not BIGQUERY_PROJECT_ID:
    raise ValueError("Environment variable BIGQUERY_PROJECT_ID is not set.")
if not BIGQUERY_DATASET_ID:
    raise ValueError("Environment variable BIGQUERY_DATASET_ID is not set.")

# Construct the dataset ID
DATASET_ID = f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}"
DATASET_REF = f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}"

# Initialize the BigQuery client
client = bigquery.Client(project=BIGQUERY_PROJECT_ID, location=BIGQUERY_REGION)

# --- Utility Function to Execute Queries ---
def execute_bigquery_query(client, query, query_name=""):
    """Executes a SQL query in BigQuery."""
    print(f"\n--- Executing {query_name} ---")
    try:
        query_job = client.query(query)
        # Wait for the job to complete
        query_job.result()
        print(f"{query_name} completed successfully.")
        if query_job.num_dml_affected_rows:
            print(f"Affected rows: {query_job.num_dml_affected_rows}")

    except Exception as e:
        print(f"Error executing {query_name}: {e}")
        print(f"Failed Query:\n{query}")
        raise # Re-raise the exception to stop script if critical step fails


# --- Table Definitions ---

def create_orders_table():
    """Creates the 'orders' table in BigQuery."""
    table_id = f"{DATASET_ID}.orders"
    print(f"Attempting to create table: {table_id}")

    schema = [
        bigquery.SchemaField("order_id", "STRING", mode="REQUIRED",
                             description="Unique identifier for the order."),
        bigquery.SchemaField("customer_email", "STRING", mode="REQUIRED",
                             description="Customer's email address."),
        bigquery.SchemaField("order_date", "TIMESTAMP", mode="REQUIRED",
                             description="Date and time the order was placed."),
        bigquery.SchemaField("total_amount", "FLOAT64", mode="REQUIRED",
                             description="Total amount of the order."),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED",
                             description="Current status of the order (e.g., 'pending', 'completed', 'cancelled')."),
    ]

    # Define clustering fields
    clustering_fields = ["customer_email", "order_date"]

    table = bigquery.Table(table_id, schema=schema)
    table.clustering_fields = clustering_fields
    table.description = "Stores information about customer orders."

    try:
        table = client.create_table(table, exists_ok=True)
        print(f"Table '{table.table_id}' successfully created or already exists.")
    except Exception as e:
        print(f"Error creating table '{table_id}': {e}")
        raise

def create_products_table():
    """Creates the 'products' table in BigQuery."""
    table_id = f"{DATASET_ID}.products"
    print(f"Attempting to create table: {table_id}")

    schema = [
        bigquery.SchemaField("product_id", "STRING", mode="REQUIRED",
                             description="Unique identifier for the product."),
        bigquery.SchemaField("product_name", "STRING", mode="REQUIRED",
                             description="Name of the product (should be unique for application logic)."),
        bigquery.SchemaField("description", "STRING",
                             description="Detailed description of the product."),
        bigquery.SchemaField("price", "FLOAT64", mode="REQUIRED",
                             description="Price of the product."),
        bigquery.SchemaField("stock_quantity", "INT64", mode="REQUIRED",
                             description="Current stock quantity."),
        bigquery.SchemaField("embedding", "FLOAT", mode="REPEATED",
                             description="Vector embedding for semantic search (e.g., 768 dimensions for Google Multilingual Embedding Model 002)."),
    ]

    # Define clustering fields
    clustering_fields = ["product_name"]

    table = bigquery.Table(table_id, schema=schema)
    table.clustering_fields = clustering_fields
    table.description = "Stores information about products, including their embeddings."

    try:
        table = client.create_table(table, exists_ok=True)
        print(f"Table '{table.table_id}' successfully created or already exists.")
    except Exception as e:
        print(f"Error creating table '{table_id}': {e}")
        raise

def create_order_products_table():
    """Creates the 'order_products' table (junction table) in BigQuery."""
    table_id = f"{DATASET_ID}.order_products"
    print(f"Attempting to create table: {table_id}")

    schema = [
        bigquery.SchemaField("order_product_id", "STRING", mode="REQUIRED",
                             description="Unique identifier for the order product entry."),
        bigquery.SchemaField("order_id", "STRING", mode="REQUIRED",
                             description="ID of the associated order."),
        bigquery.SchemaField("product_id", "STRING", mode="REQUIRED",
                             description="ID of the associated product."),
        bigquery.SchemaField("quantity", "INT64", mode="REQUIRED",
                             description="Quantity of the product in the order."),
        bigquery.SchemaField("unit_price", "FLOAT64", mode="REQUIRED",
                             description="Unit price of the product at the time of order."),
    ]

    # Define clustering fields
    clustering_fields = ["order_id", "product_id"]

    table = bigquery.Table(table_id, schema=schema)
    table.clustering_fields = clustering_fields
    table.description = "Junction table linking orders to products and specifying quantities."

    try:
        table = client.create_table(table, exists_ok=True)
        print(f"Table '{table.table_id}' successfully created or already exists.")
    except Exception as e:
        print(f"Error creating table '{table_id}': {e}")
        raise

def create_vertex_ai_embeddings_model():
    """
    Creates a BigQuery ML connection to Vertex AI and registers the embedding model.
    """
    connection_id = "vertex_ai_embedding_conn"
    full_connection_id = f"{BIGQUERY_REGION}.{BIGQUERY_CONNECTION_NAME}"
    remote_model_name = f"{BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME}"
    full_remote_model_id = f"{DATASET_REF}.{remote_model_name}"


    # SQL for creating a BigQuery ML remote model pointing to the Vertex AI embedding model
    # This model uses the connection created above.
    CREATE_REMOTE_EMBEDDING_MODEL_SQL = f"""
    CREATE OR REPLACE MODEL `{full_remote_model_id}`
    REMOTE WITH CONNECTION `{full_connection_id}`
    OPTIONS(
        endpoint = 'text-multilingual-embedding-002'
    );
    """
    print(CREATE_REMOTE_EMBEDDING_MODEL_SQL)
    execute_bigquery_query(client, CREATE_REMOTE_EMBEDDING_MODEL_SQL, "Remote Embedding Model Registration")

# --- Main script execution ---
def main():
    """Main function to create all BigQuery tables, connection, and model."""
    print("Starting BigQuery setup script...")

    # Create tables first
    create_orders_table()
    create_products_table()
    create_order_products_table()

    # Create Vertex AI connection and register embedding model
    create_vertex_ai_embeddings_model()

    print("\nBigQuery setup script completed.")


if __name__ == "__main__":
    main()