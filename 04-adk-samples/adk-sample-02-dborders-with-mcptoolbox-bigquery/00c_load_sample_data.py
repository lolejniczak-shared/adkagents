import os
from google.cloud import bigquery
import time # Import time for potential delays
from dotenv import load_dotenv

# 1. --- Configuration ---
# Load environment variables from your .env file
load_dotenv()

BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
BIGQUERY_DATASET_ID = os.getenv("BIGQUERY_DATASET_ID")
BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME = os.getenv("BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME")

if not BIGQUERY_PROJECT_ID:
    raise ValueError("Environment variable BIGQUERY_PROJECT_ID is not set.")
if not BIGQUERY_DATASET_ID:
    raise ValueError("Environment variable BIGQUERY_DATASET_ID is not set.")

# Construct the full table and model references
PRODUCTS_TABLE = f"`{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}.products`"
ORDERS_TABLE = f"`{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}.orders`"
ORDER_PRODUCTS_TABLE = f"`{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}.order_products`"
REMOTE_EMBEDDING_MODEL = f"`{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_EMBEDDING_MODEL_OBJECT_NAME}`"

# Initialize the BigQuery client
client = bigquery.Client(project=BIGQUERY_PROJECT_ID)

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

# --- SQL Query for Product Data Insertion ---
# This SQL uses the ML.GENERATE_EMBEDDING function with the previously registered
# remote model. Ensure the connection exists and has 'Vertex AI User' role.
INSERT_PRODUCTS_SQL = f"""
INSERT INTO {PRODUCTS_TABLE} (
    product_id,
    product_name,
    description,
    price,
    stock_quantity
    ##embedding
)
SELECT
    GENERATE_UUID() AS product_id,
    data.product_name,
    data.description,
    data.price,
    data.stock_quantity
    ##ml_output.embeddings AS embedding
FROM
    UNNEST([
        STRUCT('Laptop Pro X' AS product_name, 'Powerful laptop with 16GB RAM and 1TB SSD. Ideal for demanding tasks and creative professionals.' AS description, 1200.00 AS price, 50 AS stock_quantity),
        STRUCT('Mechanical Keyboard Elite', 'Tactile switches, customizable RGB backlight, and durable aluminum design for peak gaming and typing performance.', 85.50, 120),
        STRUCT('Wireless Mouse Ergo', 'Ergonomic design for comfortable long-term use, precise tracking, and silent clicks. Perfect for office work.', 35.99, 200),
        STRUCT('4K Monitor Ultra', '27-inch IPS panel with vibrant colors, high refresh rate, and HDR support for stunning visuals.', 350.00, 75),
        STRUCT('Webcam HD 1080p', 'High-definition video for clear calls and streaming, with auto-focus and low-light correction.', 49.00, 150),
        STRUCT('Noise-Cancelling Headphones', 'Immersive audio experience with active noise cancellation, comfortable earcups, and long battery life for travel and focus.', 199.99, 90),
        STRUCT('USB-C Hub Pro', 'Multi-port adapter for modern laptops, including HDMI, USB 3.0, and SD card readers. Expand your connectivity.', 29.95, 300),
        STRUCT('External SSD 1TB', 'Fast and portable storage solution with USB 3.2 Gen 2 interface, perfect for large files and backups.', 99.00, 100),
        STRUCT('Gaming Headset RGB', 'Surround sound headset with customizable RGB lighting, clear microphone, and comfortable ear cushions for extended gaming sessions.', 75.00, 80),
        STRUCT('Smartwatch Fit X', 'Fitness tracking, heart rate monitor, sleep analysis, and notifications. Stay active and connected on the go.', 120.00, 110),
        STRUCT('Smart Home Speaker', 'Voice-controlled assistant with premium audio quality, compatible with various smart home devices.', 89.99, 130),
        STRUCT('Robot Vacuum Cleaner', 'Automated cleaning with smart mapping, multi-floor support, and powerful suction for pet hair.', 299.00, 60),
        STRUCT('Espresso Machine Auto', 'Bean-to-cup espresso maker with integrated grinder and automatic milk frother for barista-quality drinks.', 450.00, 40),
        STRUCT('Air Fryer XL', 'Healthy cooking with large capacity, digital touchscreen, and pre-set programs for a variety of dishes.', 110.00, 100),
        STRUCT('Blender High Power', 'Crushes ice and blends smoothies with ease, featuring multiple speed settings and a durable glass jar.', 65.00, 180),
        STRUCT('Electric Toothbrush Sonic', 'Advanced sonic cleaning for healthier gums and brighter teeth, with multiple brushing modes and pressure sensor.', 55.00, 250),
        STRUCT('Smart LED Light Bulbs', 'Control lighting from your phone, dimmable, and color-changing. Create the perfect ambiance for any occasion.', 25.00, 500),
        STRUCT('Portable Projector Mini', 'Compact projector for movies and presentations on the go, with built-in speaker and HDMI input.', 150.00, 70),
        STRUCT('Action Camera 4K', 'Capture your adventures in stunning 4K, waterproof, with image stabilization and wide-angle lens.', 180.00, 90),
        STRUCT('Drone Explorer', 'Easy-to-fly drone with HD camera, long battery life, and GPS precise hovering for aerial photography.', 320.00, 30),
        STRUCT('Digital Drawing Tablet', 'Professional tablet for artists and designers, with high-resolution active area and pressure-sensitive pen.', 220.00, 60),
        STRUCT('Home Security Camera', 'Wireless camera with motion detection, night vision, and two-way audio for comprehensive home monitoring.', 95.00, 140),
        STRUCT('Portable Bluetooth Speaker', 'Compact speaker with powerful sound, long-lasting battery, and waterproof design for outdoor adventures.', 40.00, 220),
        STRUCT('E-Reader Oasis', 'Glare-free screen, long battery life, waterproof, and adjustable warm light for comfortable reading day and night.', 115.00, 90),
        STRUCT('Desk Lamp LED Smart', 'Adjustable brightness and color temperature, app controlled, with a sleek modern design for your workspace.', 45.00, 170),
        STRUCT('Fitness Tracker HR', 'Monitors heart rate, steps, sleep, and calories burned. Helps you achieve your fitness goals.', 70.00, 160),
        STRUCT('VR Headset Pro', 'Immersive virtual reality experience with high-resolution display, wide field of view, and precise motion tracking.', 499.00, 25),
        STRUCT('Wireless Charging Pad', 'Fast wireless charging for compatible devices, slim design, and LED indicator. Declutter your desk.', 20.00, 350),
        STRUCT('Smart Plug Mini', 'Control any appliance from your smartphone, set schedules, and monitor energy usage. Make your home smarter.', 15.00, 400),
        STRUCT('Portable Power Bank', 'High capacity power bank for on-the-go charging of smartphones and tablets. Never run out of battery.', 30.00, 280)
    ]) AS data
"""

print(INSERT_PRODUCTS_SQL)

# --- SQL Query for Order Data Insertion ---
INSERT_ORDERS_SQL = f"""
INSERT INTO {ORDERS_TABLE} (
    order_id,
    customer_email,
    order_date,
    total_amount, -- total_amount will be updated later based on order_products
    status
)
VALUES
(GENERATE_UUID(), 'alice.smith@example.com', '2024-01-15 10:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'bob.johnson@example.com', '2024-01-20 11:30:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'charlie.brown@example.com', '2024-02-01 14:15:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'diana.prince@example.com', '2024-02-10 09:45:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'eve.adams@example.com', '2024-02-15 16:00:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'frank.white@example.com', '2024-03-01 10:20:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'grace.taylor@example.com', '2024-03-05 13:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'henry.green@example.com', '2024-03-12 17:00:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'ivy.king@example.com', '2024-03-20 08:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'jack.lee@example.com', '2024-04-01 11:00:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'karen.miller@example.com', '2024-04-05 14:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'liam.thomas@example.com', '2024-04-10 16:30:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'mia.jackson@example.com', '2024-04-15 09:00:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'noah.white@example.com', '2024-04-20 12:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'olivia.harris@example.com', '2024-05-01 10:10:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'peter.clark@example.com', '2024-05-05 15:00:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'quinn.lewis@example.com', '2024-05-10 11:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'rachel.scott@example.com', '2024-05-15 13:00:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'sam.young@example.com', '2024-05-20 17:00:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'tina.hall@example.com', '2024-05-25 08:30:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'alice.smith@example.com', '2024-06-01 09:00:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'bob.johnson@example.com', '2024-06-05 10:00:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'charlie.brown@example.com', '2024-06-10 11:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'diana.prince@example.com', '2024-06-15 12:00:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'eve.adams@example.com', '2024-06-20 13:00:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'frank.white@example.com', '2024-06-25 14:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'grace.taylor@example.com', '2024-07-01 15:00:00 UTC', 0.00, 'pending'),
(GENERATE_UUID(), 'henry.green@example.com', '2024-07-05 16:00:00 UTC', 0.00, 'shipped'),
(GENERATE_UUID(), 'ivy.king@example.com', '2024-07-10 17:00:00 UTC', 0.00, 'completed'),
(GENERATE_UUID(), 'jack.lee@example.com', '2024-07-15 18:00:00 UTC', 0.00, 'pending');
"""

# --- SQL Query for Order Products Data Insertion ---
INSERT_ORDER_PRODUCTS_SQL = f"""
INSERT INTO {ORDER_PRODUCTS_TABLE} (
    order_product_id,
    order_id,
    product_id,
    quantity,
    unit_price
)
SELECT
    GENERATE_UUID() AS order_product_id,
    o.order_id,
    p.product_id,
    -- Simulate random quantity (1 to 3) using MOD() and a sequence number
    MOD(ABS(FARM_FINGERPRINT(CONCAT(o.order_id, p.product_id, CAST(seq AS STRING)))), 3) + 1 AS quantity,
    p.price AS unit_price
FROM
    {ORDERS_TABLE} AS o
    -- Select a limited number of products to cross join for variety,
    -- and use a sequence to create multiple entries per order/product combination
    CROSS JOIN (SELECT product_id, price FROM {PRODUCTS_TABLE} LIMIT 10) AS p
    CROSS JOIN UNNEST(GENERATE_ARRAY(1, 3)) AS seq -- Generates 1 to 3 "slots" for products per order
WHERE
    MOD(ABS(FARM_FINGERPRINT(CONCAT(o.order_id, p.product_id, CAST(seq AS STRING)))), 5) < 3 -- Adjust this to control how many products each order gets
QUALIFY
    ROW_NUMBER() OVER (PARTITION BY o.order_id ORDER BY ABS(FARM_FINGERPRINT(p.product_id))) <= 3 -- Limit to max 3 products per order
LIMIT 100; -- Limit overall inserts to avoid too much data for testing
"""

# --- SQL Query for Updating Order Total Amounts ---
UPDATE_ORDER_TOTALS_SQL = f"""
UPDATE {ORDERS_TABLE} AS o
SET
    total_amount = (
        SELECT SUM(op.quantity * op.unit_price)
        FROM {ORDER_PRODUCTS_TABLE} AS op
        WHERE op.order_id = o.order_id
    )
WHERE
    EXISTS (SELECT 1 FROM {ORDER_PRODUCTS_TABLE} AS op WHERE op.order_id = o.order_id);
"""





UPDATE_PRODUCT_EMBEDDINGS_SQL = f"""
UPDATE {PRODUCTS_TABLE} AS o
SET
    embedding = (
     SELECT op.ml_generate_embedding_result FROM ML.GENERATE_EMBEDDING(
     MODEL {REMOTE_EMBEDDING_MODEL}, 
     (SELECT description as content, product_id FROM {PRODUCTS_TABLE})
     ) AS op
     WHERE op.product_id = o.product_id
    ) WHERE
    EXISTS (SELECT 1 FROM {PRODUCTS_TABLE} AS op WHERE op.product_id = o.product_id);
"""


print(UPDATE_PRODUCT_EMBEDDINGS_SQL)

# --- Main script execution ---
def main():
    """Main function to insert sample data into BigQuery tables."""
    print("Starting BigQuery sample data insertion script...")

    # Execute product insertion first, as order_products depends on products
    execute_bigquery_query(client, INSERT_PRODUCTS_SQL, "Product Data Insertion")
    # Add a small delay if needed, though BigQuery jobs are asynchronous and client.query().result() waits
    time.sleep(2) # Give a moment before inserting orders

    # Execute order insertion
    execute_bigquery_query(client, INSERT_ORDERS_SQL, "Order Data Insertion")
    time.sleep(2) # Give a moment before inserting order_products

    # Execute order_product insertion
    execute_bigquery_query(client, INSERT_ORDER_PRODUCTS_SQL, "Order Product Data Insertion")
    time.sleep(5) # Give more time as this might be more complex

    # Execute update for order total amounts
    execute_bigquery_query(client, UPDATE_ORDER_TOTALS_SQL, "Update Order Total Amounts")
    execute_bigquery_query(client, UPDATE_PRODUCT_EMBEDDINGS_SQL, "Update product embeddings")
    print("\nBigQuery sample data insertion script completed.")


if __name__ == "__main__":
    main()