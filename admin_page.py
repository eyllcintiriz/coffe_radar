import streamlit as st
from db_helpers import get_reviews, remove_review, get_cafes, remove_cafe, get_reports, remove_report

def admin_page():
    st.title("Admin Interface")

    # Section for managing cafes
    st.subheader("Manage Cafes")
    cafes = get_cafes()
    for cafe in cafes:
        st.write(f"**{cafe}**")
        if st.button(f"Remove Cafe: {cafe}", key=f"remove_cafe_{cafe}"):
            remove_cafe(cafe)
            st.success(f"{cafe} removed successfully!")
            st.rerun()

    # Section for managing reviews
    st.subheader("Manage Reviews")
    for cafe in cafes:
        st.write(f"**Reviews for {cafe}**")
        reviews = get_reviews(cafe)
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
    for report_id, username, content_type, content_id, reason in reports:
        st.write(f"**Report ID**: {report_id}")
        st.write(f"**Reported by**: {username}")
        st.write(f"**Content Type**: {content_type}")
        st.write(f"**Content ID**: {content_id}")
        st.write(f"**Reason**: {reason}")
        if st.button(f"Remove Report: {report_id}", key=f"remove_report_{report_id}"):
            remove_report(report_id)
            st.success(f"Report {report_id} removed successfully!")
            st.rerun()
        st.write("---")

        # Section for managing reports
    st.subheader("Manage Reports")
    reports = get_reports()
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
                st.experimental_rerun()
        with cols[1]:
            if st.button("Remove Cafe", key=f"remove_cafe_{cafe_name}_{report_id}"):
                remove_cafe(cafe_name)
                remove_report(report_id)
                st.success(f"Cafe '{cafe_name}' removed.")
                st.experimental_rerun()

        st.markdown("---")