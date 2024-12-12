import sqlite3

# Existing functions remain the same...

def accept_policies(user_id, privacy_policy=False, terms_of_service=False):
    """
    Record user's acceptance of privacy policy and terms of service
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        # Try to insert or update policy acceptance
        cursor.execute("""
            INSERT OR REPLACE INTO user_policy_acceptance 
            (user_id, privacy_policy_accepted, terms_of_service_accepted) 
            VALUES (?, ?, ?)
        """, (user_id, int(privacy_policy), int(terms_of_service)))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

def check_policy_acceptance(user_id):
    """
    Check if user has accepted both policies
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT privacy_policy_accepted, terms_of_service_accepted 
            FROM user_policy_acceptance 
            WHERE user_id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        
        if result:
            return {
                'privacy_policy': bool(result[0]),
                'terms_of_service': bool(result[1])
            }
        return {
            'privacy_policy': False,
            'terms_of_service': False
        }
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {
            'privacy_policy': False,
            'terms_of_service': False
        }
    finally:
        conn.close()

# Modify register_user to handle policy acceptance
def register_user(username, password, accept_privacy=False, accept_terms=False):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # First, insert the user
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        user_id = cursor.lastrowid
        
        # Then, if policies are accepted, record that
        if accept_privacy or accept_terms:
            cursor.execute("""
                INSERT INTO user_policy_acceptance 
                (user_id, privacy_policy_accepted, terms_of_service_accepted) 
                VALUES (?, ?, ?)
            """, (user_id, int(accept_privacy), int(accept_terms)))
        
        conn.commit()
        return True, "Kayıt başarılı!"
    except sqlite3.IntegrityError:
        return False, "Bu kullanıcı adı zaten alınmış!"
    finally:
        conn.close()
