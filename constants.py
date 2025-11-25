import os
import google.generativeai as genai
import diskcache
import openai
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")
openai.api_key = OPENAI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
client = genai.GenerativeModel("gemini-2.5-flash-lite") 

cache = diskcache.Cache("./ai_cache")


class InMemoryStorage:
    def __init__(self):
        self._store = {}

    def set(self, key: str, value: object) -> None:
        self._store[key] = value

    def get(self, key: str) -> object:
        return self._store.get(key)

redis_instance = InMemoryStorage()
