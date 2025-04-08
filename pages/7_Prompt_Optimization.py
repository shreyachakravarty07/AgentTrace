# pages/7_Prompt_Optimization.py

import streamlit as st
from agenttrace.conversation import Conversation
from agenttrace.prompt_optimizer import optimize_prompt

def main() -> None:
    st.title("Prompt Optimization Assistant")
    st.write("Analyze a conversation turn and receive suggestions to improve your prompt for better responses.")

    # Ensure a conversation exists
    if "conversation" not in st.session_state:
        st.info("No conversation history found. Please start a conversation first.")
        return

    conversation = st.session_state.conversation
    history = conversation.get_history()

    if not history:
        st.info("No conversation turns available. Please generate some turns first.")
        return

    # Select a conversation turn for analysis
    st.subheader("Select a Turn for Optimization")
    turn_number = st.selectbox("Choose Turn", options=range(1, len(history) + 1), format_func=lambda x: f"Turn {x}")
    selected_turn = history[turn_number - 1]

    st.markdown("**Prompt:**")
    st.write(selected_turn["prompt"])
    st.markdown("**Response:**")
    st.write(selected_turn["response"])

    if st.button("Get Optimization Suggestion"):
        suggestion_dict = optimize_prompt(selected_turn["prompt"], selected_turn["response"])
        st.markdown("### Suggestion:")
        st.write(suggestion_dict["suggestion"])

if __name__ == "__main__":
    main()
