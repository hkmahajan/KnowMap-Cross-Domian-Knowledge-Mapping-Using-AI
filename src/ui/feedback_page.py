import streamlit as st
import pandas as pd

def feedback_page():
    st.title("💬 User Feedback System")

    st.write("Please rate the relevance of the extracted graph.")
    rating = st.slider("Rate Graph Accuracy", 1, 5, 3)
    comment = st.text_area("Additional Comments")

    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")
        st.write(f"⭐ Rating: {rating}/5")
        st.write(f"🗒️ Comment: {comment}")

    st.markdown("---")
    st.subheader("📈 Recent Feedback")
    feedback_data = {
        "User": ["User1", "User2", "User3"],
        "Rating": [5, 4, 3],
        "Comment": ["Great output!", "Good accuracy", "Needs better linking"]
    }
    df = pd.DataFrame(feedback_data)
    st.dataframe(df)
