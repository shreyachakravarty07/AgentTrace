import streamlit as st
from agenttrace.conversation import Conversation

def main():
    st.title("Replay Functionality")
    st.write("Replay and modify previous conversation turns.")

    # Ensure conversation exists in session state
    if "conversation" not in st.session_state:
        st.info("No conversation history found. Please start a conversation first.")
        return

    conversation = st.session_state.conversation
    history = conversation.get_history()

    if not history:
        st.info("No conversation history to replay.")
        return

    # Select turn to replay
    turn_indices = list(range(1, len(history) + 1))
    selected_turn = st.selectbox("Select turn to replay:", turn_indices)
    original_prompt = history[selected_turn - 1]["prompt"]
    st.write(f"**Original Prompt:** {original_prompt}")

    # Input for modification
    prompt_modification = st.text_input("Modification to append to the prompt:", value="")
    if st.button("Replay Turn"):
        new_prompt = f"{original_prompt} {prompt_modification}".strip()
        new_response = conversation.replay_turn(selected_turn - 1, prompt_modification)
        st.success("Turn replayed!")
        st.write(f"**New Prompt:** {new_prompt}")
        st.write(f"**New Response:** {new_response}")

if __name__ == "__main__":
    main()
