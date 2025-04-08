"""
Module: agenttrace.analyzer
Provides functions to analyze the output of the LLM for issues such as prompt echoing and excessive repetition.
"""

import re
from difflib import SequenceMatcher
from collections import Counter
from typing import Dict

def analyze_response(prompt: str, response: str) -> Dict[str, float]:
    """
    Analyze the generated response for quality issues.

    Metrics computed:
    - prompt_similarity: similarity ratio between the prompt and the response (values 0-1).
    - echo_flag: 1.0 if the prompt is heavily echoed, else 0.0.
    - repetition_score: fraction of the most common sentence relative to total sentences.

    Args:
        prompt (str): The original prompt.
        response (str): The generated response.

    Returns:
        Dict[str, float]: A dictionary with keys:
            - "prompt_similarity": similarity ratio,
            - "echo_flag": 1.0 if similarity > 0.5, else 0.0,
            - "repetition_score": ratio of the highest sentence frequency.
    """
    # Calculate similarity between prompt and response (in lower case)
    similarity = SequenceMatcher(None, prompt.strip().lower(), response.strip().lower()).ratio()
    echo_flag = 1.0 if similarity > 0.5 else 0.0

    # Split the response into sentences for repetition analysis
    sentences = re.split(r'[.!?]+', response)
    sentences = [s.strip() for s in sentences if s.strip()]
    repetition_score = 0.0
    if sentences:
        counter = Counter(sentences)
        total_sentences = sum(counter.values())
        max_freq = max(counter.values())
        repetition_score = max_freq / total_sentences

    return {
        "prompt_similarity": similarity,
        "echo_flag": echo_flag,
        "repetition_score": repetition_score
    }
