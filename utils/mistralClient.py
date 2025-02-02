import requests

# Replace with your Mistral API endpoint and API key
API_URL = "https://api.mistral.ai/v1/completions"
API_KEY = "API_KEY"

def send_prompt_to_mistral(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "mistral-7b",  # Replace with the specific model if needed
        "prompt": prompt,
        "max_tokens": 200,      # Adjust as needed
        "temperature": 0.2,     # Adjust for response randomness
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
prompt_text = "Write a short poem about the sea."
response = send_prompt_to_mistral(prompt_text)

if response:
    print("Response from Mistral API:", end=" ")
    print(response)
