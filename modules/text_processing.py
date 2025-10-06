# modules/text_processing.py
import os
import requests

class GeminiProcessor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not set. Set GEMINI_API_KEY in environment variables.")
        self.BASE_URL = "https://api.generative.google/v1beta3/text-bison-001:generate"


from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not set. Set GEMINI_API_KEY in environment variables or .env file.")

    def _call_api(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "prompt": prompt,
            "temperature": 0.5,
            "max_output_tokens": 800
        }
        try:
            response = requests.post(self.BASE_URL, json=data, headers=headers, timeout=20)
            if response.status_code == 200:
                resp_json = response.json()
                return resp_json.get("candidates", [{}])[0].get("content", "")
            else:
                return f"⚠️ API request error: {response.status_code} {response.text}"
        except requests.exceptions.RequestException as e:
            return f"⚠️ API request exception: {str(e)}"

    # -----------------------------
    # Summary
    def generate_summary(self, text: str, style: str = "short") -> str:
        prompt = f"Summarize the following text in a {style} style:\n\n{text}"
        return self._call_api(prompt)

    # -----------------------------
    # Quiz
    def generate_quiz(self, text: str, num_questions: int = 5) -> str:
        prompt = (
            f"Create a quiz of {num_questions} questions based on the text below. "
            f"Format as Q&A:\n\n{text}"
        )
        return self._call_api(prompt)

    # -----------------------------
    # Flashcards
    def generate_flashcards(self, text: str) -> str:
        prompt = f"Create realistic study flashcards (question and answer) from the following text:\n\n{text}"
        return self._call_api(prompt)
