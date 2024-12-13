import sqlite3

def init_db():
    conn = sqlite3.connect("../../users.db")
    cursor = conn.cursor()
    
    # Kullanıcı tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin'))
        )
    """)
    
    
    # Cafes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cafes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            location TEXT,
            details TEXT
        )
    """)
    
    # Feedbacks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feedback_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            cafe_name TEXT,
            review TEXT,
            rating INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            cafe_name TEXT,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (cafe_name) REFERENCES cafes (name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_cafes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            cafe_name TEXT,
            cafe_details TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
		# add a default admin user
    cursor.execute("""
        INSERT INTO users (username, password, role)
				VALUES ('admin', 'admin', 'admin')
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommended_cafes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        cafe_name TEXT,
        location TEXT,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    cursor.execute("""
        ALTER TABLE users ADD COLUMN points INTEGER DEFAULT 0
    """)
    
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()