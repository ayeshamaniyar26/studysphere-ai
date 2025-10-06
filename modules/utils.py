import streamlit as st
from gtts import gTTS
import io
import time
import requests
from datetime import datetime, timedelta
import re


class TTSManager:
    """Text-to-Speech using gTTS (actually works!)"""

    def __init__(self):
        self.is_playing = False

    def speak(self, text: str, lang='en'):
        """Convert text to speech and play in Streamlit"""
        try:
            if not text or not text.strip():
                st.warning("No text to speak")
                return

            # Limit text length for faster processing
            text_to_speak = text[:1000] if len(text) > 1000 else text

            # Create audio using gTTS
            tts = gTTS(text=text_to_speak, lang=lang, slow=False)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)

            # Play audio in Streamlit
            st.audio(audio_bytes, format='audio/mp3')
            self.is_playing = True

        except Exception as e:
            st.error(f"TTS Error: {e}")
            self.is_playing = False

    def get_status(self):
        """Get current status"""
        return "🔊 Ready to speak" if not self.is_playing else "🔊 Audio playing"


class QuizTimer:
    """Timer for quiz exam mode"""

    def __init__(self, duration_minutes: int):
        self.duration = duration_minutes * 60  # Convert to seconds
        self.start_time = None
        self.is_running = False

    def start(self):
        """Start the timer"""
        if 'quiz_start_time' not in st.session_state:
            st.session_state.quiz_start_time = time.time()
        self.start_time = st.session_state.quiz_start_time
        self.is_running = True

    def get_remaining_time(self):
        """Get remaining time in seconds"""
        if not self.start_time:
            return self.duration

        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)
        return int(remaining)

    def is_expired(self):
        """Check if timer has expired"""
        return self.get_remaining_time() <= 0

    def format_time(self):
        """Format time as MM:SS"""
        remaining = self.get_remaining_time()
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

    def display(self):
        """Display timer in Streamlit"""
        remaining = self.get_remaining_time()

        if remaining > 60:
            color = "🟢"
        elif remaining > 30:
            color = "🟡"
        else:
            color = "🔴"

        time_str = self.format_time()

        if self.is_expired():
            st.error("⏰ Time's Up!")
            return True
        else:
            st.info(f"{color} Time Remaining: **{time_str}**")
            return False


class PomodoroTimer:
    """Simple Pomodoro study timer"""

    def __init__(self, work_minutes=25, break_minutes=5):
        self.work_duration = work_minutes * 60
        self.break_duration = break_minutes * 60
        self.is_work_session = True

    def start_session(self):
        """Start a new pomodoro session"""
        if 'pomodoro_start' not in st.session_state:
            st.session_state.pomodoro_start = time.time()
            st.session_state.pomodoro_type = 'work'

    def get_remaining_time(self):
        """Get remaining time in current session"""
        if 'pomodoro_start' not in st.session_state:
            return self.work_duration if self.is_work_session else self.break_duration

        elapsed = time.time() - st.session_state.pomodoro_start
        duration = self.work_duration if st.session_state.pomodoro_type == 'work' else self.break_duration
        remaining = max(0, duration - elapsed)
        return int(remaining)

    def format_time(self):
        """Format time as MM:SS"""
        remaining = self.get_remaining_time()
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

    def is_expired(self):
        """Check if session expired"""
        return self.get_remaining_time() <= 0

    def display(self):
        """Display pomodoro timer"""
        if 'pomodoro_start' not in st.session_state:
            return

        session_type = st.session_state.pomodoro_type
        remaining = self.get_remaining_time()

        if session_type == 'work':
            icon = "📚"
            label = "Focus Time"
        else:
            icon = "☕"
            label = "Break Time"

        time_str = self.format_time()

        if self.is_expired():
            if session_type == 'work':
                st.success("🎉 Work session complete! Take a break!")
                st.session_state.pomodoro_type = 'break'
            else:
                st.success("🔔 Break over! Ready for another session?")
                st.session_state.pomodoro_type = 'work'

            st.session_state.pomodoro_start = time.time()
        else:
            st.info(f"{icon} **{label}**: {time_str}")

        return remaining


def format_quiz_questions(quiz_text: str):
    """Parse quiz text into structured format"""
    questions = []
    current_q = {}

    lines = quiz_text.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("Q") and ":" in line:
            if current_q:
                questions.append(current_q)
            current_q = {"question": line.split(":", 1)[1].strip(), "options": [], "answer": "", "explanation": ""}

        elif line.startswith(("A)", "B)", "C)", "D)")):
            current_q["options"].append(line)

        elif "Correct Answer:" in line:
            current_q["answer"] = line.split(":", 1)[1].strip()

        elif "Explanation:" in line:
            current_q["explanation"] = line.split(":", 1)[1].strip()

    if current_q:
        questions.append(current_q)

    return questions


def format_flashcards(flashcard_text: str):
    """Parse flashcard text into Q&A pairs"""
    cards = []
    lines = flashcard_text.strip().split("\n")
    current_card = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("Q:"):
            if current_card:
                cards.append(current_card)
            current_card = {"question": line[2:].strip(), "answer": ""}

        elif line.startswith("A:") and current_card:
            current_card["answer"] = line[2:].strip()

    if current_card:
        cards.append(current_card)

    return cards


def clean_extracted_text(text: str) -> str:
    """Clean up extracted text by removing headers, footers, page numbers"""
    if not text:
        return ""

    # Remove page numbers (standalone numbers)
    text = re.sub(r'\n\d+\n', '\n', text)

    # Remove common headers/footers patterns
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'©.*?\d{4}', '', text)  # Copyright notices

    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    return text.strip()


def get_daily_quote():
    """Fetch daily motivational quote from ZenQuotes API"""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                quote = data[0].get('q', 'Stay motivated!')
                author = data[0].get('a', 'Anonymous')
                return f'"{quote}"\n\n— {author}'
    except:
        pass

    # Fallback quotes
    fallback_quotes = [
        '"Education is the most powerful weapon which you can use to change the world."\n\n— Nelson Mandela',
        '"The beautiful thing about learning is that no one can take it away from you."\n\n— B.B. King',
        '"Study while others are sleeping; work while others are loafing."\n\n— William A. Ward',
        '"Success is the sum of small efforts repeated day in and day out."\n\n— Robert Collier'
    ]

    day_index = datetime.now().timetuple().tm_yday % len(fallback_quotes)
    return fallback_quotes[day_index]


def copy_to_clipboard(text: str):
    """Copy given text to clipboard"""
    try:
        import pyperclip
        pyperclip.copy(text)
        st.success("✅ Text copied to clipboard!")
    except ModuleNotFoundError:
        st.warning("pyperclip not installed. Install with `pip install pyperclip`")
    except Exception as e:
        st.error(f"Error copying to clipboard: {e}")
