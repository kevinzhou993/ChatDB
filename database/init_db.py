import sqlite3
import pandas as pd

# connect
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# -----------------------
# Create tables
# -----------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT,
    state TEXT,
    signup_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category_id INTEGER,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL
)
""")

conn.commit()

# -----------------------
# Load CSV
# -----------------------

def load_csv(table, file):
    df = pd.read_csv(file)
    df.to_sql(table, conn, if_exists='append', index=False)

load_csv("customers", "customers.csv")
load_csv("categories", "categories.csv")
load_csv("products", "products.csv")
load_csv("orders", "orders.csv")
load_csv("order_items", "order_items.csv")

conn.close()

print("✅ Database created successfully!")