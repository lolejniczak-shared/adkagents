-- Sample Data Generation for E-commerce System (Using embedding() function for Google Multilingual Embedding Model 002)

-- Insert 30 Sample Products
-- Each embedding is generated directly from the description using the hypothetical embedding() function.
INSERT INTO products (product_name, description, price, stock_quantity, embedding) VALUES
('Laptop Pro X', 'Powerful laptop with 16GB RAM and 1TB SSD. Ideal for demanding tasks and creative professionals.', 1200.00, 50, embedding('text-multilingual-embedding-002', 'Powerful laptop with 16GB RAM and 1TB SSD. Ideal for demanding tasks and creative professionals.')),
('Mechanical Keyboard Elite', 'Tactile switches, customizable RGB backlight, and durable aluminum design for peak gaming and typing performance.', 85.50, 120, embedding('text-multilingual-embedding-002', 'Tactile switches, customizable RGB backlight, and durable aluminum design for peak gaming and typing performance.')),
('Wireless Mouse Ergo', 'Ergonomic design for comfortable long-term use, precise tracking, and silent clicks. Perfect for office work.', 35.99, 200, embedding('text-multilingual-embedding-002', 'Ergonomic design for comfortable long-term use, precise tracking, and silent clicks. Perfect for office work.')),
('4K Monitor Ultra', '27-inch IPS panel with vibrant colors, high refresh rate, and HDR support for stunning visuals.', 350.00, 75, embedding('text-multilingual-embedding-002', '27-inch IPS panel with vibrant colors, high refresh rate, and HDR support for stunning visuals.')),
('Webcam HD 1080p', 'High-definition video for clear calls and streaming, with auto-focus and low-light correction.', 49.00, 150, embedding('text-multilingual-embedding-002', 'High-definition video for clear calls and streaming, with auto-focus and low-light correction.')),
('Noise-Cancelling Headphones', 'Immersive audio experience with active noise cancellation, comfortable earcups, and long battery life for travel and focus.', 199.99, 90, embedding('text-multilingual-embedding-002', 'Immersive audio experience with active noise cancellation, comfortable earcups, and long battery life for travel and focus.')),
('USB-C Hub Pro', 'Multi-port adapter for modern laptops, including HDMI, USB 3.0, and SD card readers. Expand your connectivity.', 29.95, 300, embedding('text-multilingual-embedding-002', 'Multi-port adapter for modern laptops, including HDMI, USB 3.0, and SD card readers. Expand your connectivity.')),
('External SSD 1TB', 'Fast and portable storage solution with USB 3.2 Gen 2 interface, perfect for large files and backups.', 99.00, 100, embedding('text-multilingual-embedding-002', 'Fast and portable storage solution with USB 3.2 Gen 2 interface, perfect for large files and backups.')),
('Gaming Headset RGB', 'Surround sound headset with customizable RGB lighting, clear microphone, and comfortable ear cushions for extended gaming sessions.', 75.00, 80, embedding('text-multilingual-embedding-002', 'Surround sound headset with customizable RGB lighting, clear microphone, and comfortable ear cushions for extended gaming sessions.')),
('Smartwatch Fit X', 'Fitness tracking, heart rate monitor, sleep analysis, and notifications. Stay active and connected on the go.', 120.00, 110, embedding('text-multilingual-embedding-002', 'Fitness tracking, heart rate monitor, sleep analysis, and notifications. Stay active and connected on the go.')),
('Smart Home Speaker', 'Voice-controlled assistant with premium audio quality, compatible with various smart home devices.', 89.99, 130, embedding('text-multilingual-embedding-002', 'Voice-controlled assistant with premium audio quality, compatible with various smart home devices.')),
('Robot Vacuum Cleaner', 'Automated cleaning with smart mapping, multi-floor support, and powerful suction for pet hair.', 299.00, 60, embedding('text-multilingual-embedding-002', 'Automated cleaning with smart mapping, multi-floor support, and powerful suction for pet hair.')),
('Espresso Machine Auto', 'Bean-to-cup espresso maker with integrated grinder and automatic milk frother for barista-quality drinks.', 450.00, 40, embedding('text-multilingual-embedding-002', 'Bean-to-cup espresso maker with integrated grinder and automatic milk frother for barista-quality drinks.')),
('Air Fryer XL', 'Healthy cooking with large capacity, digital touchscreen, and pre-set programs for a variety of dishes.', 110.00, 100, embedding('text-multilingual-embedding-002', 'Healthy cooking with large capacity, digital touchscreen, and pre-set programs for a variety of dishes.')),
('Blender High Power', 'Crushes ice and blends smoothies with ease, featuring multiple speed settings and a durable glass jar.', 65.00, 180, embedding('text-multilingual-embedding-002', 'Crushes ice and blends smoothies with ease, featuring multiple speed settings and a durable glass jar.')),
('Electric Toothbrush Sonic', 'Advanced sonic cleaning for healthier gums and brighter teeth, with multiple brushing modes and pressure sensor.', 55.00, 250, embedding('text-multilingual-embedding-002', 'Advanced sonic cleaning for healthier gums and brighter teeth, with multiple brushing modes and pressure sensor.')),
('Smart LED Light Bulbs', 'Control lighting from your phone, dimmable, and color-changing. Create the perfect ambiance for any occasion.', 25.00, 500, embedding('text-multilingual-embedding-002', 'Control lighting from your phone, dimmable, and color-changing. Create the perfect ambiance for any occasion.')),
('Portable Projector Mini', 'Compact projector for movies and presentations on the go, with built-in speaker and HDMI input.', 150.00, 70, embedding('text-multilingual-embedding-002', 'Compact projector for movies and presentations on the go, with built-in speaker and HDMI input.')),
('Action Camera 4K', 'Capture your adventures in stunning 4K, waterproof, with image stabilization and wide-angle lens.', 180.00, 90, embedding('text-multilingual-embedding-002', 'Capture your adventures in stunning 4K, waterproof, with image stabilization and wide-angle lens.')),
('Drone Explorer', 'Easy-to-fly drone with HD camera, long battery life, and GPS precise hovering for aerial photography.', 320.00, 30, embedding('text-multilingual-embedding-002', 'Easy-to-fly drone with HD camera, long battery life, and GPS precise hovering for aerial photography.')),
('Digital Drawing Tablet', 'Professional tablet for artists and designers, with high-resolution active area and pressure-sensitive pen.', 220.00, 60, embedding('text-multilingual-embedding-002', 'Professional tablet for artists and designers, with high-resolution active area and pressure-sensitive pen.')),
('Home Security Camera', 'Wireless camera with motion detection, night vision, and two-way audio for comprehensive home monitoring.', 95.00, 140, embedding('text-multilingual-embedding-002', 'Wireless camera with motion detection, night vision, and two-way audio for comprehensive home monitoring.')),
('Portable Bluetooth Speaker', 'Compact speaker with powerful sound, long-lasting battery, and waterproof design for outdoor adventures.', 40.00, 220, embedding('text-multilingual-embedding-002', 'Compact speaker with powerful sound, long-lasting battery, and waterproof design for outdoor adventures.')),
('E-Reader Oasis', 'Glare-free screen, long battery life, waterproof, and adjustable warm light for comfortable reading day and night.', 115.00, 90, embedding('text-multilingual-embedding-002', 'Glare-free screen, long battery life, waterproof, and adjustable warm light for comfortable reading day and night.')),
('Desk Lamp LED Smart', 'Adjustable brightness and color temperature, app controlled, with a sleek modern design for your workspace.', 45.00, 170, embedding('text-multilingual-embedding-002', 'Adjustable brightness and color temperature, app controlled, with a sleek modern design for your workspace.')),
('Fitness Tracker HR', 'Monitors heart rate, steps, sleep, and calories burned. Helps you achieve your fitness goals.', 70.00, 160, embedding('text-multilingual-embedding-002', 'Monitors heart rate, steps, sleep, and calories burned. Helps you achieve your fitness goals.')),
('VR Headset Pro', 'Immersive virtual reality experience with high-resolution display, wide field of view, and precise motion tracking.', 499.00, 25, embedding('text-multilingual-embedding-002', 'Immersive virtual reality experience with high-resolution display, wide field of view, and precise motion tracking.')),
('Wireless Charging Pad', 'Fast wireless charging for compatible devices, slim design, and LED indicator. Declutter your desk.', 20.00, 350, embedding('text-multilingual-embedding-002', 'Fast wireless charging for compatible devices, slim design, and LED indicator. Declutter your desk.')),
('Smart Plug Mini', 'Control any appliance from your smartphone, set schedules, and monitor energy usage. Make your home smarter.', 15.00, 400, embedding('text-multilingual-embedding-002', 'Control any appliance from your smartphone, set schedules, and monitor energy usage. Make your home smarter.')),
('Portable Power Bank', 'High capacity power bank for on-the-go charging of smartphones and tablets. Never run out of battery.', 30.00, 280, embedding('text-multilingual-embedding-002', 'High capacity power bank for on-the-go charging of smartphones and tablets. Never run out of battery.'));


-- Insert 30 Sample Orders
INSERT INTO orders (customer_email, order_date, total_amount, status) VALUES
('alice.smith@example.com', '2024-01-15 10:00:00', 1235.99, 'completed'),
('bob.johnson@example.com', '2024-01-20 11:30:00', 85.50, 'pending'),
('charlie.brown@example.com', '2024-02-01 14:15:00', 350.00, 'shipped'),
('diana.prince@example.com', '2024-02-10 09:45:00', 49.00, 'completed'),
('eve.adams@example.com', '2024-02-15 16:00:00', 2000.00, 'pending'), -- Multi-item order placeholder
('frank.white@example.com', '2024-03-01 10:20:00', 29.95, 'shipped'),
('grace.taylor@example.com', '2024-03-05 13:00:00', 99.00, 'completed'),
('henry.green@example.com', '2024-03-12 17:00:00', 75.00, 'pending'),
('ivy.king@example.com', '2024-03-20 08:00:00', 120.00, 'completed'),
('jack.lee@example.com', '2024-04-01 11:00:00', 89.99, 'shipped'),
('karen.miller@example.com', '2024-04-05 14:00:00', 299.00, 'completed'),
('liam.thomas@example.com', '2024-04-10 16:30:00', 450.00, 'pending'),
('mia.jackson@example.com', '2024-04-15 09:00:00', 110.00, 'shipped'),
('noah.white@example.com', '2024-04-20 12:00:00', 65.00, 'completed'),
('olivia.harris@example.com', '2024-05-01 10:10:00', 55.00, 'pending'),
('peter.clark@example.com', '2024-05-05 15:00:00', 25.00, 'shipped'),
('quinn.lewis@example.com', '2024-05-10 11:00:00', 150.00, 'completed'),
('rachel.scott@example.com', '2024-05-15 13:00:00', 180.00, 'pending'),
('sam.young@example.com', '2024-05-20 17:00:00', 320.00, 'shipped'),
('tina.hall@example.com', '2024-05-25 08:30:00', 220.00, 'completed'),
('alice.smith@example.com', '2024-06-01 09:00:00', 35.99, 'pending'),
('bob.johnson@example.com', '2024-06-05 10:00:00', 199.99, 'shipped'),
('charlie.brown@example.com', '2024-06-10 11:00:00', 99.00, 'completed'),
('diana.prince@example.com', '2024-06-15 12:00:00', 75.00, 'pending'),
('eve.adams@example.com', '2024-06-20 13:00:00', 120.00, 'shipped'),
('frank.white@example.com', '2024-06-25 14:00:00', 89.99, 'completed'),
('grace.taylor@example.com', '2024-07-01 15:00:00', 299.00, 'pending'),
('henry.green@example.com', '2024-07-05 16:00:00', 450.00, 'shipped'),
('ivy.king@example.com', '2024-07-10 17:00:00', 110.00, 'completed'),
('jack.lee@example.com', '2024-07-15 18:00:00', 65.00, 'pending');

-- Insert 30 Sample Order Products
DO $$
DECLARE
    r_order RECORD;
    r_product RECORD;
    i INT := 0;
BEGIN
    FOR r_order IN (SELECT order_id FROM orders ORDER BY RANDOM() LIMIT 30)
    LOOP
        -- Each order gets at least one product
        FOR r_product IN (SELECT product_id, price FROM products ORDER BY RANDOM() LIMIT (FLOOR(RANDOM() * 3) + 1)) -- 1 to 3 products per order
        LOOP
            INSERT INTO order_products (order_id, product_id, quantity, unit_price)
            VALUES (r_order.order_id, r_product.product_id, FLOOR(RANDOM() * 3) + 1, r_product.price); -- Quantity 1-3
        END LOOP;
        i := i + 1;
        IF i >= 30 THEN
            EXIT;
        END IF;
    END LOOP;
END $$;

-- Optional: Update total_amount for existing orders based on inserted order_products
-- This ensures total_amount is accurate after populating order_products
UPDATE orders o
SET total_amount = (
    SELECT SUM(op.quantity * op.unit_price)
    FROM order_products op
    WHERE op.order_id = o.order_id
)
WHERE EXISTS (SELECT 1 FROM order_products op WHERE op.order_id = o.order_id);

-- End of Sample Data Script