from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="RetailStock API")

# 1. Connect to SQLite (This automatically creates a file named 'retail.db')
conn = sqlite3.connect("retail.db", check_same_thread=False)
cursor = conn.cursor()

# 2. Create the database table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    stock INTEGER,
    price REAL
)
""")
conn.commit()

class Product(BaseModel):
    id: int
    name: str
    stock: int
    price: float

@app.get("/")
def home():
    return {"message": "RetailStock API is running perfectly."}

# 3. Read data from the real database
@app.get("/inventory")
def get_inventory():
    cursor.execute("SELECT * FROM products")
    items = cursor.fetchall()
    
    formatted_items = []
    for item in items:
        formatted_items.append({"id": item[0], "name": item[1], "stock": item[2], "price": item[3]})
        
    return formatted_items

# 4. Save new data into the real database
@app.post("/inventory")
def add_product(item: Product):
    # Check if ID already exists to prevent errors
    cursor.execute("SELECT * FROM products WHERE id=?", (item.id,))
    if cursor.fetchone():
        return {"error": "Product ID already exists."}
        
    cursor.execute("INSERT INTO products (id, name, stock, price) VALUES (?, ?, ?, ?)", 
                   (item.id, item.name, item.stock, item.price))
    conn.commit()
    return {"message": f"{item.name} permanently added to the database!"}