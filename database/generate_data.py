import pandas as pd
import random
from faker import Faker

fake = Faker()

# -----------------------
# 1. Customers
# -----------------------
customers = []
for i in range(1, 101):
    customers.append({
        "customer_id": i,
        "name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "state": fake.state(),
        "signup_date": fake.date_between(start_date="-2y", end_date="today")
    })

df_customers = pd.DataFrame(customers)

# -----------------------
# 2. Categories
# -----------------------
category_list = ["Electronics", "Clothing", "Home", "Sports", "Books"]

categories = []
for i, cat in enumerate(category_list, start=1):
    categories.append({
        "category_id": i,
        "category_name": cat
    })

df_categories = pd.DataFrame(categories)

# -----------------------
# 3. Products
# -----------------------
products = []
for i in range(1, 201):
    category_id = random.randint(1, len(category_list))
    products.append({
        "product_id": i,
        "product_name": fake.word().capitalize(),
        "category_id": category_id,
        "price": round(random.uniform(5, 500), 2)
    })

df_products = pd.DataFrame(products)

# -----------------------
# 4. Orders
# -----------------------
orders = []
for i in range(1, 501):
    customer_id = random.randint(1, 100)
    orders.append({
        "order_id": i,
        "customer_id": customer_id,
        "order_date": fake.date_between(start_date="-1y", end_date="today"),
        "total_amount": 0,  # will update later
        "status": random.choice(["completed", "pending", "cancelled"])
    })

df_orders = pd.DataFrame(orders)

# -----------------------
# 5. Order Items
# -----------------------
order_items = []
order_totals = {}

order_item_id = 1

for order in orders:
    num_items = random.randint(1, 5)
    total = 0

    for _ in range(num_items):
        product_id = random.randint(1, 200)
        quantity = random.randint(1, 3)

        price = df_products.loc[df_products["product_id"] == product_id, "price"].values[0]
        total += price * quantity

        order_items.append({
            "order_item_id": order_item_id,
            "order_id": order["order_id"],
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": price
        })

        order_item_id += 1

    order_totals[order["order_id"]] = round(total, 2)

# update order totals
df_order_items = pd.DataFrame(order_items)

df_orders["total_amount"] = df_orders["order_id"].map(order_totals)

# -----------------------
# Save CSV
# -----------------------
df_customers.to_csv("customers.csv", index=False)
df_categories.to_csv("categories.csv", index=False)
df_products.to_csv("products.csv", index=False)
df_orders.to_csv("orders.csv", index=False)
df_order_items.to_csv("order_items.csv", index=False)

print("✅ Data generated successfully!")