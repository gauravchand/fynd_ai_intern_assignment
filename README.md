# 🚀 AI-Powered Customer Feedback System
### Fynd AI Intern - Take Home Assessment

This repository contains the solution for the Fynd AI Intern Assessment. It consists of two main components: an **LLM-based Rating Prediction experiment** (Task 1) and a **Full-Stack AI Feedback Web Application** (Task 2).

---

## 📝 Task 1: Rating Prediction via Prompting

**Objective:** Classify Yelp reviews into 1-5 star ratings using the `llama-3.1-8b-instant` model (via Groq) and strictly output valid JSON.

### Approaches Implemented
1.  **Zero-Shot:** Direct classification without examples.
2.  **Few-Shot:** Provided 3 examples (Negative, Neutral, Positive) to guide the model.
3.  **Chain-of-Thought (CoT):** Forced the model to analyze keywords and tone *before* assigning a rating.

### 📊 Results (Evaluated on 200 Samples)

| Approach | Accuracy | JSON Validity | Key Observation |
| :--- | :--- | :--- | :--- |
| **Zero-Shot** | 60.50% | 100% | Good baseline, but struggles with nuance. |
| **Few-Shot** | **61.50%** | 100% | **Best Performer.** Examples helped calibrate the scale. |
| **Chain-of-Thought** | 60.50% | 100% | Provided rich explanations but similar accuracy to Zero-Shot. |

> **Note:** All approaches achieved **100% valid JSON output** by using `response_format={"type": "json_object"}` and robust system prompts.

---

## 💻 Task 2: Web-Based AI Feedback System

**Objective:** Build a User and Admin dashboard to collect and analyze feedback using LLMs.

### Features
* **Unified Architecture:** Built as a single **Streamlit** app with sidebar navigation to share state easily.
* **User Dashboard:**
    * Star rating slider & text input.
    * **Real-time AI Response:** Generates an empathetic, context-aware reply to the user immediately upon submission.
* **Admin Dashboard:**
    * Live feed of all submitted reviews.
    * **AI Analytics:** Automatically summarizes reviews into 5 words and suggests "Recommended Actions" for the admin.
    * Visual metrics (bar charts, average rating).
* **Tech Stack:** Python, Streamlit, Pandas, Groq API.

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/fynd-ai-assessment.git](https://github.com/your-username/fynd-ai-assessment.git)
cd fynd-ai-assessment
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Set up API key
You need a Groq API key. You can set it in your environment variable.
```bash
export GROQ_API_KEY="your_gsk_key_here"
```
### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deployment

The application is deployed on Hugging Face Spaces.

* **Configuration:** The app reads the GROQ_API_KEY from the Space's Environment Secrets to ensure security.
* **Data Storage:** Uses a local reviews.csv for data persistence.
   * Note: On the free tier, this file resets when the Space restarts.
 
## 👤 Author
* **Gaurav Thakur**
* **Github:** https://github.com/gauravchand
