# modules/ocr_audio.py
import pytesseract
from PIL import Image
import pyttsx3
from modules.text_processing import GeminiProcessor

class OCRAudioProcessor:
    def __init__(self):
        self.ai_processor = GeminiProcessor()  # Use Gemini Flash API
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speech speed

    # -----------------
    # Extract text from image
    def extract_text_from_image(self, file_path: str) -> str:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)

            if text.strip():
                # Use AI to explain the image content
                explanation = self.ai_processor.explain_image(text)
                return f"📄 Extracted Text:\n{text}\n\n💡 Explanation:\n{explanation}"
            else:
                return "No text detected in the image."

        except Exception as e:
            return f"OCR error: {str(e)}"

    # -----------------
    # Text-to-Speech
    def text_to_speech(self, text: str):
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {str(e)}")
