import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

base_dir = os.path.dirname(__file__)
env_path = os.path.join(base_dir, "..", ".env")
load_dotenv(env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_schema():
    return """
Tables:

customers(customer_id, name, email, city, state, signup_date)
categories(category_id, category_name)
products(product_id, product_name, category_id, price)
orders(order_id, customer_id, order_date, total_amount, status)
order_items(order_item_id, order_id, product_id, quantity, unit_price)
"""


def generate_sql(user_query):
    prompt = f"""
You are a SQL assistant.

Given the following database schema:
{get_schema()}

Convert the user request into a valid SQLite SQL query.

Rules:
- Only use the tables and columns provided
- Use JOIN when needed
- Only return ONE SQLite SQL query
- Never return multiple SQL statements
- Do not include markdown code fences
- SQLite syntax only

User request:
{user_query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a SQL generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    if sql.startswith("```sql"):
        sql = sql.replace("```sql", "", 1).strip()
    if sql.startswith("```"):
        sql = sql.replace("```", "", 1).strip()
    if sql.endswith("```"):
        sql = sql[:-3].strip()

    return sql


def validate_sql(sql):
    return sql.strip().lower().startswith("select")


def execute_sql(sql):
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, "..", "database", "ecommerce.db")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(sql, conn)
    conn.close()

    columns = df.columns.tolist()
    rows = df.values.tolist()
    return columns, rows


if __name__ == "__main__":
    while True:
        user_input = input("Ask your database: ")

        try:
            sql = generate_sql(user_input)
            print("\nGenerated SQL:\n")
            print(sql)

            if not validate_sql(sql):
                print("\nOnly SELECT queries are allowed.")
                continue

            df = execute_sql(sql)
            print("\nQuery Result:\n")
            print(df.head(20))

        except Exception as e:
            print("\nError:", e)