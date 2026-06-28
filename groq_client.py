import streamlit as st
from openai import OpenAI

GROQ_URL = "https://api.groq.com/openai/v1"

# Using a fallback list directly if config isn't populated on the cloud
GROQ_MODELS = ["llama3-8b-8192", "mixtral-8x7b-32768"]

def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    # 1. Safely pull the API key from Streamlit Cloud secrets
    if "GROQ_API_KEY" not in st.secrets:
        return "Error: GROQ_API_KEY not found in Streamlit Secrets."
    
    api_key = st.secrets["GROQ_API_KEY"]

    # 2. Initialize the OpenAI client with Groq's endpoint
    client = OpenAI(
        api_key=api_key,
        base_url=GROQ_URL,
    )
    
    last_error = None
    
    # 3. Try available models
    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            return content if content else ""
        except Exception as e:
            last_error = e
            
    return f"Groq Error: {last_error}"
