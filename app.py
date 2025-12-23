import streamlit as st
from chatbot import MedicalChatbot
import time

# Page configuration
st.set_page_config(
    page_title="Medical Q&A Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_chatbot():
    """Load and initialize chatbot (cached)"""
    chatbot = MedicalChatbot()
    return chatbot

def initialize_chatbot(chatbot):
    """Initialize chatbot with progress bar"""
    if not chatbot.is_initialized:
        with st.spinner("Initializing Medical Chatbot... This may take a few minutes on first run."):
            progress_bar = st.progress(0)
            
            # Simulate progress updates
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            chatbot.initialize()
            progress_bar.empty()

def main():
    # Header
    st.markdown('<h1 style="font-size: 2.5rem; color: #2E86AB; text-align: center; margin-bottom: 2rem;">🏥 Medical Q&A Chatbot</h1>', unsafe_allow_html=True)
    
    # Load chatbot
    chatbot = load_chatbot()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This Medical Q&A Chatbot uses the MedQuAD dataset to answer medical questions.
        
        **Features:**
        - Medical entity recognition
        - Semantic search for relevant answers
        - Source attribution
        - Confidence scoring
        """)
        
        st.header("🎨 Theme")
        theme_choice = st.selectbox(
            "Choose theme for better text visibility:",
            ["Auto (System)", "Light", "Dark"]
        )
        
        st.header("🔧 Settings")
        show_entities = st.checkbox("Show Medical Entities", value=True)
        show_similar = st.checkbox("Show Similar Questions", value=False)
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.1)
        
        st.header("⚠️ Disclaimer")
        st.warning("This chatbot provides educational information only. Always consult healthcare professionals for medical advice.")
    
    # Apply theme-based CSS
    if theme_choice == "Dark":
        st.markdown("""
        <style>
        .stMarkdown, .stMarkdown p, .stMarkdown div {
            color: #FFFFFF !important;
        }
        .stChatMessage {
            color: #FFFFFF !important;
        }
        .stInfo {
            background-color: rgba(33, 150, 243, 0.2);
            border: 1px solid #64B5F6;
            color: #FFFFFF !important;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme_choice == "Light":
        st.markdown("""
        <style>
        .stMarkdown, .stMarkdown p, .stMarkdown div {
            color: #000000 !important;
        }
        .stChatMessage {
            color: #000000 !important;
        }
        .stInfo {
            background-color: #E3F2FD;
            border: 1px solid #2196F3;
            color: #1565C0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if not chatbot.is_initialized:
        initialize_chatbot(chatbot)
    
    # Main chat interface
    if chatbot.is_initialized:
        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
                    
                    # Show entities if enabled
                    if show_entities and "entities" in message:
                        entities = message["entities"]
                        if any(entities.values()):
                            st.info("**Identified Medical Terms:**")
                            for entity_type, entity_list in entities.items():
                                if entity_list:
                                    st.write(f"• **{entity_type.title()}:** {', '.join(entity_list)}")
                    
                    # Show confidence and source
                    if "confidence" in message and "source" in message:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Confidence", f"{message['confidence']:.2f}")
                        with col2:
                            st.metric("Source", message['source'])
        
        # Chat input
        user_question = st.chat_input("Ask a medical question...")
        
        if user_question:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_question})
            
            # Get bot response
            with st.spinner("Thinking..."):
                response = chatbot.get_response(user_question)
                
                # Add disclaimer
                final_answer = chatbot.add_disclaimer(response['answer'])
                
                # Add bot message to history
                bot_message = {
                    "role": "assistant",
                    "content": final_answer,
                    "entities": response['entities'],
                    "confidence": response['confidence'],
                    "source": response['source']
                }
                st.session_state.messages.append(bot_message)
            
            # Show similar questions if enabled
            if show_similar:
                similar_questions = chatbot.get_similar_questions(user_question, top_k=3)
                if similar_questions:
                    st.subheader("Similar Questions:")
                    for i, sq in enumerate(similar_questions, 1):
                        with st.expander(f"{i}. {sq['question'][:100]}..."):
                            st.write(f"**Answer:** {sq['answer'][:200]}...")
                            st.write(f"**Confidence:** {sq['score']:.2f}")
            
            st.rerun()
    
    else:
        st.error("Failed to initialize chatbot. Please check your internet connection and try again.")

    # Footer
    st.markdown("---")
    st.markdown("**Data Source:** MedQuAD Dataset | **Built with:** Streamlit, TF-IDF/Sentence Transformers, FAISS")

if __name__ == "__main__":
    main()