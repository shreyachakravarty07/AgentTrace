# pages/8_Agent_Orchestration.py

import streamlit as st
from agenttrace.orchestrator import create_agent_chain, run_agent_chain
from agenttrace.logger import setup_logger
import graphviz
import json

logger = setup_logger("AgentTrace.AgentOrchestration")

def main() -> None:
    st.title("Agent Orchestration with Enhanced Workflow")
    st.write("Define a complex task and generate a detailed, JSON-formatted plan with a multi-agent orchestration simulation. You can also edit the prompt template for full control.")

    # Sidebar configuration for orchestration
    st.sidebar.header("Orchestration Settings")
    model_name = st.sidebar.text_input("LLM Model Name (repo id)", value="gpt2")
    max_length = st.sidebar.number_input("Max Output Length", value=100, min_value=50, max_value=1000, step=10)
    task_description = st.sidebar.text_area("Task Description", 
        value="Plan a comprehensive marketing strategy for a new tech product.")
    custom_template = st.sidebar.text_area("Editable Prompt Template", 
        value=(
            "You are an expert AI agent specialized in planning complex tasks.\n"
            "Given the following task, provide a detailed, step-by-step plan in JSON format.\n"
            "Your output must be valid JSON with a key 'plan' containing an array of steps.\n"
            "Each step should be an object with 'step_number', 'description', and 'notes'.\n\n"
            "Task: {task}\n\n"
            "Ensure that your output is strictly in JSON format."
        ),
        height=200
    )

    if st.button("Run Agent Workflow"):
        try:
            chain = create_agent_chain(model_name, max_length, task_description, custom_template)
            result = run_agent_chain(chain, task_description)
            st.markdown("### Generated Plan (JSON):")
            st.json(result)
            logger.info("Agent workflow executed successfully.")
            
            # Enhanced Visualization:
            if isinstance(result, dict) and "plan" in result and isinstance(result["plan"], list):
                dot = graphviz.Digraph(comment="Agent Workflow")
                # Create nodes with detailed labels from each step
                for step in result["plan"]:
                    step_num = step.get("step_number", "N/A")
                    desc = step.get("description", "")
                    notes = step.get("notes", "")
                    label = f"Step {step_num}\n{desc}\nNotes: {notes}"
                    dot.node(str(step_num), label)
                # Connect nodes in sequential order
                steps = result["plan"]
                for i in range(len(steps) - 1):
                    current = steps[i].get("step_number", str(i+1))
                    next_step = steps[i+1].get("step_number", str(i+2))
                    dot.edge(str(current), str(next_step), label="next")
                st.markdown("### Workflow Visualization:")
                st.graphviz_chart(dot)
            else:
                st.info("No structured plan found to visualize. Please check your prompt template and task description.")
        except Exception as e:
            st.error(f"Error running agent workflow: {e}")
            logger.error(f"Error running agent workflow: {e}")

if __name__ == "__main__":
    main()
