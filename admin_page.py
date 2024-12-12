import streamlit as st
from db_helpers import accept_recommended_cafe, get_recommended_cafes, get_reviews, remove_recommended_cafe, remove_review, get_cafes, remove_cafe, get_reports, remove_report

def admin_page():
    st.title("Admin Interface")

    # Section for managing cafes
    st.subheader("Manage Nearby Cafes")
    cafes = get_cafes()
    if not cafes:
        st.info("No cafes to show.")
    for cafe in cafes:
        st.write(f"**{cafe}**")
        if st.button(f"Remove Cafe: {cafe}", key=f"remove_cafe_{cafe}"):
            remove_cafe(cafe)
            st.success(f"{cafe} removed successfully!")
            st.rerun()

    # Section for managing reviews
    st.subheader("Manage Reviews")
    if not cafes:
        st.info("No cafes to show reviews for.")
    for cafe in cafes:
        st.write(f"**Reviews for {cafe}**")
        reviews = get_reviews(cafe)
        if not reviews:
            st.info("No reviews to show.")
        for review, rating, username in reviews:
            st.write(f"**{username}**")
            st.write(f"Rating: {rating} ⭐")
            st.write(f"Review: {review}")
            if st.button(f"Remove Review by {username}", key=f"remove_review_{username}_{cafe}"):
                remove_review(username, cafe)
                st.success(f"Review by {username} removed successfully!")
                st.rerun()
            st.write("---")


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