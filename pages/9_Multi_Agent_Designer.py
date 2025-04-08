import streamlit as st
import graphviz
import json
import torch
from collections import defaultdict, deque
from agenttrace.orchestrator import create_agent_chain, run_agent_chain
from agenttrace.logger import setup_logger
import gc


logger = setup_logger("AgentTrace.MultiAgentDesigner")

def topological_sort(agents, dependencies):
    """
    Compute a topological order for the agent graph.
    If an agent has multiple upstream inputs, its input will be the concatenation of all outputs.
    """
    graph = defaultdict(list)
    indegree = {agent['id']: 0 for agent in agents}
    
    for src, tgt in dependencies:
        graph[src].append(tgt)
        indegree[tgt] += 1
    
    # Initialize queue with agents having no incoming edges.
    queue = deque([aid for aid in indegree if indegree[aid] == 0])
    order = []
    while queue:
        aid = queue.popleft()
        order.append(aid)
        for neighbor in graph[aid]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != len(agents):
        raise ValueError("Cycle detected or missing agents in dependencies!")
    
    return order, graph

def run_workflow(agents, dependencies, global_task):
    """
    Run agents in topological order. For agents with multiple inputs,
    concatenate their upstream outputs (separated by newlines).
    Returns a dict mapping agent id to its output.
    Each agent uses its own max_length parameter.
    Explicitly deallocates GPU memory after each agent run.
    """
    order, graph = topological_sort(agents, dependencies)
    outputs = {}
    # Build a lookup dictionary for agents by id
    agent_dict = {agent["id"]: agent for agent in agents}
    
    for aid in order:
        # Determine input for current agent: either global task or concatenated outputs.
        upstream_outputs = [outputs[src] for src, tgt in dependencies if tgt == aid]
        input_text = "\n".join(upstream_outputs) if upstream_outputs else global_task
        
        agent = agent_dict[aid]
        st.write(f"**Running {agent['name']} (ID: {aid})**")
        try:
            chain = create_agent_chain(
                model_name=agent["model_name"],
                max_length=agent["max_length"],
                task_description=global_task,
                custom_template=agent["prompt_template"]
            )
            result = run_agent_chain(chain, input_text)
            outputs[aid] = json.dumps(result) if isinstance(result, dict) else str(result)
            # Deallocate GPU memory after each agent run
            # del chain
            # gc.collect()
            # torch.cuda.empty_cache()
        except Exception as e:
            outputs[aid] = f"Error: {e}"
            st.error(f"Error in {agent['name']}: {e}")
            logger.error(f"Error in agent {agent['name']}: {e}")
            break
    return outputs

def visualize_workflow(agents, dependencies):
    dot = graphviz.Digraph(comment="Multi-Agent Workflow")
    for agent in agents:
        dot.node(str(agent["id"]), f"{agent['name']}\n(Model: {agent['model_name']})")
    for src, tgt in dependencies:
        dot.edge(str(src), str(tgt), label="feeds into")
    return dot

def main():
    st.title("Multi-Agent Designer")
    st.write(
        "Design a custom multi-agent workflow by adding agents, defining their roles, and specifying how they interact. "
        "You can create a non-linear (branching) structure where multiple agents perform tasks independently, and their outputs "
        "can be merged and fed into a final agent. Only one agent runs at a time to suit memory constraints."
    )
    
    # Sidebar: Global Workflow Settings
    st.sidebar.header("Global Task Settings")
    global_task = st.sidebar.text_area("Overall Task Description", 
                                       value="Plan a comprehensive marketing strategy for a new tech product.")
    global_max_length = st.sidebar.number_input("Global Max Output Length (fallback)", value=100, min_value=50, max_value=3000, step=10)
    
    # Sidebar: Add Agent
    st.sidebar.header("Add Agent")
    with st.sidebar.form(key="agent_form"):
        agent_id = st.text_input("Agent ID", value="A1")
        agent_name = st.text_input("Agent Name", value="Agent 1")
        model_name = st.text_input("LLM Model Name", value="google/gemma-3-1b-it")
        prompt_template = st.text_area(
            "Agent Prompt Template (use {task} as placeholder)",
            value=(
                "You are an expert agent for a specific task.\n"
                "Given the task: {task}\n"
                "Generate a detailed plan in JSON format with keys 'step_number', 'description', and 'notes'."
            )
        )
        agent_max_length = st.number_input("Agent Max Output Length", value=100, min_value=50, max_value=3000, step=10)
        add_agent = st.form_submit_button(label="Add Agent")
    
    if "agents" not in st.session_state:
        st.session_state.agents = []
    if add_agent:
        agent = {
            "id": agent_id.strip(),
            "name": agent_name.strip(),
            "model_name": model_name.strip(),
            "prompt_template": prompt_template,
            "max_length": agent_max_length
        }
        st.session_state.agents.append(agent)
        st.success(f"Added {agent_name}!")
        logger.info(f"Added agent: {agent}")
    
    # Sidebar: Define Dependencies using dropdowns
    st.sidebar.header("Define Dependencies")
    if "dependencies" not in st.session_state:
        st.session_state.dependencies = []
    
    if st.session_state.agents:
        agent_ids = [agent["id"] for agent in st.session_state.agents]
        with st.sidebar.form(key="dependency_form"):
            dep_source = st.selectbox("Source Agent ID", options=agent_ids, key="dep_source")
            dep_target = st.selectbox("Target Agent ID", options=agent_ids, key="dep_target")
            add_dependency_btn = st.form_submit_button(label="Add Dependency")
        if add_dependency_btn:
            if dep_source == dep_target:
                st.warning("Source and target cannot be the same agent.")
            else:
                st.session_state.dependencies.append((dep_source.strip(), dep_target.strip()))
                st.success(f"Added dependency: {dep_source} -> {dep_target}")
    else:
        st.sidebar.info("Add agents first to define dependencies.")
    
    st.subheader("Defined Agents")
    if st.session_state.agents:
        for agent in st.session_state.agents:
            st.markdown(f"**ID: {agent['id']} | Name: {agent['name']}**")
            st.markdown(f"- **Model:** {agent['model_name']}")
            st.markdown(f"- **Max Output Length:** {agent['max_length']}")
            st.markdown("**Prompt Template:**")
            st.code(agent['prompt_template'])
    else:
        st.info("No agents defined yet. Use the sidebar to add agents.")
    
    st.subheader("Defined Dependencies")
    if st.session_state.dependencies:
        for dep in st.session_state.dependencies:
            st.markdown(f"- **{dep[0]} -> {dep[1]}**")
    else:
        st.info("No dependencies defined yet. Add dependencies to connect agents.")
    
    # Button: Run Workflow
    if st.button("Run Multi-Agent Workflow"):
        if not st.session_state.agents:
            st.error("No agents defined!")
        else:
            with st.spinner("Running workflow..."):
                outputs = run_workflow(
                    agents=st.session_state.agents,
                    dependencies=st.session_state.dependencies,
                    global_task=global_task
                )
            st.markdown("### Workflow Results")
            for agent_id, output in outputs.items():
                st.markdown(f"**Agent {agent_id} Output:**")
                st.code(output)
            # Visualize the workflow using Graphviz
            dot = visualize_workflow(st.session_state.agents, st.session_state.dependencies)
            st.markdown("### Workflow Visualization")
            st.graphviz_chart(dot)
    
    # Reset Button
    if st.button("Reset Multi-Agent Workflow"):
        st.session_state.agents = []
        st.session_state.dependencies = []
        st.success("Multi-agent workflow reset.")
        st.experimental_rerun()

if __name__ == "__main__":
    main()