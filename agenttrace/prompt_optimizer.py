"""
Module: agenttrace.prompt_optimizer
Provides a prompt optimization assistant that analyzes a conversation turn
and suggests improvements based on output analysis.
"""

from typing import Dict
from agenttrace.analyzer import analyze_response

def optimize_prompt(prompt: str, response: str) -> Dict[str, str]:
    """
    Analyze the prompt and its corresponding response to suggest improvements.

    Heuristics:
      - High prompt similarity indicates the model may be echoing the prompt;
        suggest rephrasing or adding details.
      - High repetition score suggests repetitive output; recommend more constraints
        or more specific instructions.

    Args:
        prompt (str): The original prompt.
        response (str): The generated response.

    Returns:
        Dict[str, str]: A dictionary containing a suggestion.
    """
    analysis = analyze_response(prompt, response)
    suggestion = "Your prompt appears to be working well."
    
    if analysis["prompt_similarity"] > 0.7:
        suggestion = ("The response is very similar to your prompt. "
                      "Consider rephrasing your prompt or adding more specific details "
                      "to encourage a more diverse output.")
    elif analysis["repetition_score"] > 0.6:
        suggestion = ("The output seems repetitive. Try modifying the prompt to include "
                      "constraints or ask for more variety in the response.")

    return {"suggestion": suggestion}
