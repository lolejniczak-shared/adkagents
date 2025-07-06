-- Deploy AlloyDB E-commerce Data Model (Updated for Google Multilingual Embedding Model 002)

-- Enable the pgvector extension if not already enabled
-- You might need superuser privileges for this.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS google_ml_integration;

-- Table: orders
CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_email VARCHAR(255) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending'
);

-- Indexes for orders table
CREATE INDEX IF NOT EXISTS idx_orders_customer_email ON orders (customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders (order_date);

-- Table: products
CREATE TABLE IF NOT EXISTS products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    embedding VECTOR(768) --  dimensionality to 768 for Google Multilingual Embedding Model 002
);

-- Indexes for products table
CREATE UNIQUE INDEX IF NOT EXISTS idx_products_product_name ON products (product_name);
-- HNSW index for efficient semantic search on embedding. Adjust m and ef_construction as needed.
-- Make sure you have the HNSW index type available for pgvector.
CREATE INDEX IF NOT EXISTS idx_products_embedding ON products USING HNSW (embedding vector_cosine_ops) WITH (m=16, ef_construction=64);


-- Table: order_products (Junction Table)
CREATE TABLE IF NOT EXISTS order_products (
    order_product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    CONSTRAINT unique_order_product UNIQUE (order_id, product_id) -- Ensures a product appears only once per order
);

-- Indexes for order_products table
CREATE INDEX IF NOT EXISTS idx_order_products_order_id ON order_products (order_id);
CREATE INDEX IF NOT EXISTS idx_order_products_product_id ON order_products (product_id);

-- End of Deployment Script