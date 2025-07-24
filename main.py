from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

prompt = "Who is trump?"
result = generator(prompt, max_new_tokens=64)

print(result[0]['generated_text'])
