# AgentTrace

**AgentTrace** is a comprehensive debugging and optimization toolkit designed for AI agent workflows. It combines multiple advanced features—ranging from multi-turn conversation management and output analysis to agent orchestration and comparative analysis—to help developers understand, fine-tune, and enhance the behavior of large language models (LLMs).

AgentTrace is built with modularity and best coding practices in mind and leverages modern tools like Streamlit, LangChain, Transformers, and Graphviz to provide a robust, industry-grade platform.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
  - [Conversation Manager](#conversation-manager)
  - [Replay Functionality](#replay-functionality)
  - [Output Analyzer](#output-analyzer)
  - [Session Exporter](#session-exporter)
  - [Chain-of-Thought Visualization](#chain-of-thought-visualization)
  - [Comparative Analysis](#comparative-analysis)
  - [Prompt Optimization Assistant](#prompt-optimization-assistant)
  - [Agent Orchestration](#agent-orchestration)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview

AgentTrace is designed to help developers debug and optimize the internal reasoning (chain-of-thought) of AI agents. By combining multiple features—such as multi-turn conversation logging, replay functionality, output analysis, and advanced orchestration using LangChain—AgentTrace provides:
- **In-depth insights** into LLM behavior (token-level traces, confidence scores, and analysis metrics)
- **Interactive tools** for prompt optimization and performance comparison
- **Flexible architecture** that allows easy switching between different LLM backends

---

## Project Structure

```
agenttrace/
├── agenttrace/
│   ├── __init__.py
│   ├── core.py                # Core functions to load and generate LLM outputs.
│   ├── conversation.py        # Manages multi-turn conversation, storing prompts/responses.
│   ├── logger.py              # Logging setup for consistent, debug-friendly output.
│   ├── analyzer.py            # Analyzes outputs for prompt echo, repetition, etc.
│   ├── orchestrator.py        # Uses LangChain to create and run agent orchestration workflows.
│   ├── prompt_optimizer.py    # Provides suggestions to improve prompts based on analysis.
│   └── exporter.py            # Exports session data (conversation history & metrics) as JSON.
│
├── pages/                     # Multipage dashboard for different features.
│   ├── 1_Conversation_Manager.py
│   ├── 2_Replay_Functionality.py
│   ├── 3_Output_Analyzer.py
│   ├── 4_Session_Export.py
│   ├── 5_Chain_of_Thought.py       # (If implemented, for detailed token-level trace visualization.)
│   ├── 6_Comparative_Analysis.py
│   ├── 7_Prompt_Optimization.py
│   └── 8_Agent_Orchestration.py
│
└── streamlit_app.py         # Main landing page for the multipage dashboard.
```

Each module is designed to be modular and extendable, enabling you to integrate additional functionalities or switch out components as needed.

---

## Features

### Conversation Manager

- **Purpose:**  
  Engage in multi-turn conversations with an LLM. Each turn (prompt/response pair) is logged to form a complete chain-of-thought.
  
- **How It Works:**  
  Uses a dedicated `Conversation` class to store turns. It leverages our LLM backend abstraction (currently via HuggingFace) for generating responses.

---

### Replay Functionality

- **Purpose:**  
  Allows you to replay and modify previous conversation turns. This is valuable for testing different prompt variations and understanding model behavior.
  
- **How It Works:**  
  The `replay_turn` method in `conversation.py` re-runs a selected turn with an optional modification appended to the original prompt.

---

### Output Analyzer

- **Purpose:**  
  Analyzes the LLM output for issues like excessive prompt echoing and repetition, by computing token-level metrics (e.g., similarity ratio, repetition score).
  
- **How It Works:**  
  The `analyze_response` function in `analyzer.py` returns key metrics that help identify potential issues in the generated output.

---

### Session Exporter

- **Purpose:**  
  Export your entire conversation session—including each turn and analysis metrics—into a JSON file for offline review, debugging, or auditing.
  
- **How It Works:**  
  The `export_session` and `export_session_to_json` functions in `exporter.py` package all session data into a structured JSON object.

---

### Chain-of-Thought Visualization

- **Purpose:**  
  Provides a detailed, token-level visualization of the model’s reasoning process. This includes the generated tokens along with their confidence scores.
  
- **How It Works:**  
  By extending the LLM backend to include a `generate_with_trace` method, the system captures detailed trace information. This can be visualized using Graphviz on a dedicated dashboard page.

---

### Comparative Analysis

- **Purpose:**  
  Compare outputs and chain-of-thought traces from two different models or configurations. This is useful for benchmarking and diagnosing differences in model behavior.
  
- **How It Works:**  
  A dedicated dashboard page lets you input two model names and a prompt. It then runs both models, displays their outputs, token traces, and calculates a similarity metric.

---

### Prompt Optimization Assistant

- **Purpose:**  
  Offers actionable suggestions to refine your prompts, based on an analysis of output metrics (e.g., prompt similarity, repetition).
  
- **How It Works:**  
  The `optimize_prompt` function in `prompt_optimizer.py` analyzes a prompt/response pair and returns recommendations for improvement, helping you iterate more effectively.

---

### Agent Orchestration

- **Purpose:**  
  Simulate multi-agent workflows using LangChain. Generate detailed, JSON-formatted plans for complex tasks, and visualize the workflow in an interactive graph.
  
- **How It Works:**  
  The `orchestrator.py` module builds an `LLMChain` with an editable prompt template. It instructs the model to output a structured JSON plan, which is then parsed and visualized using Graphviz.

---

## Installation & Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/agenttrace.git
   cd agenttrace
   ```

2. **Create a Virtual Environment (Using Python 3.11.9):**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   **Dependencies include:**
   - streamlit
   - transformers
   - torch
   - langchain
   - langchain_huggingface
   - graphviz
   - (other utilities as needed)

4. **Run the Dashboard:**

   ```bash
   streamlit run streamlit_app.py
   ```

---

## Usage

- **Landing Page:**  
  The main landing page provides a modern, card-based UI that lists all the key features. Click on any feature card to navigate to its dedicated page.

- **Feature Pages:**  
  Each feature (Conversation Manager, Replay Functionality, Output Analyzer, etc.) has its own page under the `pages/` directory. These pages allow you to interact with the corresponding functionality, view logs, visualize outputs, and export sessions.

- **Configuration:**  
  Use the sidebar to select models, adjust parameters (like maximum output length), and even edit prompt templates for agent orchestration. The system is designed to be modular and configurable.

---

## Troubleshooting

- **Model Not Updating:**  
  If the model name is changed in the sidebar but the system uses the old model, ensure you reset the conversation (or use the reset button) to reinitialize the session state.

- **Output Parsing Errors:**  
  If the output isn’t valid JSON (especially in the Agent Orchestration feature), check your prompt template and consider using an instruction-tuned model or increasing `max_length`.

- **Async and Torch Errors in WSL:**  
  Add the following snippet at the top of your main file to force an event loop:
  ```python
  import asyncio
  try:
      asyncio.get_running_loop()
  except RuntimeError:
      asyncio.set_event_loop(asyncio.new_event_loop())
  ```
  Also, ensure you have the latest versions of PyTorch, Streamlit, and LangChain.

- **Performance:**  
  With limited hardware (e.g., GTX 1650 with 4 GB VRAM), consider using smaller or quantized models for better performance.

---

## Future Enhancements

- **Enhanced Chain-of-Thought Graphs:**  
  Develop interactive, dynamic visualizations that display the entire token-level reasoning process.
- **Multi-Agent Orchestration:**  
  Extend the orchestration functionality to simulate interactions between multiple specialized agents.
- **Auto-Tuning and Feedback Loop:**  
  Integrate mechanisms that automatically adjust sampling parameters based on output analysis across multiple turns.
- **Support for Additional Backends:**  
  Add support for additional LLM backends (e.g., llama.cpp, GPT4All) to improve flexibility and performance.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*AgentTrace* aims to provide an all-in-one platform for AI agent debugging, prompt optimization, and workflow orchestration. By combining multiple advanced features with a clean, modern UI, it empowers developers to build more reliable and efficient AI systems.

For any questions or contributions, please open an issue or submit a pull request on GitHub.
