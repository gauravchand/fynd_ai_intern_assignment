import streamlit as st
import pandas as pd
import os
import time
from openai import OpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Fynd AI Feedback System", layout="wide")

# Get API Key from Environment Variable (Secure for Hugging Face)
api_key = os.environ.get("GROQ_API_KEY")

# Fallback: Stop the app if no key is found
if not api_key:
    st.error("API Key not found! Please set the GROQ_API_KEY secret in Hugging Face Settings.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

MODEL_ID = "llama-3.1-8b-instant"
DATA_FILE = "reviews.csv"

# --- 2. DATA HANDLING ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Timestamp", "Stars", "Review", "AI_Response", "AI_Summary", "AI_Action"
        ])

def save_data(new_entry):
    df = load_data()
    new_df = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return df

# --- 3. AI FUNCTIONS ---
def generate_ai_response(review_text, stars):
    prompt = f"""
    You are a customer service representative. 
    Write a short, polite response to a customer who gave a {stars}-star review.
    Review: "{review_text}"
    Keep it empathetic. Max 2 sentences.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def analyze_review_for_admin(review_text, stars):
    prompt = f"""
    Analyze this review (Rating: {stars}/5).
    Review: "{review_text}"
    Return a string with two parts separated by a pipe symbol (|):
    Part 1: A 5-word summary.
    Part 2: Recommended action for admin.
    Format: Summary | Action
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.split("|")
    except Exception as e:
        return ["Error", "Error"]

# --- 4. UI LAYOUT ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["User Dashboard", "Admin Dashboard"])

if page == "User Dashboard":
    st.title("🌟 Submit Your Feedback")
    with st.form("review_form"):
        stars = st.slider("Rating", 1, 5, 5)
        review_text = st.text_area("Your Review")
        submitted = st.form_submit_button("Submit Review")

        if submitted and review_text:
            with st.spinner("Processing..."):
                user_reply = generate_ai_response(review_text, stars)
                analysis = analyze_review_for_admin(review_text, stars)
                if len(analysis) == 2:
                    summary, action = analysis[0].strip(), analysis[1].strip()
                else:
                    summary, action = analysis[0], "Manual review required"

                save_data({
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Stars": stars,
                    "Review": review_text,
                    "AI_Response": user_reply,
                    "AI_Summary": summary,
                    "AI_Action": action
                })
            st.success("Submitted!")
            st.markdown(f"**Response:** {user_reply}")

elif page == "Admin Dashboard":
    st.title("📊 Admin Dashboard")
    df = load_data()
    if not df.empty:
        st.metric("Total Reviews", len(df))
        st.dataframe(df[::-1])
    else:
        st.info("No reviews yet.")
