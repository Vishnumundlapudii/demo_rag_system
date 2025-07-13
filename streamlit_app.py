import streamlit as st
import os
from rag_backend import LangChainChatbot

# Page configuration
st.set_page_config(
    page_title="LangChain Documentation Chatbot",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .chat-message.bot {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .source-link {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the chatbot"""
    if 'chatbot' not in st.session_state:
        with st.spinner("🚀 Initializing LangChain Documentation Chatbot..."):
            chatbot = LangChainChatbot()
            success = chatbot.initialize()
            if success:
                st.session_state.chatbot = chatbot
                st.success("✅ Chatbot initialized successfully!")
            else:
                st.error("❌ Failed to initialize chatbot. Please check your configuration.")
                return False
    return True

def display_message(message, is_user=True):
    """Display a chat message"""
    message_class = "user" if is_user else "bot"
    icon = "👤" if is_user else "🤖"
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
            <strong>{"You" if is_user else "LangChain Assistant"}</strong>
        </div>
        <div>{message}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.title("🦜 LangChain Documentation Chatbot")
    st.markdown("Ask me anything about LangChain framework and its documentation!")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This chatbot uses RAG (Retrieval-Augmented Generation) to answer questions about LangChain documentation.
        
        **Features:**
        - 💬 Conversational memory
        - 📚 Real-time documentation search
        - 🔗 Source references
        - 🧹 Clear conversation history
        """)
        
        st.header("🛠️ Configuration")
        
        # Environment check
        api_key_status = "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing"
        st.write(f"OpenAI API Key: {api_key_status}")
        
        e2e_endpoint_status = "✅ Configured" if os.getenv("E2E_LLM_ENDPOINT") else "❌ Not configured"
        st.write(f"E2E Endpoint: {e2e_endpoint_status}")
        
        # Clear conversation button
        if st.button("🧹 Clear Conversation", type="secondary"):
            if 'messages' in st.session_state:
                st.session_state.messages = []
            if 'chatbot' in st.session_state:
                st.session_state.chatbot.clear_memory()
            st.rerun()
        
        st.header("💡 Sample Questions")
        sample_questions = [
            "What is LangChain?",
            "How do I create a vector store?",
            "What are document loaders?",
            "How does conversational memory work?",
            "What is the difference between chains and agents?"
        ]
        
        for question in sample_questions:
            if st.button(f"💬 {question}", key=f"sample_{question}"):
                st.session_state.current_question = question

    # Initialize chatbot
    if not initialize_chatbot():
        st.stop()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_msg = """
        👋 Hello! I'm your LangChain Documentation Assistant. 
        
        I can help you with:
        - Understanding LangChain concepts
        - Code examples and implementations
        - Best practices and troubleshooting
        - Component usage and configuration
        
        What would you like to know about LangChain?
        """
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    # Display chat history
    for message in st.session_state.messages:
        display_message(message["content"], message["role"] == "user")

    # Handle sample question click
    if "current_question" in st.session_state:
        prompt = st.session_state.current_question
        del st.session_state.current_question
    else:
        # Chat input
        prompt = st.chat_input("Ask me about LangChain...")

    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message(prompt, True)

        # Get bot response
        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.chatbot.chat(prompt)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                display_message(response, False)
                
                # Show sources
                sources = st.session_state.chatbot.get_sources(prompt)
                if sources:
                    with st.expander("📚 Sources", expanded=False):
                        for i, source in enumerate(sources[:3], 1):
                            st.markdown(f"{i}. [{source['title']}]({source['url']})")
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                display_message(error_msg, False)

        # Rerun to show the new messages
        st.rerun()

if __name__ == "__main__":
    main()