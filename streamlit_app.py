"""
Streamlit Demo Application for Athena Virtual Assistant

This module provides a simple web interface to interact with the Athena virtual assistant,
demonstrating its capabilities through a user-friendly interface.
"""

import streamlit as st
import json
import requests
from typing import Dict, Any
import config

# Configure the page
st.set_page_config(
    page_title="Athena Virtual Assistant Demo",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #000000;
        color: #ffffff;
    }
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #FF6B6B;
    }
    .response-box {
        background-color: #000000;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #1a1a1a;
        color: #ffffff;
        margin-left: 20%;
        border: 1px solid #333333;
    }
    .assistant-message {
        background-color: #000000;
        color: #ffffff;
        margin-right: 20%;
        border: 1px solid #333333;
    }
    /* Additional styles for dark theme */
    .stMarkdown {
        color: #ffffff;
    }
    .stTextInput > div > div > input::placeholder {
        color: #888888;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 Athena Virtual Assistant Demo")
st.markdown("""
    Welcome to the Athena Virtual Assistant Demo! This interface allows you to interact with Athena
    and experience its capabilities firsthand. Try asking it to:
    - Find hotels or Airbnbs
    - Search for flights or bus tickets
    - Order food or groceries
    - Play music on Spotify
    - Send emails
    - And much more!
""")

# Initialize session state for chat history and input
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# Function to send request to Athena backend
def send_to_athena(query: str) -> Dict[str, Any]:
    """
    Send a query to the Athena backend and get the response.
    
    Args:
        query: The user's input query
        
    Returns:
        Dict: The response from Athena
    """
    try:
        response = requests.post(
            f"http://{config.APP_SETTINGS['HOST']}:{config.APP_SETTINGS['PORT']}/",
            json={"query": query}
        )
        return response.json()
    except Exception as e:
        return {"type": "error", "data": {"message": f"Error connecting to Athena: {str(e)}"}}

# Function to format response for display
def format_response(response: Dict[str, Any]) -> str:
    """
    Format the response from Athena for display in the UI.
    
    Args:
        response: The response from Athena
        
    Returns:
        str: Formatted response string
    """
    if response["type"] == "error":
        return f"❌ Error: {response['data']['message']}"
    elif response["type"] == "text":
        return response["data"]
    else:
        return json.dumps(response["data"], indent=2)

# Create the main interface
st.markdown("### 💬 Chat with Athena")

# Display chat history
for message in st.session_state.chat_history:
    with st.container():
        message_class = "user-message" if message["role"] == "user" else "assistant-message"
        st.markdown(f"""
            <div class="chat-message {message_class}">
                <strong>{'You' if message['role'] == 'user' else 'Athena'}:</strong><br>
                {message['content']}
            </div>
        """, unsafe_allow_html=True)

# Create a form for input
with st.form(key="chat_form"):
    user_input = st.text_input("Type your message here:", key=f"user_input_{st.session_state.input_key}")
    submit_button = st.form_submit_button("Send")

# Handle form submission
if submit_button and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Get response from Athena
    response = send_to_athena(user_input)
    
    # Add Athena's response to chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": format_response(response)
    })
    
    # Increment input key to clear the input
    st.session_state.input_key += 1
    
    # Rerun the app
    st.rerun()

# Sidebar with information
with st.sidebar:
    st.header("About Athena")
    st.markdown("""
        Athena is an open-source AI assistant that can:
        
        - 🏨 Find and book accommodations
        - ✈️ Search for flights and bus tickets
        - 🍽️ Order food and groceries
        - 🎵 Control music playback
        - 📧 Send and read emails
        - 🔍 Search the web for information
        
        Try asking it to help you with any of these tasks!
    """)
    
    st.header("Example Queries")
    st.markdown("""
        Here are some example queries you can try:
        
        1. "Find me an Airbnb in Goa for next weekend"
        2. "Book bus tickets from Mumbai to Pune for tomorrow"
        3. "Order groceries from Zepto - add milk, eggs, and bread"
        4. "Play my favorite playlist on Spotify"
        5. "Send an email to my team about the project deadline"
    """)
    
    st.header("Settings")
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using FastAPI and Streamlit</p>
        <p>Check out the <a href='https://github.com/yourusername/athena'>GitHub repository</a></p>
    </div>
""", unsafe_allow_html=True) 