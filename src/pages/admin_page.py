import streamlit as st
from src.utils.db_helpers import accept_recommended_cafe, get_recommended_cafes, get_reviews, remove_recommended_cafe, remove_review, get_cafes, remove_cafe, get_reports, remove_report
from src.utils.db_helpers import get_reviews, remove_review, get_cafes, remove_cafe, get_reports, remove_report, get_feedbacks, remove_feedback, get_users, promote_user, demote_user

def admin_page():
    st.title("Admin Interface")

    # Section for managing cafes
    st.subheader("Manage Cafes")
    cafes = get_cafes()
    if not cafes:
        st.info("No cafes to show.")
    else:
        num_columns = 3  # Number of cafes per row
        for i in range(0, len(cafes), num_columns):
            cols = st.columns(num_columns)
            for col, cafe in zip(cols, cafes[i:i+num_columns]):
                with col:
                    st.markdown(f"**{cafe['name']}**")
                    if st.button("Remove Cafe", key=f"remove_cafe_{cafe['name']}"):
                        remove_cafe(cafe['name'])
                        st.success(f"{cafe['name']} removed successfully!")
                        st.rerun()

    st.markdown("---")

    # Section for managing reviews
    st.subheader("Manage Reviews")
    if not cafes:
        st.info("No cafes to show reviews for.")
    else:
        for cafe in cafes:
            reviews = get_reviews(cafe['name'])
            if not reviews:
                continue
            else:
                st.markdown(f"**Reviews for {cafe['name']}**")
                num_columns = 2  # Number of reviews per row
                cols = st.columns(num_columns)
                
                for review, rating, username in reviews:
                    col = cols[reviews.index((review, rating, username)) % num_columns]
                    with col:
                        st.markdown(f"**{username}**")
                        st.write(f"Rating: {rating} ⭐")
                        st.write(f"Review: {review}")
                        if st.button("Remove Review", key=f"remove_review_{username}_{cafe['name']}"):
                            remove_review(username, cafe['name'])
                            st.success(f"Review by {username} removed successfully!")
                            st.rerun()
                            st.write("---")

    st.markdown("---")

    # Section for managing reports
    st.subheader("Manage Reports")
    reports = get_reports()
    if not reports:
        st.info("No reports to show.")
    for report in reports:
        report_id, username, cafe_name, reason, timestamp = report
        st.write(f"**Report ID**: {report_id}")
        st.write(f"**Reported by**: {username}")
        st.write(f"**Cafe**: {cafe_name}")
        st.write(f"**Reason**: {reason}")
        st.write(f"**Timestamp**: {timestamp}")

        cols = st.columns([1, 1])
        with cols[0]:
            if st.button("Dismiss Report", key=f"dismiss_{report_id}"):
                remove_report(report_id)
                st.success(f"Report {report_id} dismissed.")
                st.rerun()
        with cols[1]:
            if st.button("Remove Cafe", key=f"remove_cafe_{cafe_name}_{report_id}"):
                remove_cafe(cafe_name)
                remove_report(report_id)
                st.success(f"Cafe '{cafe_name}' removed.")
                st.rerun()

        st.markdown("---")

        # Section for managing recommended cafes
    st.subheader("Manage Recommended Cafes")
    recommended_cafes = get_recommended_cafes()
    for recommendation in recommended_cafes:
        recommendation_id, username, cafe_name, location, description, timestamp = recommendation
        st.write(f"**Recommendation ID**: {recommendation_id}")
        st.write(f"**Recommended by**: {username}")
        st.write(f"**Cafe Name**: {cafe_name}")
        st.write(f"**Location**: {location}")
        st.write(f"**Description**: {description}")
        st.write(f"**Timestamp**: {timestamp}")

        cols = st.columns([1, 1, 4])
        with cols[0]:
            if st.button("Accept", key=f"accept_{recommendation_id}"):
                accept_recommended_cafe(recommendation_id)
                st.success(f"Cafe '{cafe_name}' has been accepted and added to the database.")
                st.rerun()
        with cols[1]:
            if st.button("Reject", key=f"reject_{recommendation_id}"):
                remove_recommended_cafe(recommendation_id)
                st.info(f"Recommendation '{cafe_name}' has been rejected.")
                st.rerun()

        st.markdown("---")
    st.markdown("---")
        
    # Section for managing feedbacks
    st.subheader("Manage Feedbacks")
    feedbacks = get_feedbacks()
    if not feedbacks:
        st.info("No feedbacks to show.")
    for feedback in feedbacks:
        feedback_id, user_id, feedback_text, timestamp = feedback
        username = get_users()[user_id - 1][1]
        st.write(f"**Feedback ID**: {feedback_id}")
        st.write(f"**Username**: {username}")
        st.write(f"**Feedback**: {feedback_text}")
        st.write(f"**Timestamp**: {timestamp}")

        if st.button("Remove Feedback", key=f"remove_feedback_{feedback_id}"):
            remove_feedback(feedback_id)
            st.success(f"Feedback {feedback_id} removed.")
            st.rerun()

    st.markdown("---")
        
    # Section for managing users
    st.subheader("Manage Users")
    users = get_users()
    if not users:
        st.info("No users to show.")
    else:
        num_columns = 3  # Number of columns per row
        for i in range(0, len(users), num_columns):
            cols = st.columns(num_columns)
            for col, user in zip(cols, users[i:i+num_columns]):
                user_id, username, _password, email, phone, address, role, points = user
                with col:
                    st.markdown(f"#### {username} ({role.title()})")
                    st.write(f"**Email:** {email}")
                    st.write(f"**Phone:** {phone}")
                    if role.lower() != "admin":
                        if st.button("Promote to Admin", key=f"promote_{user_id}"):
                            promote_user(user_id)
                            st.success(f"{username} promoted to admin.", icon="👑")
                    else:
                        if st.button("Demote to User", key=f"demote_{user_id}"):
                            demote_user(user_id)
                            st.success(f"{username} demoted to user.", icon="👤")

    st.markdown("---")
