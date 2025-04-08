import streamlit as st
from agenttrace.analyzer import analyze_response

def main():
    st.title("Output Analyzer")
    st.write("Analyze the quality of the latest LLM response.")

    # Ensure conversation exists in session state
    if "conversation" not in st.session_state:
        st.info("No conversation history found. Please start a conversation first.")
        return

    conversation = st.session_state.conversation
    history = conversation.get_history()

    if not history:
        st.info("No conversation history to analyze.")
        return

    # Analyze the last turn
    last_turn = history[-1]
    prompt = last_turn["prompt"]
    response = last_turn["response"]

    st.subheader("Last Turn")
    st.write(f"**Prompt:** {prompt}")
    st.write(f"**Response:** {response}")

    if st.button("Analyze Last Turn"):
        analysis = analyze_response(prompt, response)
        st.subheader("Analysis Results")
        st.write(f"**Prompt Similarity:** {analysis['prompt_similarity']:.2f}")
        st.write(f"**Echo Flag:** {'Yes' if analysis['echo_flag'] else 'No'}")
        st.write(f"**Repetition Score:** {analysis['repetition_score']:.2f}")

if __name__ == "__main__":
    main()
