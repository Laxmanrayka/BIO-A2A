from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              messages=[{"role": "user","content":"BRCA1 gene kya hota hai? 2 lines mein batao."}])
print("Groq connected!")
print(response.choices[0].message.content)

