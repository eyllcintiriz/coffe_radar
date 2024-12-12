import json
import sqlite3

def authenticate(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

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
    
def get_users():
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users")
		users = cursor.fetchall()
		conn.close()
		return users

def promote_user(user_id):
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
		conn.commit()
		conn.close()
              
def demote_user(user_id):
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("UPDATE users SET role = 'user' WHERE id = ?", (user_id,))
		conn.commit()
		conn.close()

def get_user_id(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def add_cafe(name, location, details):
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("INSERT INTO cafes (name, location, details) VALUES (?, ?, ?)", (name, location, details))
		conn.commit()
		conn.close()

def get_cafes():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cafes")
    cafes = cursor.fetchall()
    conn.close()
    return [json.loads(cafe[3]) for cafe in cafes]

def is_cafe_in_favorites(user_id, cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorite_cafes WHERE user_id = ? AND cafe_name = ?", (user_id, cafe_name))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_favorite_cafe(user_id, cafe_name, cafe_details):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO favorite_cafes (user_id, cafe_name, cafe_details) VALUES (?, ?, ?)", (user_id, cafe_name, cafe_details))
    conn.commit()
    conn.close()

def get_favorite_cafes(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favorite_cafes WHERE user_id = ?", (user_id,))
    cafes = cursor.fetchall()
    conn.close()
    return cafes

def remove_favorite_cafe(user_id, cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorite_cafes WHERE user_id = ? AND cafe_name = ?", (user_id, cafe_name))
    conn.commit()
    conn.close()
    return True

def submit_feedback(user_id, feedback_text):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedbacks (user_id, feedback_text) VALUES (?, ?)",
        (user_id, feedback_text)
    )
    conn.commit()
    conn.close()
    
def get_feedbacks():
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM feedbacks")
		feedbacks = cursor.fetchall()
		conn.close()
		return feedbacks

def remove_feedback(feedback_id):
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("DELETE FROM feedbacks WHERE id = ?", (feedback_id,))
		conn.commit()
		conn.close()
              

def add_review(user_id, cafe_name, review, rating):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Check if the user has already reviewed this cafe
    cursor.execute("SELECT 1 FROM reviews WHERE user_id = ? AND cafe_name = ?", (user_id, cafe_name))
    existing_review = cursor.fetchone()
    
    if existing_review:
        conn.close()
        return False, "You have already reviewed this cafe."
    
    cursor.execute("INSERT INTO reviews (user_id, cafe_name, review, rating) VALUES (?, ?, ?, ?)", 
                   (user_id, cafe_name, review, rating))
    
    # Increment the user's points by a fixed amount (e.g., 10 points per review)
    cursor.execute("UPDATE users SET points = points + 10 WHERE id = ?", (user_id,))
    
    conn.commit()
    conn.close()
    return True, "Review submitted successfully."

def get_reviews(cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reviews.review, reviews.rating, users.username
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.cafe_name = ?
    """, (cafe_name,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def get_user_reviews(user_id):
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("SELECT cafe_name, review, rating FROM reviews WHERE user_id = ?", (user_id,))
		reviews = cursor.fetchall()
		conn.close()
		return reviews

def remove_review(username, cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM reviews
        WHERE user_id = (SELECT id FROM users WHERE username = ?) AND cafe_name = ?
    """, (username, cafe_name))
    conn.commit()
    conn.close()

def remove_cafe(cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cafes WHERE name = ?", (cafe_name,))
    cursor.execute("DELETE FROM reviews WHERE cafe_name = ?", (cafe_name,))
    cursor.execute("DELETE FROM favorite_cafes WHERE cafe_name = ?", (cafe_name,))
    cursor.execute("DELETE FROM reports WHERE cafe_name = ?", (cafe_name,))
    conn.commit()
    conn.close()

def add_report(user_id, cafe_name, reason):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (user_id, cafe_name, reason) VALUES (?, ?, ?)",
                   (user_id, cafe_name, reason))
    conn.commit()
    conn.close()

def get_reports():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reports.id, users.username, reports.cafe_name, reports.reason, reports.timestamp
        FROM reports
        JOIN users ON reports.user_id = users.id
    """)
    reports = cursor.fetchall()
    conn.close()
    return reports

def remove_report(report_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()
    
# calculate combined ratings from yelp and db users and return rating and reviews count
def calculate_rating(yelp_cafe_rating, yelp_cafe_rating_count, cafe_name):
		conn = sqlite3.connect("users.db")
		cursor = conn.cursor()
		cursor.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE cafe_name = ?", (cafe_name,))
		db_rating, db_rating_count = cursor.fetchone()
		conn.close()
		
		if db_rating is None:
				return yelp_cafe_rating, yelp_cafe_rating_count
		else:
				combined_rating = (yelp_cafe_rating * yelp_cafe_rating_count + db_rating * db_rating_count) / (yelp_cafe_rating_count + db_rating_count)
				return round(combined_rating, 1), yelp_cafe_rating_count + db_rating_count
          
def get_user_role(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "user"

def submit_recommended_cafe(user_id, cafe_name, location, description):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO recommended_cafes (user_id, cafe_name, location, description)
        VALUES (?, ?, ?, ?)
    """, (user_id, cafe_name, location, description))
    conn.commit()
    conn.close()

def get_recommended_cafes():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT recommended_cafes.id, users.username, recommended_cafes.cafe_name,
               recommended_cafes.location, recommended_cafes.description, recommended_cafes.timestamp
        FROM recommended_cafes
        JOIN users ON recommended_cafes.user_id = users.id
    """)
    cafes = cursor.fetchall()
    conn.close()
    return cafes

def remove_recommended_cafe(recommendation_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recommended_cafes WHERE id = ?", (recommendation_id,))
    conn.commit()
    conn.close()

def accept_recommended_cafe(recommendation_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Get the recommended cafe details
    cursor.execute("SELECT cafe_name, location FROM recommended_cafes WHERE id = ?", (recommendation_id,))
    cafe = cursor.fetchone()
    if cafe:
        cafe_name, location = cafe
        # Add to cafes table
        cursor.execute("INSERT INTO cafes (name, location, features) VALUES (?, ?, '')", (cafe_name, location))
        # Remove from recommended_cafes table
        cursor.execute("DELETE FROM recommended_cafes WHERE id = ?", (recommendation_id,))
        conn.commit()
    conn.close()