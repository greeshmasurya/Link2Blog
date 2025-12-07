import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GRADIENT_API_KEY")

def generate_blog(transcript, style):
    if API_KEY == "YOUR_API_KEY_SECRET":
        return "Error: Please update the API_KEY."

    url = "https://apis.gradient.network/api/v1/ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
Convert the following YouTube transcript into a clean, structured blog post.
Apply the selected writing style: {style}.
Add:
- title
- summary
- sections with headings
- 4–6 key insights
- conclusion

Transcript:
{transcript[:15000]} 
""" 

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7,
        "performance_type": 0,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"API Error: {str(e)}"
