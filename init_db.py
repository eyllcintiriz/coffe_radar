import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Kullanıcı tablosunu oluştur veya güncelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            phone TEXT,
            address TEXT
        )
    """)

    # Tabloya `email` sütununu ekle (varsa atla)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass  # Sütun zaten varsa hata vermez

    # Eksik sütunları ekle
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
    except sqlite3.OperationalError:
        pass  # `phone` sütunu zaten varsa hata vermez
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address TEXT")
    except sqlite3.OperationalError:
        pass  # `address` sütunu zaten varsa hata vermez

    
    # Favori kafeler tablosu, cafe_id Yelp API'den geliyor, cafe_details ise JSON formatındaki detaylar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_cafes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            cafe_id TEXT,
            cafe_details TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Kafeler tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cafes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            location TEXT,
            features TEXT
        )
    """)
    
		# Geri bildirim tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feedback_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Örnek kafeler ekleme
    cafes = [
        ("Cafe Latte", "Ankara, Turkey", "WiFi, Outdoor Seating"),
        ("Espresso House", "Istanbul, Turkey", "Pet Friendly, Vegan Options"),
        ("Brewed Awakening", "Izmir, Turkey", "Cozy Atmosphere, Specialty Coffee"),
    ]
    for cafe in cafes:
        try:
            cursor.execute("INSERT INTO cafes (name, location, features) VALUES (?, ?, ?)", cafe)
        except sqlite3.IntegrityError:
            pass  # Eğer kafe zaten varsa hata vermesin!
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()