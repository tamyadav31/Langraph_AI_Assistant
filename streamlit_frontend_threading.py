import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid
import time
from datetime import datetime

# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    thread_name = f"Chat {datetime.now().strftime('%b %d, %H:%M')}"
    add_thread(st.session_state['thread_id'], thread_name)
    st.session_state['message_history'] = []
    
    # Show success message
    st.success("New conversation created!")
    time.sleep(0.5)  # Brief pause to show the message
    st.rerun()  # Refresh to clear the success message

def add_thread(thread_id, name=None):
    if thread_id not in [t['id'] for t in st.session_state['chat_threads']]:
        if name is None:
            name = f"Thread {len(st.session_state['chat_threads']) + 1}"
        
        st.session_state['chat_threads'].append({
            'id': thread_id,
            'name': name,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'messages_count': 0
        })

def load_conversation(thread_id):
    messages = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
    
    # Update message count in thread metadata
    for i, thread in enumerate(st.session_state['chat_threads']):
        if thread['id'] == thread_id:
            st.session_state['chat_threads'][i]['messages_count'] = len(messages)
            break
            
    return messages

def update_thread_name(thread_id, new_name):
    for i, thread in enumerate(st.session_state['chat_threads']):
        if thread['id'] == thread_id:
            st.session_state['chat_threads'][i]['name'] = new_name
            break
            
def delete_thread(thread_id):
    # Remove thread from list
    st.session_state['chat_threads'] = [t for t in st.session_state['chat_threads'] if t['id'] != thread_id]
    
    # If current thread was deleted, create a new one
    if st.session_state['thread_id'] == thread_id:
        reset_chat()
    elif not st.session_state['chat_threads']:  # If all threads were deleted
        reset_chat()
    else:  # Switch to the most recent thread
        st.session_state['thread_id'] = st.session_state['chat_threads'][-1]['id']
        messages = load_conversation(st.session_state['thread_id'])
        
        temp_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})
        
        st.session_state['message_history'] = temp_messages

# **************************************** Session Setup ******************************

# Set page config first (must be the first Streamlit command)
st.set_page_config(
    page_title="LangGraph AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []
    
if 'show_thread_options' not in st.session_state:
    st.session_state['show_thread_options'] = False

if 'rename_thread_id' not in st.session_state:
    st.session_state['rename_thread_id'] = None
    

# Initialize the first thread if none exists
if not st.session_state['chat_threads']:
    thread_name = f"Chat {datetime.now().strftime('%b %d, %H:%M')}"
    add_thread(st.session_state['thread_id'], thread_name)

# **************************************** Custom CSS ********************************

def local_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #f5f7f9;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        .chat-message:hover {
            box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        }
        .chat-message.user {
            background-color: #e6f3ff;
            border-left: 5px solid #2b6cb0;
        }
        .chat-message.assistant {
            background-color: #f0fff4;
            border-left: 5px solid #38a169;
        }
        .message-header {
            font-size: 0.8rem;
            color: #555;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
        }
        .message-content {
            font-size: 1rem;
            line-height: 1.5;
        }
        .sidebar-button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
        .thread-item {
            padding: 0.8rem;
            border-radius: 0.5rem;
            margin-bottom: 0.7rem;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }
        .thread-item:hover {
            background-color: #e9ecef;
            transform: translateY(-2px);
        }
        .app-header {
            text-align: center;
            padding: 1.5rem 0;
            border-bottom: 1px solid #e9ecef;
            margin-bottom: 2rem;
            background: linear-gradient(to right, #4880EC, #019CAD);
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .app-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: white;
            margin-bottom: 0.5rem;
        }
        .app-subtitle {
            font-size: 1rem;
            color: rgba(255,255,255,0.9);
        }
        .stTextInput > div > div > input {
            border-radius: 30px;
            padding: 10px 20px;
            border: 2px solid #e1e4e8;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #4880EC;
            box-shadow: 0 0 0 2px rgba(72,128,236,0.2);
        }
        .stButton > button {
            border-radius: 20px;
            padding: 0.25rem 1rem;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .welcome-message {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            border: 1px dashed #dee2e6;
        }
        .typing-indicator {
            display: inline-block;
            position: relative;
            width: 50px;
            height: 20px;
        }
        .typing-indicator span {
            height: 8px;
            width: 8px;
            float: left;
            margin: 0 1px;
            background-color: #9E9EA1;
            display: block;
            border-radius: 50%;
            opacity: 0.4;
        }
        .typing-indicator span:nth-of-type(1) {
            animation: 1s blink infinite 0.3333s;
        }
        .typing-indicator span:nth-of-type(2) {
            animation: 1s blink infinite 0.6666s;
        }
        .typing-indicator span:nth-of-type(3) {
            animation: 1s blink infinite 0.9999s;
        }
        @keyframes blink {
            50% {
                opacity: 1;
            }
        }
        .chat-container {
            max-height: 70vh;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 20px;
        }
        .message-timestamp {
            font-size: 0.7rem;
            color: #888;
        }
        @media (max-width: 768px) {
            .app-title {
                font-size: 1.8rem;
            }
            .app-subtitle {
                font-size: 0.8rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# **************************************** App Header **********************************

st.markdown("""
<div class='app-header'>
    <div class='app-title'>LangGraph AI Assistant</div>
    <div class='app-subtitle'>Your intelligent chatbot powered by LangGraph and LangChain</div>
</div>
""", unsafe_allow_html=True)

# App info section with collapsible details
with st.expander("ℹ️ About this App"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        This chatbot demonstrates the power of **LangGraph** for creating stateful, conversational AI applications.
        
        **Features:**
        - Multiple conversation threads with persistent memory
        - Streaming responses for better user experience
        - Thread management system with naming and search
        - Modern UI with responsive design
        - Dark/light theme options
        - Built with Streamlit, LangGraph, and LangChain
        
        Start a conversation by typing in the chat input below, or create a new chat thread using the sidebar.
        """)
    with col2:
        st.image("https://python.langchain.com/assets/images/langchain_langgraph-f21a7f6c5d79ae53defb4ba5aadca903.png", width=150)
        st.caption("Powered by LangChain & LangGraph")
        
    st.info("💡 **Tip:** You can manage your conversation threads from the sidebar. Create new ones, rename them, or switch between previous discussions.")

# **************************************** Sidebar UI *********************************

st.sidebar.markdown("""<div style='text-align: center;'>
<h2 style='margin-bottom: 0;'>🤖 LangGraph Chatbot</h2>
</div>""", unsafe_allow_html=True)

# New chat button with icon
if st.sidebar.button('📝 New Chat', key='new_chat_btn', use_container_width=True):
    reset_chat()

# Add a search box for conversations
search_query = st.sidebar.text_input('🔍 Search conversations', placeholder='Search by name...')

# Conversations section
st.sidebar.markdown("""<div style='display: flex; justify-content: space-between; align-items: center;'>
<h3 style='margin-bottom: 0;'>Conversations</h3>
</div>""", unsafe_allow_html=True)

# Display threads with better formatting
for thread in reversed(st.session_state['chat_threads']):
    thread_id = thread['id']
    thread_name = thread['name']
    thread_date = thread['created_at']
    is_active = thread_id == st.session_state['thread_id']
    
    # Filter threads based on search query
    if search_query and search_query.lower() not in thread_name.lower():
        continue
    
    # Container for each thread with selection options
    with st.sidebar.container():
        col1, col2 = st.columns([5, 1])
        
        # Main thread button
        button_style = "background-color: #e6f3ff;" if is_active else ""
        with col1:
            if st.button(f"{thread_name}", key=f"thread_{thread_id}", use_container_width=True):
                st.session_state['thread_id'] = thread_id
                st.session_state['show_thread_options'] = False
                messages = load_conversation(thread_id)

                temp_messages = []
                for msg in messages:
                    if isinstance(msg, HumanMessage):
                        role='user'
                    else:
                        role='assistant'
                    temp_messages.append({'role': role, 'content': msg.content})

                st.session_state['message_history'] = temp_messages
                st.rerun()
                
        # Options button        
        with col2:
            if st.button('⋮', key=f"options_{thread_id}"):
                if st.session_state['show_thread_options'] and st.session_state['rename_thread_id'] == thread_id:
                    st.session_state['show_thread_options'] = False
                    st.session_state['rename_thread_id'] = None
                else:
                    st.session_state['show_thread_options'] = True
                    st.session_state['rename_thread_id'] = thread_id
                st.rerun()
        
        # Show options if this thread is selected for options
        if st.session_state['show_thread_options'] and st.session_state['rename_thread_id'] == thread_id:
            # Rename option
            new_name = st.text_input("New name", value=thread_name, key=f"rename_{thread_id}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save", key=f"save_{thread_id}"):
                    update_thread_name(thread_id, new_name)
                    st.session_state['show_thread_options'] = False
                    st.session_state['rename_thread_id'] = None
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_{thread_id}"):
                    delete_thread(thread_id)
                    st.session_state['show_thread_options'] = False
                    st.session_state['rename_thread_id'] = None
                    st.rerun()
        
        # Show thread info in small text
        st.caption(f"{thread_date} · {thread.get('messages_count', 0)} messages")


# **************************************** Main UI ************************************

# Create a container for the chat messages with proper styling
chat_container = st.container()
with chat_container:
    # Show welcome message if no messages yet
    if not st.session_state['message_history']:
        st.markdown("""
        <div class="welcome-message">
            <h3>👋 Welcome to LangGraph AI Assistant!</h3>
            <p>I'm here to help answer your questions. Start by typing a message below.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show conversation history
    for idx, message in enumerate(st.session_state['message_history']):
        # Generate a timestamp if not present
        if 'timestamp' not in message:
            message['timestamp'] = datetime.now().strftime('%I:%M %p')
            
        with st.chat_message(message['role']):
            # Show user/assistant name and timestamp
            display_name = "You" if message['role'] == 'user' else "Assistant"
            st.markdown(f"<div class='message-header'>{display_name} <span class='message-timestamp'>{message['timestamp']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='message-content'>{message['content']}</div>", unsafe_allow_html=True)

# Add button to clear the conversation
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🗑️ Clear", help="Clear the current conversation"):
        st.session_state['message_history'] = []
        st.rerun()

# Chat input at the bottom
user_input = st.chat_input('Type your message here...')

if user_input:
    # Get current timestamp
    current_time = datetime.now().strftime('%I:%M %p')

    # Add user message to history with timestamp
    st.session_state['message_history'].append({
        'role': 'user', 
        'content': user_input,
        'timestamp': current_time
    })
    
    # Display user message
    with st.chat_message('user'):
        st.markdown(f"<div class='message-header'>You <span class='message-timestamp'>{current_time}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='message-content'>{user_input}</div>", unsafe_allow_html=True)

    # Configure the chat thread
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # Display assistant response with typing indicator
    with st.chat_message('assistant'):
        current_time = datetime.now().strftime('%I:%M %p')
        st.markdown(f"<div class='message-header'>Assistant <span class='message-timestamp'>{current_time}</span></div>", unsafe_allow_html=True)
        
        # Create typing indicator
        typing_indicator = st.empty()
        typing_indicator.markdown("""
        <div class="typing-indicator">  
            <span></span>
            <span></span>
            <span></span>
        </div>
        """, unsafe_allow_html=True)
        
        # Placeholder for the message content
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        ):
            full_response += message_chunk.content
            message_placeholder.markdown(f"<div class='message-content'>{full_response}</div>", unsafe_allow_html=True)
            time.sleep(0.01)  # Small delay for smoother streaming
        
        # Clear the typing indicator when done
        typing_indicator.empty()
        
        # Store the final response
        ai_message = full_response

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})