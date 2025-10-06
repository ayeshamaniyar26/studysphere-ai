import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
import re
from PIL import Image
import pytesseract

class GeminiProcessor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("⚠️ GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=self.api_key)
        # Use the CORRECT model name for free tier
        self.model = genai.GenerativeModel("models/gemini-flash-latest")

    
    def generate(self, prompt, max_tokens=2048):
        """Generate content using Gemini"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            st.error(f"Gemini API Error: {e}")
            return f"Error generating response: {e}"
    
    @st.cache_data(ttl=3600)
    def generate_summary(_self, text, style="concise", length=150):
        """Generate summary with caching"""
        style_prompts = {
            "short": "very brief and concise",
            "long": "detailed and comprehensive",
            "bullet points": "in bullet point format",
            "exam-style": "in exam preparation format with key points"
        }
        
        style_desc = style_prompts.get(style.lower(), "concise")
        
        prompt = f"""Summarize the following text in a {style_desc} manner, 
approximately {length} words:

{text[:10000]}"""
        
        return _self.generate(prompt)
    
    def generate_quiz(self, text, num_questions=5, difficulty="medium"):
        """Generate quiz questions"""
        prompt = f"""Create {num_questions} multiple-choice questions from the text below.
Difficulty level: {difficulty}

Format each question exactly as:
Q1: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [A/B/C/D]
Explanation: [Brief explanation]

Text:
{text[:8000]}"""
        
        return self.generate(prompt, max_tokens=2048)
    
    @st.cache_data(ttl=3600)
    def generate_flashcards(_self, text, num_cards=10):
        """Generate flashcards with caching"""
        prompt = f"""Create {num_cards} study flashcards from the following text.
Format each flashcard as:
Q: [Question]
A: [Answer]

Make them concise and focused on key concepts.

Text:
{text[:8000]}"""
        
        return _self.generate(prompt, max_tokens=1500)
    
    def tutor_mode(self, question, context):
        """Answer questions based on context"""
        prompt = f"""You are a helpful and patient tutor. Answer the student's question based on the provided context.
If the answer isn't in the context, say so politely and provide general guidance.

Context:
{context[:8000]}

Student's Question: {question}

Provide a clear, educational answer:"""
        
        return self.generate(prompt, max_tokens=1024)
    
    def explain_image_with_ocr(self, image_file):
        """Extract text from image using OCR then explain with AI"""
        try:
            # Reset file pointer
            image_file.seek(0)
            
            # Load image
            img = Image.open(image_file)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(img)
            
            if not extracted_text.strip():
                return "⚠️ No text detected in image. The image might be purely visual or the text is unclear."
            
            # Use Gemini to explain the extracted text
            prompt = f"""Analyze and explain this text that was extracted from an image:

{extracted_text}

Provide:
1. **Content Summary**: What is this image about?
2. **Key Information**: Main points or data shown
3. **Educational Context**: What subject/topic does this relate to?
4. **Explanation**: Explain the concepts in simple terms
5. **Key Takeaways**: 3-4 important points

Be thorough and educational."""
            
            explanation = self.generate(prompt, max_tokens=1500)
            
            return f"📄 **Extracted Text:**\n{extracted_text}\n\n---\n\n🤖 **AI Explanation:**\n{explanation}"
            
        except Exception as e:
            st.error(f"Image analysis error: {e}")
            return f"Unable to analyze image: {str(e)}"
    
    def analyze_url(self, url: str):
        """Analyze YouTube video or website URL"""
        try:
            # Detect URL type
            if 'youtube.com' in url or 'youtu.be' in url:
                return self._analyze_youtube(url)
            else:
                return self._analyze_website(url)
        except Exception as e:
            return f"⚠️ Unable to fetch content. Error: {str(e)}"
    
    def _extract_youtube_id(self, url: str):
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def _analyze_youtube(self, url: str):
        """Analyze YouTube video"""
        try:
            # Extract video ID
            video_id = self._extract_youtube_id(url)
            if not video_id:
                return "⚠️ Invalid YouTube URL"
            
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([t['text'] for t in transcript_list])
            
            # Detect language
            try:
                lang = detect(transcript_text[:200])
                language = "Hindi" if lang == 'hi' else "English" if lang == 'en' else lang.upper()
            except:
                language = "Unknown"
            
            # Get video title (approximate from transcript)
            title_guess = transcript_text[:100] + "..."
            
            # Summarize with Gemini
            summary_prompt = f"""Summarize this YouTube video transcript in 1 paragraph and 4-5 bullet points:

Transcript:
{transcript_text[:5000]}

Format:
**Summary**: [1 paragraph]

**Key Points**:
- Point 1
- Point 2
- Point 3
- Point 4"""
            
            summary = self.generate(summary_prompt, max_tokens=800)
            
            return f"""🔗 **Type**: YouTube Video
🎯 **Topic**: {title_guess}
🗣 **Language**: {language}

{summary}"""
            
        except Exception as e:
            return f"⚠️ Unable to fetch YouTube transcript. Error: {str(e)}\n\nNote: Some videos may not have transcripts available."
    
    def _analyze_website(self, url: str):
        """Analyze website or blog"""
        try:
            # Fetch webpage
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Unknown"
            
            # Extract main content (paragraphs)
            paragraphs = soup.find_all('p')
            content_text = " ".join([p.get_text().strip() for p in paragraphs[:20]])
            
            if not content_text:
                return "⚠️ Unable to extract meaningful content from this webpage."
            
            # Summarize with Gemini
            summary_prompt = f"""Analyze this webpage content and provide:

Title: {title_text}

Content:
{content_text[:3000]}

Format:
**Purpose**: [What is this webpage about?]
**Main Topics**: [Key subjects covered]
**Summary**: [2-3 sentences]
**Key Takeaways**: [3-4 bullet points]"""
            
            summary = self.generate(summary_prompt, max_tokens=800)
            
            return f"""🔗 **Type**: Website/Blog
📄 **Title**: {title_text}

{summary}"""
            
        except requests.exceptions.Timeout:
            return "⚠️ Request timeout. The website took too long to respond."
        except requests.exceptions.RequestException as e:
            return f"⚠️ Unable to fetch website. Error: {str(e)}"
    
    def refine_answer(self, question, initial_answer, retrieved_context):
        """Self-correcting RAG: Refine answer based on retrieved context"""
        prompt = f"""You previously answered a question, but now have additional context.
Refine your answer to be more accurate and complete.

Question: {question}
Previous Answer: {initial_answer}

Additional Context:
{retrieved_context}

Provide an improved, accurate answer:"""
        
        return self.generate(prompt, max_tokens=1024)