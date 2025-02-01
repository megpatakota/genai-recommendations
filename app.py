from utils import get_recommendations
import streamlit as st

# Function to display recommendations in a structured format
def display_recommendations(recommendations):
    st.subheader("🎉 Your Personalized Yonder Experiences 🎉")

    for rec in recommendations["recommendations"]:
        print(f"RECOMMENDATION: {rec}")
        with st.container():
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #4CAF50; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin-bottom: 10px;
                    background-color: #f9f9f9;">
                    <h3 style="color: #333;">{rec.title}</h3>
                    <p><strong>Category:</strong> {rec.category} 🏷️</p>
                    <p>{rec.explanation}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Streamlit UI
st.title("🎯 Yonder Experience Recommender")
st.subheader("🔎 Discover Your Next Adventure!")

# Store user input in session state
if "selected_member_id" not in st.session_state:
    st.session_state.selected_member_id = ""

# 🔥 Fix: Avoid duplicate button issues
member_id_input = st.text_input("Enter Member ID")


if st.button("Get Recommendations", key="get_recommendations_btn"):
    st.session_state.selected_member_id = member_id_input  # Store in session state

# Fetch and display recommendations only when a valid ID is set
if st.session_state.selected_member_id:
    recommendations = get_recommendations(st.session_state.selected_member_id)

    if "recommendations" in recommendations and recommendations["recommendations"]:
        display_recommendations(recommendations)
    else:
        st.warning("⚠️ No recommendations found for this member.")
