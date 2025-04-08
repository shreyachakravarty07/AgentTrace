# agenttrace/orchestrator.py
import torch

from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
import json
import logging

logger = logging.getLogger(__name__)

def create_agent_chain(model_name: str, max_length: int, 
                       task_description: str, 
                       custom_template: str = None) -> RunnableSequence:
    """
    Creates a RunnableSequence that functions as an agent workflow for generating a detailed plan.
    
    Args:
        model_name (str): The identifier of the model to use (e.g., "gpt2" or "EleutherAI/gpt-neo-125M").
        max_length (int): The maximum output length for the generation.
        task_description (str): The description of the task for which to generate a plan.
        custom_template (str, optional): An editable prompt template containing the '{task}' placeholder.
        
    Returns:
        RunnableSequence: A configured sequence ready to run the agent workflow.
    """
    # Default prompt template that instructs the model to output a JSON formatted plan.
    default_template = (
        "You are an expert AI agent specialized in planning complex tasks.\n"
        "Given the following task, provide a detailed, step-by-step plan in JSON format.\n"
        "Your output must be valid JSON with a key 'plan' containing an array of steps.\n"
        "Each step should be an object with 'step_number', 'description', and 'notes'.\n\n"
        "Task: {task}\n\n"
        "Ensure that your output is strictly in JSON format."
    )
    template_str = custom_template if custom_template else default_template
    prompt = PromptTemplate(template=template_str, input_variables=["task"])
    
    # Create a HuggingFace text-generation pipeline with the specified model and parameters.
    hf_pipeline = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=model_name,
        max_new_tokens=max_length,
        do_sample=True,
        temperature=0.9,
        top_p=0.95,
        top_k=50,
        return_full_text=False
    )
    
    # Wrap the pipeline using LangChain's HuggingFacePipeline wrapper.
    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    
    # Create the RunnableSequence using the pipe operator.
    chain = prompt | llm | StrOutputParser()
    logger.info(f"Created agent chain with model '{model_name}' and custom template.")
    return chain

def run_agent_chain(chain: RunnableSequence, task_description: str) -> dict:
    """
    Executes the given RunnableSequence for the provided task description and parses the output as JSON.
    
    Args:
        chain (RunnableSequence): The agent chain to run.
        task_description (str): The task input to feed into the chain.
        
    Returns:
        dict: The parsed JSON plan if successful; otherwise, a dict with key 'raw_output'.
    """
    raw_output = chain.invoke({"task": task_description})
    print("This is task:", task_description)
    try:
        print("This is the output:", raw_output)
        parsed_output = json.loads(raw_output)
        return parsed_output
    except json.JSONDecodeError:
        logging.error("Failed to parse output as JSON. Returning raw output.")
        return {"raw_output": raw_output}
