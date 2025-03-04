import streamlit as st
import requests
import io
import contextlib
import time

# Replace with your actual Google API Key from AI Studio
GOOGLE_API_KEY = "AIzaSyAFma3e4utEGL9ot8OkiJqqSiLlIM6WsQw"
MODEL_NAME = "gemini-1.5-pro"

st.set_page_config(page_title="My Compiler", page_icon="✨", layout="wide")

# Custom CSS for Futuristic UI
st.markdown("""
    <style>
        body {
            background-color: #0D1117;
            color: #E6EDF3;
        }
        .stApp {
            background: rgba(13, 17, 23, 0.95);
            border-radius: 15px;
            padding: 20px;
        }
        .stButton > button {
            background: linear-gradient(45deg, #ff8c00, #ff0080);
            color: white;
            border-radius: 10px;
            font-size: 16px;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0px 0px 15px rgba(255, 140, 0, 0.6);
        }
        .center-text {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #ff8c00;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("https://i.imgur.com/4M7IWwP.png", width=100)

languages = {
    "Python": "python3",
    "JavaScript": "nodejs",
    "Java": "java",
    "C++": "cpp17",
    "C#": "csharp",
    "Go": "go",
    "Ruby": "ruby",
    "Swift": "swift",
    "Kotlin": "kotlin",
    "Rust": "rust"
}

def query_gemini(prompt):
    """Generates a response using Google's Gemini 1.5 Pro API."""
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "⚠️ No valid output received from Gemini."
    else:
        return f"⚠️ API Error: {response.json()}"

# Sidebar Navigation
with st.sidebar:
    menu_option = st.radio("Navigation", ["🏠 Dashboard", "💻 Code Generator", "⚡ My Compiler", "🧠 Learn With AI", "🏆 Challenges"])

if menu_option == "🏠 Dashboard":
    st.markdown("<div class='center-text'>👋 Welcome to My Compiler!</div>", unsafe_allow_html=True)
    st.write("Your AI-powered coding assistant!")

elif menu_option == "💻 Code Generator":
    st.header("💻 AI-Powered Code Generator")
    code_description = st.text_area("Enter your code description:", placeholder="E.g., 'Create a function that calculates the factorial of a number.'")
    language = st.selectbox("Select Programming Language:", list(languages.keys()), index=0)

    if st.button("✨ Generate Code"):
        if not code_description.strip():
            st.error("❌ Please enter a valid description!")
        else:
            with st.spinner("Generating code with AI... ⏳"):
                generated_code = query_gemini(f"Generate a {language} function for: {code_description}")
            st.success(f"✅ Code generated successfully in {language}!")
            st.code(generated_code, language=language.lower())

elif menu_option == "⚡ My Compiler":
    st.header("⚡ My Compiler")
    selected_language = st.selectbox("Choose Language:", list(languages.keys()), index=0)
    code_input = st.text_area(f"Enter {selected_language} Code:", height=300, placeholder=f"Write your {selected_language} code here...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Run Code"):
            if code_input.strip():
                with st.spinner("Running code... ⏳"):
                    try:
                        exec_output = io.StringIO()
                        with contextlib.redirect_stdout(exec_output):
                            exec(code_input)
                        output = exec_output.getvalue()
                    except Exception as e:
                        output = str(e)
                st.markdown("### Output:")
                st.code(output, language="bash")
            else:
                st.error("❌ Please enter some code to execute!")
    
    with col2:
        if st.button("🧠 Explain"):
            with st.spinner("Analyzing code... ⏳"):
                explanation = query_gemini(f"Explain the following {selected_language} code in simple terms: {code_input}")
            st.subheader("Code Explanation:")
            st.write(explanation)

elif menu_option == "🧠 Learn With AI":
    st.header("🧠 AI Chat Panel")
    user_input = st.text_area("Chat with AI:", height=200, placeholder="Ask me anything about your code...")
    if st.button("💬 Send"):
        with st.spinner("Thinking... ⏳"):
            response = query_gemini(user_input)
        st.subheader("AI Response:")
        st.write(response)

elif menu_option == "🏆 Challenges":
    st.header("🏆 Coding Challenges")
    challenge_level = st.selectbox("Select Difficulty Level:", ["Easy", "Medium", "Hard"])
    challenges = {
        "Easy": "Write a function to check if a number is even or odd.",
        "Medium": "Write a function to find the second largest element in an array.",
        "Hard": "Implement a function to check if a given string is a valid palindrome, ignoring spaces and punctuation."
    }
    st.write(f"### Challenge: {challenges[challenge_level]}")
    user_solution = st.text_area("Write your solution:", height=200, placeholder="Enter your code here...")
    
    if st.button("💡 Get AI Hint"):
        hint = query_gemini(f"Give me a hint for solving this problem: {challenges[challenge_level]}")
        st.subheader("Hint:")
        st.write(hint)
    
    if st.button("✅ Submit Solution"):
        with st.spinner("Evaluating your solution... ⏳"):
            evaluation_prompt = f"Evaluate the following code for correctness and suggest improvements if needed. If correct, congratulate the user.\n\nProblem: {challenges[challenge_level]}\n\nUser's Solution:\n{user_solution}"
            evaluation = query_gemini(evaluation_prompt)
        st.subheader("AI Evaluation:")
        st.write(evaluation)

