import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Existing tables remain the same...
    
    # New table for policy acceptance tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_policy_acceptance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            privacy_policy_accepted INTEGER DEFAULT 0,
            terms_of_service_accepted INTEGER DEFAULT 0,
            acceptance_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Rest of the existing code remains the same...
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
