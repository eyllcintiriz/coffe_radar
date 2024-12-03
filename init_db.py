import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Kullanıcı tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    
    # Favori kafeler tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_cafes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            cafe_name TEXT,
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
    
    # Örnek kafeler ekleme
    #apiden çekilen veriler ile oluşturulacak ????
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
