import sqlite3

# Kullanıcı doğrulama
def authenticate(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Kullanıcı kaydı
def register_user(username, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True, "Kayıt başarılı!"
    except sqlite3.IntegrityError:
        return False, "Bu kullanıcı adı zaten alınmış!"

# Kullanıcı ID'sini al
def get_user_id(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

# Kafelerle ilgili fonksiyonlar
def get_cafes():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cafes")
    cafes = cursor.fetchall()
    conn.close()
    return [cafe[0] for cafe in cafes]

def get_cafe_details(cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT location, features FROM cafes WHERE name = ?", (cafe_name,))
    details = cursor.fetchone()
    conn.close()
    return details

# Favori kafelerle ilgili fonksiyonlar
def is_cafe_in_favorites(user_id, cafe_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorite_cafes WHERE user_id = ? AND cafe_id = ?", (user_id, cafe_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_favorite_cafe(user_id, cafe_id, cafe_details):
    print(cafe_details)
    print(cafe_id)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO favorite_cafes (user_id, cafe_id, cafe_details) VALUES (?, ?, ?)", (user_id, cafe_id, cafe_details))
    conn.commit()
    conn.close()

def get_favorite_cafes(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favorite_cafes WHERE user_id = ?", (user_id,))
    cafes = cursor.fetchall()
    conn.close()
    return cafes

def remove_favorite_cafe(user_id, cafe_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorite_cafes WHERE user_id = ? AND cafe_id = ?", (user_id, cafe_id))
    conn.commit()
    conn.close()
    
def submit_feedback(user_id, feedback_text):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (user_id, feedback_text) VALUES (?, ?)",
        (user_id, feedback_text)
    )
    conn.commit()
    conn.close()