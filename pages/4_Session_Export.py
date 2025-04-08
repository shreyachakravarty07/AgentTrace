import streamlit as st
import json
from agenttrace.exporter import export_session
from agenttrace.logger import setup_logger

logger = setup_logger("AgentTrace.SessionExport")

def main() -> None:
    st.title("Session Exporter")
    st.write("Export your entire conversation session with analysis metrics to a JSON file.")

    # Ensure conversation exists in session state
    if "conversation" not in st.session_state:
        st.info("No conversation history found. Please start a conversation first.")
        return

    conversation = st.session_state.conversation

    if st.button("Export Session"):
        session_data = export_session(conversation)
        # Convert the session data to JSON string for download
        json_str = json.dumps(session_data, indent=4)
        st.download_button(
            label="Download Session as JSON",
            data=json_str,
            file_name="agenttrace_session.json",
            mime="application/json"
        )
        logger.info("Session exported successfully.")

if __name__ == "__main__":
    main()
