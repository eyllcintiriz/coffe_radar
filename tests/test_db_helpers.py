from src.utils.db_helpers import *
from tests.conftest import setup_db

def test_authenticate(setup_db):
    conn = setup_db
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("testuser", "testpass"))
    conn.commit()
    users = get_users()
    print(f"Users: {users}")
    user = authenticate("testuser", "testpass")
    print(f"User: {user}")
    assert user is not None

def test_register_user(setup_db):
    conn = setup_db
    success, message = register_user("newuser", "newpass")
    print(f"Success: {success}, Message: {message}")
    assert success
    assert message == "Kayıt başarılı!"

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", ("newuser",))
    user = cursor.fetchone()
    assert user is not None

def test_get_users(setup_db):
    conn = setup_db
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user1", "pass1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user2", "pass2"))
    conn.commit()

    users = get_users()
    assert len(users) == 5 

def test_promote_user(setup_db):
    conn = setup_db
    cursor = conn.cursor()
    user_id = get_user_id("user1")
    promote_user(user_id)
    cursor.execute("SELECT role FROM users WHERE username = ?", ("user1",))
    role = cursor.fetchone()[0]
    assert role == "admin"

def test_demote_user(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	demote_user(user_id)

	cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
	role = cursor.fetchone()[0]
	assert role == "user"

def test_add_cafe(setup_db):
	add_cafe("Cafe1", "Location1", json.dumps({"detail": "Details1"}))
	conn = setup_db
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM cafes WHERE name = ?", ("Cafe1",))
	cafe = cursor.fetchone()
	assert cafe is not None

def test_get_cafes(setup_db):
	cafes = get_cafes()
	assert len(cafes) == 1

def test_add_favorite_cafe(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	add_favorite_cafe(user_id, "Cafe1", json.dumps({"detail": "Details1"}))

	cursor.execute("SELECT * FROM favorite_cafes WHERE user_id = ? AND cafe_name = ?", (user_id, "Cafe1"))
	favorite = cursor.fetchone()
	assert favorite is not None

def test_get_favorite_cafes(setup_db):
	user_id = get_user_id("user1")

	favorites = get_favorite_cafes(user_id)
	assert len(favorites) == 1

def test_remove_favorite_cafe(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	remove_favorite_cafe(user_id, "Cafe1")

	cursor.execute("SELECT * FROM favorite_cafes WHERE user_id = ? AND cafe_name = ?", (user_id, "Cafe1"))
	favorite = cursor.fetchone()
	assert favorite is None

def test_submit_feedback(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	submit_feedback(user_id, "Great app!")

	cursor.execute("SELECT * FROM feedbacks WHERE user_id = ?", (user_id,))
	feedback = cursor.fetchone()
	assert feedback is not None

def test_get_feedbacks(setup_db):
	conn = setup_db

	feedbacks = get_feedbacks()
	assert len(feedbacks) == 1

def test_remove_feedback(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")

	cursor.execute("SELECT id FROM feedbacks WHERE user_id = ?", (user_id,))
	feedback_id = cursor.fetchone()[0]
	remove_feedback(feedback_id)

	cursor.execute("SELECT * FROM feedbacks WHERE id = ?", (feedback_id,))
	feedback = cursor.fetchone()
	assert feedback is None

def test_add_review(setup_db):
	user_id = get_user_id("user1")
	success, message = add_review(user_id, "Cafe1", "Nice place", 4)
	assert success
	assert message == "Yorumunuz başarıyla gönderildi."

def test_get_reviews(setup_db):
	conn = setup_db

	reviews = get_reviews("Cafe1")
	assert len(reviews) == 1

def test_remove_review(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	remove_review("user1", "Cafe1")

	cursor.execute("SELECT * FROM reviews WHERE user_id = ? AND cafe_name = ?", (user_id, "Cafe1"))
	review = cursor.fetchone()
	assert review is None

def test_remove_cafe(setup_db):
	remove_cafe("Cafe1")
	conn = setup_db
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM cafes WHERE name = ?", ("Cafe1",))
	cafe = cursor.fetchone()
	assert cafe is None

def test_add_report(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	add_report(user_id, "Cafe1", "Reason1")

	cursor.execute("SELECT * FROM reports WHERE user_id = ? AND cafe_name = ?", (user_id, "Cafe1"))
	report = cursor.fetchone()
	assert report is not None

def test_get_reports(setup_db):
	reports = get_reports()
	assert len(reports) == 1

def test_remove_report(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")

	cursor.execute("SELECT id FROM reports WHERE user_id = ? AND cafe_name = ?", (user_id, "Cafe1"))
	report_id = cursor.fetchone()[0]
	remove_report(report_id)

	cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
	report = cursor.fetchone()
	assert report is None

def test_get_user_role(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	role = get_user_role(user_id)
	assert role == "user"

def test_submit_recommended_cafe(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	user_id = get_user_id("user1")
	submit_recommended_cafe(user_id, "Cafe10", "Location1", "Description1")

	cursor.execute("SELECT * FROM recommended_cafes WHERE user_id = ? AND cafe_name = ?", (user_id, "Cafe10"))
	recommendation = cursor.fetchone()
	assert recommendation is not None

def test_get_recommended_cafes(setup_db):
	conn = setup_db
	cursor = conn.cursor()

	recommendations = get_recommended_cafes()
	assert len(recommendations) == 1
