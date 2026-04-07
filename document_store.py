# document_store.py
from pymongo import MongoClient
import json

# Koneksi (di Codespace MongoDB berjalan di localhost)
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
products = db['products']

# Insert dokumen
product1 = {
    "name": "Laptop Gaming",
    "price": 15000000,
    "specs": {"ram": "16GB", "storage": "512GB SSD"},
    "tags": ["electronics", "gaming"]
}
product2 = {
    "name": "Mouse Wireless",
    "price": 250000,
    "specs": {"dpi": 3200, "wireless": True},
    "tags": ["electronics", "accessories"]
}
products.insert_many([product1, product2])

# Query: cari produk dengan harga < 1 juta
cheap_products = products.find({"price": {"$lt": 1000000}})
print("Produk murah:")
for p in cheap_products:
    print(f"- {p['name']} : Rp{p['price']}")

# Update: tambah diskon
products.update_one({"name": "Laptop Gaming"}, {"$set": {"discount": 10}})

# Tampilkan semua
print("\nSemua produk:")
for p in products.find():
    print(p)