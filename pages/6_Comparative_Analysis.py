# pages/6_Comparative_Analysis.py

import streamlit as st
from difflib import SequenceMatcher
from agenttrace.llm_backend import HuggingFaceBackend
from agenttrace.analyzer import analyze_response

def main() -> None:
    st.title("Comparative Analysis of LLMs")
    st.write("Compare outputs and chain-of-thought traces from two different models for the same prompt.")

    # Sidebar options for configuring models
    st.sidebar.header("Configuration")
    model_name1 = st.sidebar.text_input("Model 1 Name", value="GPT2-large")
    model_name2 = st.sidebar.text_input("Model 2 Name", value="EleutherAI/gpt-neo-125M")
    max_length = st.sidebar.number_input("Max Output Length", value=50, min_value=10, max_value=200, step=10)
    
    # Prompt input for comparison
    prompt = st.text_input("Enter the prompt for comparison:", value="Explain Einstein's theory of relativity in layman's terms.")

    if st.button("Compare Models"):
        # Instantiate two backends for each model
        backend1 = HuggingFaceBackend(model_name1)
        backend2 = HuggingFaceBackend(model_name2)
        
        # Generate outputs with chain-of-thought traces
        output1, trace1 = backend1.generate_with_trace(prompt, max_length)
        output2, trace2 = backend2.generate_with_trace(prompt, max_length)
        
        st.markdown("### Model 1 Output")
        st.code(output1)
        st.markdown("#### Chain-of-Thought (Model 1)")
        st.table(trace1)
        
        st.markdown("### Model 2 Output")
        st.code(output2)
        st.markdown("#### Chain-of-Thought (Model 2)")
        st.table(trace2)
        
        # Compare outputs using SequenceMatcher
        similarity = SequenceMatcher(None, output1, output2).ratio()
        st.markdown("### Output Similarity")
        st.write(f"Similarity Ratio: {similarity:.2f}")

if __name__ == "__main__":
    main()
