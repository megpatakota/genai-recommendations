# app.py
import streamlit as st
import requests

# Replace this with the base URL of your FastAPI service
API_BASE_URL = "http://127.0.0.1:8000"

# Function to fetch recommendations from the API
def get_recommendations_from_api(member_id: str):
    try:
        response = requests.get(f"{API_BASE_URL}/recommendations/{member_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}

# Function to display recommendations in a structured format
def display_recommendations(recommendations):
    st.subheader("🎉 Your Personalised Experiences 🎉")

    for rec in recommendations["recommendations"]:
        with st.container():
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #4CAF50; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin-bottom: 10px;
                    background-colour: #f9f9f9;">
                    <h3 style="colour: #333;">{rec["title"]}</h3>
                    <p><strong>Category:</strong> {rec["category"]} 🏷️</p>
                    <p>{rec["explanation"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Streamlit UI
st.title("🎯 Experience Recommender")
st.subheader("🔎 Discover Your Next Adventure!")

# Store user input in session state
if "selected_member_id" not in st.session_state:
    st.session_state.selected_member_id = ""

member_id_input = st.text_input("Enter Member ID")

if st.button("Get Recommendations", key="get_recommendations_btn"):
    st.session_state.selected_member_id = member_id_input  # Store in session state

# Fetch and display recommendations only when a valid ID is set
if st.session_state.selected_member_id:
    recommendations = get_recommendations_from_api(st.session_state.selected_member_id)

    # Handle error responses or empty recommendations
    if "error" in recommendations:
        st.warning(f"⚠️ {recommendations['error']}")
    elif "recommendations" in recommendations and recommendations["recommendations"]:
        display_recommendations(recommendations)
    else:
        st.warning("⚠️ No recommendations found for this member.")
