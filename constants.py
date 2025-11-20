import os
import google.generativeai as genai
import diskcache
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")


genai.configure(api_key=GEMINI_API_KEY)
client = genai.GenerativeModel("gemini-2.0-flash") 

cache = diskcache.Cache("./ai_cache")


class InMemoryStorage:
    def __init__(self):
        self._store = {}

    def set(self, key: str, value: object) -> None:
        self._store[key] = value

    def get(self, key: str) -> object:
        return self._store.get(key)

redis_instance = InMemoryStorage()
