# pages/1_Conversation_Manager.py

import streamlit as st
from agenttrace.conversation import Conversation
from agenttrace.logger import setup_logger

logger = setup_logger("AgentTrace.1_Conversation_Manager")

def main() -> None:
    st.title("Conversation Manager")
    st.write("Interact with your LLM in a multi-turn conversation.")

    # Sidebar configuration for model and backend settings
    st.sidebar.header("Configuration")
    model_name = st.sidebar.text_input("Model Name", value="google/gemma-3-1b-it")
    max_length = st.sidebar.number_input("Max Output Length", value=50, min_value=10, max_value=2000, step=10)
    backend_type = st.sidebar.selectbox("Select LLM Backend", options=["huggingface"], index=0)

    # Check if conversation exists and if the model name has changed
    if "conversation" not in st.session_state or st.session_state.conversation.model_name != model_name:
        st.session_state.conversation = Conversation(model_name, max_length, backend_type)
        logger.info(f"Initialized conversation with model '{model_name}', max_length {max_length}, backend '{backend_type}'")
    else:
        # Optionally update max_length if changed
        st.session_state.conversation.max_length = max_length

    # Optionally, add a reset button to clear the conversation manually:
    if st.sidebar.button("Reset Conversation"):
        st.session_state.pop("conversation", None)
        st.success("Conversation reset. Please re-enter settings.")
        st.experimental_rerun()

    # Input for new prompt
    prompt = st.text_input("Enter your prompt:")
    if st.button("Send"):
        if prompt.strip():
            response = st.session_state.conversation.add_turn(prompt)
            st.success("Response generated!")
            st.code(response)
        else:
            st.warning("Please enter a valid prompt.")

    # Display conversation history
    st.subheader("Conversation History")
    history = st.session_state.conversation.get_history()
    if history:
        for idx, turn in enumerate(history):
            st.markdown(f"**Turn {idx + 1}:**")
            st.markdown(f"**Prompt:** {turn['prompt']}")
            st.markdown(f"**Response:** {turn['response']}")
            st.markdown("---")
    else:
        st.info("No conversation history yet.")

if __name__ == "__main__":
    main()
