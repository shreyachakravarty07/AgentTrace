# pages/5_Chain_of_Thought.py

import streamlit as st
from agenttrace.conversation import Conversation
from agenttrace.logger import setup_logger
import torch

logger = setup_logger("AgentTrace.ChainOfThought")

def main() -> None:
    st.title("Chain-of-Thought Visualization")
    st.write("Generate text with detailed token-level chain-of-thought and confidence scores.")

    # Sidebar configuration for model and backend settings
    st.sidebar.header("Configuration")
    model_name = st.sidebar.text_input("Model Name", value="GPT2-large")
    max_length = st.sidebar.number_input("Max Output Length", value=50, min_value=10, max_value=2000, step=10)
    backend_type = st.sidebar.selectbox("Select LLM Backend", options=["huggingface"], index=0)

    # Initialize conversation in session state if not present
    if "conversation" not in st.session_state:
        st.session_state.conversation = Conversation(model_name, max_length, backend_type)
    
    st.subheader("Enter Prompt for Chain-of-Thought")
    prompt = st.text_input("Prompt:", value="Explain Einstein's theory of relativity in layman's terms.")
    
    if st.button("Generate with Trace"):
        try:
            # Directly call the backend's generate_with_trace method
            generated_text, trace_info = st.session_state.conversation.backend.generate_with_trace(prompt, max_length)
            st.markdown("### Generated Text:")
            st.code(generated_text)
            st.markdown("### Chain-of-Thought Trace:")
            st.table(trace_info)
            logger.info("Chain-of-thought generated successfully.")
        except Exception as e:
            st.error(f"Error during generation with trace: {e}")

if __name__ == "__main__":
    main()
