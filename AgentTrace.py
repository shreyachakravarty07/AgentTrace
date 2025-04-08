import streamlit as st

st.set_page_config(page_title="AgentTrace Dashboard", layout="wide")

st.title("AgentTrace Dashboard")
st.write("Welcome to AgentTrace – a comprehensive debugging and optimization tool for AI agent workflows. Use the cards below to explore each feature.")

# Inject custom CSS for attractive, spaced-out card design
st.markdown("""
<style>
.card {
    background-color: #FAF8F1 !important;  /* Soft cream background */
    color: #333333 !important;            /* Dark text */
    border-radius: 8px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    min-height: 220px;  /* Use min-height for flexibility */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow-wrap: break-word;  /* Ensures words break if too long */
}

.card h3, .card p, .card a {
    overflow-wrap: break-word;  /* Wrap long text in headings, paragraphs, and links */
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}

.card a {
    color: #1f77b4 !important;
    text-decoration: none;
    font-weight: 600;
    font-size: 14px;
}

.card a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ----- First row: 3 cards -----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>Conversation Manager</h3>
        <p>Engage in multi-turn conversations with your LLM. Log and analyze prompts and responses.</p>
        <a href="Conversation_Manager">Open Conversation Manager</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>Replay Functionality</h3>
        <p>Replay and modify previous conversation turns to test prompt variations and debug behavior.</p>
        <a href="Replay_Functionality">Open Replay Functionality</a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>Output Analyzer</h3>
        <p>Analyze token-level metrics to detect issues like prompt echoing and repetition.</p>
        <a href="Output_Analyzer">Open Output Analyzer</a>
    </div>
    """, unsafe_allow_html=True)

# ----- Second row: 3 cards -----
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="card">
        <h3>Prompt Optimization</h3>
        <p>Receive actionable suggestions to refine your prompts for improved responses.</p>
        <a href="Prompt_Optimization_Assistant">Open Prompt Optimization</a>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card">
        <h3>Agent Orchestration</h3>
        <p>Orchestrate multi-agent workflows using LangChain and visualize the reasoning process.</p>
        <a href="Agent_Orchestration">Open Agent Orchestration</a>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="card">
        <h3>Comparative Analysis</h3>
        <p>Compare outputs and chain-of-thought traces from different models to benchmark performance.</p>
        <a href="Comparative_Analysis">Open Comparative Analysis</a>
    </div>
    """, unsafe_allow_html=True)

# ----- Third row: 2 cards -----
col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("""
    <div class="card">
        <h3>Session Export</h3>
        <p>Export your conversation session along with detailed metrics for offline analysis and auditing.</p>
        <a href="Session_Export">Open Session Export</a>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown("""
    <div class="card">
        <h3>Chain-of-Thought Visualization</h3>
        <p>Visualize token-level reasoning and confidence scores behind each decision in your LLM's output.</p>
        <a href="Chain_of_Thought">Open Chain-of-Thought Visualization</a>
    </div>
    """, unsafe_allow_html=True)

# Add spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
