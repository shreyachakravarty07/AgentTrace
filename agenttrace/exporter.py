"""
Module: agenttrace.exporter
Exports the conversation session along with analysis metrics to a JSON structure.
"""

import json
from typing import Dict, Any, List
from agenttrace.conversation import Conversation
from agenttrace.analyzer import analyze_response
import time

def export_session(conversation: Conversation) -> Dict[str, Any]:
    """
    Export the conversation history along with analysis metrics for each turn.
    
    Returns:
        A dictionary representing the session data.
    """
    session_data: Dict[str, Any] = {
        "exported_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_name": conversation.model_name,
        "max_length": conversation.max_length,
        "turns": []
    }
    
    for turn in conversation.get_history():
        # Analyze each turn response
        analysis = analyze_response(turn["prompt"], turn["response"])
        turn_data = {
            "prompt": turn["prompt"],
            "response": turn["response"],
            "analysis": analysis
        }
        session_data["turns"].append(turn_data)
    
    return session_data

def export_session_to_json(conversation: Conversation, file_path: str) -> None:
    """
    Export the conversation session to a JSON file.
    
    Args:
        conversation (Conversation): The conversation instance.
        file_path (str): The output file path.
    """
    session_data = export_session(conversation)
    with open(file_path, "w") as f:
        json.dump(session_data, f, indent=4)
