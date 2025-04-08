from transformers import pipeline

# Test using a text generation pipeline with a small model from Hugging Face.
generator = pipeline("text-generation", model="distilgpt2")
prompt = "Hello, I am an AI agent,"
output = generator(prompt, max_length=50, do_sample=True)
print("Generated text:", output[0]['generated_text'])
