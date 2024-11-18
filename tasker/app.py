import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyCCgacf_uGLzl8PEnZR8knlvkrsPc_of90")
llm = genai.GenerativeModel("models/gemini-1.5-flash")
code_review_bot = llm.start_chat(history=[])

# Set up Streamlit page configuration
st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🤖",
    layout="centered",
)

# Define custom CSS for improved styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 3rem;
        color: #ff6f61;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #444444;
        text-align: center;
        margin-bottom: 30px;
    }
    .sidebar-content {
        font-size: 1rem;
        color: #2e4053;
        line-height: 1.6;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #b0b0b0;
        margin-top: 50px;
        padding: 20px 0;
        border-top: 1px solid #ddd;
        background-color: #f7f7f7;
    }
    .chat-container {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .chat-human {
        color: #1e8449;
        background-color: #f0f0f0;
        border-radius: 8px;
        padding: 10px;
    }
    .chat-ai {
        color: #0e6251;
        background-color: #d1f2eb;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page header
st.markdown(
    """
    <div>
        <h1 class="main-title">🤖 AI Code Review Assistant🤖</h1>
        <p class="sub-title">Your AI-powered partner for code analysis and bug fixes</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar content
with st.sidebar:
    st.header("Welcome! 👋")
    st.markdown(
        """
        <div class="sidebar-content">
        This tool helps you to:
        - 🐛 Detect and fix bugs in your code.
        - 🚀 Optimize and improve your code structure.
        - 💡 Learn better coding practices with AI guidance.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("#### 💻 Supported Languages:")
    st.write("- Python\n- Java\n- C\n- C++")
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Code-icon.svg/120px-Code-icon.svg.png",
        width=140,
    )

# Separator line
st.markdown("---")

# Language selection dropdown
language = st.selectbox(
    "🌐 Select Programming Language:",
    ["Python", "Java", "C", "C++"],
    help="Choose the language of your code for review.",
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "text": (
                "Hello! Paste your code below, and I'll help review it for bugs and suggest improvements."
            ),
        }
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "ai":
        st.markdown(f'<div class="chat-container chat-ai">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container chat-human">{message["text"]}</div>', unsafe_allow_html=True)

# Code input area
st.markdown(f"### ✏️ Paste Your {language} Code Below:")
code = st.text_area(f"Enter your {language} code here:", height=200, placeholder="Write or paste your code...")

# Handle code submission
if st.button("🚀 Submit Code for Review"):
    if not code.strip():
        st.error("❌ Please provide your code before submitting.")
    else:
        # Display user input in chat
        st.session_state.messages.append({"role": "human", "text": code})
        st.markdown(f'<div class="chat-container chat-human">{code}</div>', unsafe_allow_html=True)

        with st.spinner("🧠 Analyzing your code..."):
            try:
                # Prepare prompt for AI model
                prompt = f"Review the following {language} code for potential bugs and provide suggestions:\n\n{code}"
                response = code_review_bot.send_message(prompt)

                # Display AI's response
                st.session_state.messages.append({"role": "ai", "text": response.text})
                st.markdown(f'<div class="chat-container chat-ai">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

# Footer with developer attribution
st.markdown(
    """
    <div class="footer">
        <p>Developed with ❤️ by Yashwanth Kumar</p>
    </div>
    """,
    unsafe_allow_html=True,
)
