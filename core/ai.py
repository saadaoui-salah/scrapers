from transformers import pipeline

# Load DistilGPT-2 model
generator = pipeline("text-generation", model="gpt2")

def email_site_finder():
    prompt = "Extract the contact email of the company from the website https://www.techinsf.com/. Only return the email address without any additional text."
    output = generator(prompt, max_length=5000)
    print(output[0]['generated_text'])


email_site_finder()