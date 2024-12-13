# Coffee Radar https://cofferadar-10.streamlit.app

Coffee Radar is a web application that helps users discover nearby cafes, manage their favorite cafes, and provide feedback. The application also includes an admin interface for managing cafes, reviews, reports, and user recommendations.

## Features

- **User Authentication**: Users can register and log in to the application.
- **Cafe Discovery**: Users can discover nearby cafes based on their location.
- **Favorite Cafes**: Users can add cafes to their favorites list and manage them.
- **Reviews and Ratings**: Users can leave reviews and ratings for cafes.
- **Feedback**: Users can provide feedback about the application.
- **Admin Interface**: Admins can manage cafes, reviews, reports, and user recommendations.

## Pages

### Main Page
- Discover nearby cafes based on your location.
- View cafes on a map and sort them by distance, rating, or popularity.

### Favorite Cafes
- View and manage your favorite cafes.
- Remove cafes from your favorites list.

### Profile Page
- View and update your profile information.
- View your reviews and ratings.

### Recommend Cafe
- Recommend a new cafe to be added to the database.

### Feedback Page
- Provide feedback about the application.

### Admin Page
- Manage cafes, reviews, reports, and user recommendations.
- Promote or demote users.

### Privacy Policy and Terms of Service
- View the privacy policy and terms of service of the application.

## Installation

1. Clone the repository:
	```bash
	git clone https://github.com/yourusername/coffe_radar.git
	cd coffe_radar
	```

2. Install the required dependencies:
	```bash
	pip install -r requirements.txt
	```

3. Initialize the database inside src/data:
	```bash
	python init_db.py
	```

4. Run the application:
	```bash
	streamlit run app.py
	```

## Database Schema

- **users**: Stores user information (username, password, email, phone, address, role, points).
- **cafes**: Stores cafe information (name, location, details).
- **feedbacks**: Stores user feedback (user_id, feedback_text, timestamp).
- **reviews**: Stores user reviews (user_id, cafe_name, review, rating).
- **reports**: Stores reports about cafes (user_id, cafe_name, reason, timestamp).
- **favorite_cafes**: Stores user's favorite cafes (user_id, cafe_name, cafe_details).
- **recommended_cafes**: Stores user-recommended cafes (user_id, cafe_name, location, description, timestamp).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the GPL License.

## Contact

For any questions or feedback, please contact us via the feedback page in the application.
