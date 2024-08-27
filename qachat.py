from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo", layout="wide", initial_sidebar_state="expanded")

# Add custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #1E1E1E;
            color: #E8E8E8;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>input {
            background-color: #333333;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px;
        }
        .chat-history {
            padding: 15px;
            background-color: #2A2A2A;
            border-radius: 8px;
            max-height: 500px;
            overflow-y: scroll;
            color: #FFFFFF;
        }
        .chat-response {
            padding: 15px;
            background-color: #333333;
            border-radius: 8px;
            color: #E8E8E8;
            min-height: 100px;
            transition: opacity 0.5s ease-in-out;
        }
        .response-chunk {
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.header("Chat History")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history on the left side
with st.sidebar:
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

# Input area for user question
st.header("Gemini LLM Application")
input = st.text_input("Ask your question:", key="input")
submit = st.button("Submit")

# Response area on the right side
if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("Response")
    
    response_container = st.empty()
    response_text = ""
    
    for chunk in response:
        response_text += chunk.text
        response_container.markdown(f"<div class='chat-response'>{response_text}</div>", unsafe_allow_html=True)
        st.session_state['chat_history'].append(("Bot", chunk.text))

    # Add a copy button for the response
    if response_text:
        if st.button("Copy to Clipboard"):
            st.write(f"Copied: {response_text}")
            st.session_state['chat_history'].append(("System", "Response copied to clipboard"))

# Include any necessary JS for clipboard functionality
st.markdown("""
    <script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            console.log('Async: Copying to clipboard was successful!');
        }, function(err) {
            console.error('Async: Could not copy text: ', err);
        });
    }
    </script>
""", unsafe_allow_html=True)


