from abc import ABC, abstractmethod
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

torch.classes.__path__ = []

class LLMBackend(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_length: int) -> str:
        pass

    @abstractmethod
    def generate_with_trace(self, prompt: str, max_length: int) -> (str, list):
        """
        Generate text and return chain-of-thought details (token-level trace).
        """
        pass

class HuggingFaceBackend(LLMBackend):
    def __init__(self, model_name: str):
        self.model_name = model_name
        # Load the model and tokenizer directly for advanced generation.
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()

    def generate(self, prompt: str, max_length: int) -> str:
        # Use generate_with_trace and ignore the trace
        output, _ = self.generate_with_trace(prompt, max_length)
        return output

    def generate_with_trace(self, prompt: str, max_length: int) -> (str, list):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        prompt_length = inputs['input_ids'].shape[1]
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            do_sample=True,
            output_scores=True,
            return_dict_in_generate=True
        )
        # Decode the full output and then remove the prompt part if it exists.
        full_text = self.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        if full_text.startswith(prompt):
            generated_text = full_text[len(prompt):].strip()
        else:
            generated_text = full_text

        # Build chain-of-thought trace: For each generation step, get the top token and its confidence.
        trace_info = []
        for step, logits in enumerate(outputs.scores):
            probs = torch.softmax(logits, dim=-1)
            top_prob, top_idx = torch.topk(probs, 1)
            token_str = self.tokenizer.decode(top_idx[0])
            trace_info.append({"token": token_str.strip(), "confidence": top_prob.item()})
        return generated_text, trace_info
