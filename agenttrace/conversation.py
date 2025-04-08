"""
Module: agenttrace.conversation
Manages multi-turn conversation with an LLM using a backend abstraction.
"""

from typing import List, Dict
from agenttrace.llm_backend import HuggingFaceBackend, LLMBackend
from agenttrace.logger import setup_logger

logger = setup_logger("AgentTrace.conversation")

class Conversation:
    """
    Manages a multi-turn conversation with an LLM.
    """
    def __init__(self, model_name: str, max_length: int = 50, backend_type: str = "huggingface") -> None:
        self.model_name = model_name
        self.max_length = max_length
        self.history: List[Dict[str, str]] = []  # List of turns
        # Instantiate backend based on type
        if backend_type.lower() == "huggingface":
            self.backend: LLMBackend = HuggingFaceBackend(model_name)
        else:
            raise ValueError(f"Unsupported backend type: {backend_type}")
        logger.info(f"Conversation initialized using backend '{backend_type}' with model '{model_name}'.")

    def add_turn(self, prompt: str) -> str:
        """
        Adds a turn by generating a response using the selected backend.
        """
        response = self.backend.generate(prompt, self.max_length)
        self.history.append({"prompt": prompt, "response": response})
        logger.info(f"Turn added. Prompt: {prompt} | Response: {response}")
        return response

    def get_history(self) -> List[Dict[str, str]]:
        """
        Returns the conversation history.
        """
        return self.history

    def replay_turn(self, index: int, prompt_modification: str = "") -> str:
        """
        Replays a specific conversation turn with an optional prompt modification.
        """
        if index < 0 or index >= len(self.history):
            raise IndexError("Invalid conversation turn index.")
        original_prompt = self.history[index]["prompt"]
        new_prompt = f"{original_prompt} {prompt_modification}".strip() if prompt_modification else original_prompt
        new_response = self.backend.generate(new_prompt, self.max_length)
        logger.info(f"Replayed turn {index + 1} with modification '{prompt_modification}'. New response: {new_response}")
        return new_response
