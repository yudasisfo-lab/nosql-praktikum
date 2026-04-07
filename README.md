# nosql-praktikum
Modul Praktikum NoSQL yang dirancang untuk dijalankan di GitHub Codespaces. 
Modul ini mencakup simulasi keempat jenis database NoSQL (Document, Key-Value, Column, Graph) beserta studi kasus, perbandingan, dan rekomendasi.

Tujuan
1.Memahami karakteristik 4 jenis NoSQL.
2.Mensimulasikan operasi CRUD sederhana di masing-masing jenis.
3.Membandingkan performa dan struktur data.
4.Memberikan rekomendasi berdasarkan kebutuhan sistem.

Prasyarat
1.Akun GitHub
2.Browser modern
3.Basic SQL/Python (opsional)

Bagian 1: Setup Codespace
1.Buat repository baru di GitHub (misal: nosql-praktikum).
2.Tambahkan file .devcontainer/devcontainer.json:

{
  "name": "NoSQL Lab",
  "image": "mcr.microsoft.com/devcontainers/universal:linux",
  "features": {
    "ghcr.io/devcontainers/features/python:1": {},
    "ghcr.io/devcontainers/features/redis:1": {},
    "ghcr.io/devcontainers/features/mongodb:1": {}
  },
  "postCreateCommand": "pip install pymongo redis cassandra-driver neo4j"
}

3.Buka Codespace (klik <> Code → Codespaces → Create codespace on main).
4.Tunggu hingga semua dependensi terinstal.

Bagian 2: Document Store (MongoDB)
Karakteristik
1.Data dalam bentuk JSON-like (BSON)
2.Schema-less
3.Cocok untuk CMS, catalog product, user profile

Simulasi: Sistem Manajemen Produk
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


Jalankan:
python document_store.py

Bagian 3: Key-Value Store (Redis)
Karakteristik
1.Data sebagai pasangan key-value
2.Sangat cepat, in-memory
3.Cocok untuk caching, session store, real-time counter

Simulasi: Shopping Cart & Session
# keyvalue_store.py
import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Simulasi session user
user_id = "user:1001"
r.hset(user_id, mapping={
    "name": "Budi",
    "last_active": time.time(),
    "cart_total": 0
})

# Shopping cart (gunakan hash)
cart_key = f"cart:{user_id}"
r.hset(cart_key, "laptop", "1")
r.hset(cart_key, "mouse", "2")

# Tampilkan cart
items = r.hgetall(cart_key)
print("Shopping Cart Budi:")
for product, qty in items.items():
    print(f"  {product}: {qty} pcs")

# Update total belanja
r.hincrby(cart_key, "mouse", 1)  # tambah mouse 1 lagi
print("\nSetelah update mouse +1:")
print(r.hgetall(cart_key))

# Simpan data produk (string)
r.set("product:mouse:price", 250000)
price = r.get("product:mouse:price")
print(f"\nHarga mouse: Rp{price}")

# TTL - session expire 60 detik
r.expire(f"cart:{user_id}", 60)
print("Cart akan expired dalam 60 detik")

Jalankan:
python keyvalue_store.py

Bagian 4: Column-Family Store (Cassandra)
Karakteristik
1.Data dalam baris & kolom, tapi per baris bisa beda kolom
2.High write throughput, scalable linear
3.Cocok untuk time-series data, logging, IoT

Simulasi: Sensor IoT Logging
# column_store.py
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import uuid
from datetime import datetime

# Koneksi (Cassandra tidak otomatis di Codespace, kita gunake mock/simulasi)
# Untuk simulasi, kita buat class sederhana meniru konsep column-family
print("=== SIMULASI COLUMN-FAMILY STORE ===\n")
print("Konsep: Setiap baris (sensor_id) memiliki kolom timestamp yang berbeda-beda")

# Simulasi data dalam dictionary of dictionaries
sensor_data = {
    "sensor_temp_01": {
        "2025-04-07T10:00": 23.5,
        "2025-04-07T10:05": 23.7,
        "2025-04-07T10:10": 24.1
    },
    "sensor_hum_02": {
        "2025-04-07T10:00": 55,
        "2025-04-07T10:05": 54,
        "2025-04-07T10:10": 56
    }
}

# Insert data baru (time-series)
def insert_reading(sensor_id, timestamp, value):
    if sensor_id not in sensor_data:
        sensor_data[sensor_id] = {}
    sensor_data[sensor_id][timestamp] = value

insert_reading("sensor_temp_01", "2025-04-07T10:15", 24.3)

# Query: baca semua data dari sensor tertentu
print("Data sensor_temp_01:")
for ts, val in sensor_data["sensor_temp_01"].items():
    print(f"  {ts} -> {val}°C")

# Query: range timestamp (simulasi filter)
target_time = "2025-04-07T10:05"
if target_time in sensor_data["sensor_temp_01"]:
    print(f"\nNilai pada {target_time}: {sensor_data['sensor_temp_01'][target_time]}°C")


Catatan: Cassandra membutuhkan cluster terpisah. Untuk praktikum penuh, bisa gunakan Docker atau Astra DB free tier. Modul ini menggunakan simulasi konsep.

Bagian 5: Graph Store (Neo4j)
Karakteristik
1.Data sebagai node, relationship, property
2.Optimasi untuk hubungan kompleks
3.Cocok untuk social network, rekomendasi, fraud detection

Simulasi: Social Media Follow
# graph_store.py
from neo4j import GraphDatabase
import os

# Simulasi karena Neo4j tidak default di Codespace
# Kita gunakan dictionary structure untuk mensimulasikan graph

print("=== SIMULASI GRAPH DATABASE ===\n")

# Node: {id: {name, properties}}
nodes = {
    "alice": {"name": "Alice", "age": 25},
    "budi": {"name": "Budi", "age": 27},
    "citra": {"name": "Citra", "age": 24},
    "doni": {"name": "Doni", "age": 26}
}

# Edges: (from, to, relationship_type)
edges = [
    ("alice", "budi", "follows"),
    ("alice", "citra", "follows"),
    ("budi", "doni", "follows"),
    ("citra", "alice", "follows"),
    ("doni", "alice", "follows")
]

# Fungsi query: siapa yang diikuti oleh Alice?
def get_followed_by(user_id):
    followed = [to for (frm, to, rel) in edges if frm == user_id and rel == "follows"]
    return [nodes[u]["name"] for u in followed]

# Fungsi rekomendasi: teman dari teman yang belum diikuti
def recommend_friends(user_id):
    # Teman langsung
    direct = set(get_followed_by(user_id))
    # Teman dari teman
    friends_of_friends = set()
    for friend in direct:
        for ff in get_followed_by(friend):
            if ff != user_id and ff not in direct:
                friends_of_friends.add(ff)
    return [nodes[f]["name"] for f in friends_of_friends]

print("Alice mengikuti:", get_followed_by("alice"))
print("\nRekomendasi untuk Alice (teman dari teman):", recommend_friends("alice"))

# Simulasi query jarak 2 hop
print("\nGraph connection:")
for frm, to, rel in edges:
    print(f"  {nodes[frm]['name']} {rel} {nodes[to]['name']}")


Bagian 6: Perbandingan & Rekomendasi
Tabel Perbandingan
Kriteria	    |Document(MongoDB)	  |Key-Value(Redis)  	  |Column(Cassandra)	 |Graph(Neo4j)
Data Model	  |JSON-like	          |Hash/List/Set	      |Row with columns	   |Nodes & edges
Query	        |Rich (aggregation)	  |Get/Set by key	      |By partition key	   |Pattern matching (Cypher)
Scalability   |High (sharding)	    |High (cluster)	      |Very high	         |Medium-High
Use Case	    |CMS, catalog	        |Cache, session	      |Logging, IoT	       |Social, fraud
Consistency	  |Tunable	            |Strong (by default)	|Tunable (eventual)	 |Strong
Complexity	  |Medium	              |Low	                |High	               |High

Studi Kasus Penerapan
1.E-commerce Platform
  Document: Product catalog, user reviews
  Key-Value: Cart, session, rate limiter
  Graph: Rekomendasi produk "orang lain juga membeli"

2.Sistem Monitoring IoT
  Column: Time-series sensor data
  Key-Value: Device status terbaru (cache)

3.Social Media App
  Graph: Friend connection, feed generation
  Document: User profile, posts
  Key-Value: Like counters, session

