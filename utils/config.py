import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Dictionary of available model providers and their respective models
MODEL_OPTIONS = {
  "Groq": {
    "playground": "https://console.groq.com/",
    "models": ["llama-3.1-8b-instant", "llama3-70b-8192"]
  },

  "OpenRouter": {
    "playground": "https://openrouter.ai/",
    "models": [
      "mistralai/mistral-7b-instruct",
      "meta-llama/llama-3-8b-instruct",
      "deepseek-ai/deepseek-coder-6.7b-instruct",
      "google/gemma-2b"
    ]
  }
}
