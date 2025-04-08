"""
Module: agenttrace.core
Core functions for AgentTrace – a debugging toolkit for AI agent behavior.
This module provides an abstract function to load any LLM using Hugging Face's Transformers pipeline.
"""

import logging
from typing import Any
from transformers import pipeline

def load_llm(model_name: str, prompt: str, max_length: int = 50) -> str:
    """
    Load a large language model and generate text based on the prompt.
    
    Args:
        model_name (str): The identifier of the model (e.g., "distilgpt2" or any supported model).
        prompt (str): The input prompt to generate text from.
        max_length (int): The maximum length of generated output. Defaults to 50.
        
    Returns:
        str: The generated text (chain-of-thought).
    """
    logger = logging.getLogger("AgentTrace.core")
    try:
        logger.info(f"Initializing text generation pipeline for model '{model_name}'")
        generator = pipeline("text-generation", model=model_name)
        logger.info("Pipeline initialized. Generating output...")
        outputs = generator(prompt, max_length=max_length, do_sample=True)
        generated_text = outputs[0]["generated_text"]
        logger.info("Text generated successfully.")
        return generated_text
    except Exception as e:
        logger.error(f"Error generating text from model '{model_name}': {e}")
        return f"Error: {e}"
