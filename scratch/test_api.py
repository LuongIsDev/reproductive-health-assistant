import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL").strip()
API_KEY = os.getenv("API_KEY").strip()
MODEL_NAME = os.getenv("MODEL_NAME").strip()

print(f"Testing API with:")
print(f"  URL: {API_URL}")
print(f"  Model: {MODEL_NAME}")

client = OpenAI(base_url=API_URL, api_key=API_KEY)

try:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=10
    )
    print("SUCCESS!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("FAILED!")
    print("Error:", e)
