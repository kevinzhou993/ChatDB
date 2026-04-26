import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

query = """
SELECT c.name, SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5
"""

df = pd.read_sql(query, conn)
print(df)

conn.close()