from pymongo import MongoClient
import sys

print("=" * 50)
print("DOCUMENT STORE WITH MONGODB")
print("=" * 50)

try:
    # Coba konek ke MongoDB
    print("Mencoba koneksi ke MongoDB...")
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
    # Test koneksi
    client.admin.command('ping')
    print("✅ Berhasil konek ke MongoDB!\n")
    
    db = client['ecommerce']
    products = db['products']
    
    # Hapus data lama (opsional)
    products.delete_many({})
    
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
    print("✅ Data berhasil disimpan ke MongoDB!\n")
    
    # Query: cari produk dengan harga < 1 juta
    cheap_products = products.find({"price": {"$lt": 1000000}})
    print("🛒 Produk murah (harga < Rp1.000.000):")
    for p in cheap_products:
        print(f"  - {p['name']} : Rp{p['price']:,}")
    
    # Update: tambah diskon
    products.update_one({"name": "Laptop Gaming"}, {"$set": {"discount": 10}})
    print("\n✅ Diskon 10% ditambahkan ke Laptop Gaming")
    
    # Tampilkan semua
    print("\n📦 Semua produk:")
    for p in products.find():
        print(f"  {p}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n" + "=" * 50)
    print("MongoDB TIDAK TERINSTALL di Codespace ini.")
    print("\nSOLUSI:")
    print("1. Gunakan kode SIMULASI (document_store_simulasi.py)")
    print("2. Atau install MongoDB dengan perintah:")
    print("   sudo apt-get update")
    print("   sudo apt-get install -y mongodb")
    print("   sudo service mongodb start")
    print("=" * 50)
    
    # Tampilkan simulasi sebagai fallback
    print("\n\n📚 MENAMPILKAN SIMULASI (tanpa MongoDB):\n")
    
    # Simulasi data
    simulated_products = [
        {"name": "Laptop Gaming", "price": 15000000, "specs": {"ram": "16GB", "storage": "512GB SSD"}, "tags": ["electronics", "gaming"]},
        {"name": "Mouse Wireless", "price": 250000, "specs": {"dpi": 3200, "wireless": True}, "tags": ["electronics", "accessories"]}
    ]
    
    print("🛒 Produk murah (harga < Rp1.000.000):")
    for p in simulated_products:
        if p['price'] < 1000000:
            print(f"  - {p['name']} : Rp{p['price']:,}")
    
    # Update simulasi
    for p in simulated_products:
        if p['name'] == "Laptop Gaming":
            p['discount'] = 10
    
    print("\n📦 Semua produk (simulasi):")
    for p in simulated_products:
        print(f"  {p}")
    
    print("\n✅ SIMULASI SELESAI")

print("\n" + "=" * 50)
