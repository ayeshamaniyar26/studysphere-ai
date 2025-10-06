import streamlit as st
from modules.rag_pipeline import RAGPipeline
from modules.utils import TTSManager, format_quiz_questions, format_flashcards, clean_extracted_text, get_daily_quote, QuizTimer, PomodoroTimer
import webbrowser

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="StudySphere AI - Your 360° Learning Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== Custom CSS ====================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .stat-box {
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        color: white;
        text-align: center;
    }
    .quote-box {
        padding: 1.5rem;
        background: #f0f7ff;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        font-style: italic;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Initialize ====================
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = RAGPipeline()

if 'tts_manager' not in st.session_state:
    st.session_state.tts_manager = TTSManager()

pipeline = st.session_state.pipeline
tts = st.session_state.tts_manager

# ==================== Header ====================
st.markdown("""
<div class="main-header">
    <h1>🎓 StudySphere AI</h1>
    <h3>Your 360° Learning Companion</h3>
    <p>Transform any study material into powerful learning tools with AI</p>
</div>
""", unsafe_allow_html=True)

# ==================== Sidebar ====================
with st.sidebar:
    st.header("📚 Knowledge Base")
    
    stats = pipeline.get_vectorstore_stats()
    st.markdown(f"""
    <div class="stat-box">
        <h2>{stats['total_chunks']}</h2>
        <p>Chunks in Knowledge Base</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🗑️ Clear Knowledge Base", type="secondary"):
        if pipeline.clear_vectorstore():
            st.success("✅ Knowledge base cleared!")
            st.rerun()
    
    st.divider()
    
    # Daily Quote
    st.subheader("💡 Daily Motivation")
    with st.spinner("Loading quote..."):
        daily_quote = get_daily_quote()
    st.markdown(f'<div class="quote-box">{daily_quote}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Pomodoro Timer
    st.subheader("⏱️ Study Timer (Pomodoro)")
    
    if 'pomodoro' not in st.session_state:
        st.session_state.pomodoro = PomodoroTimer(work_minutes=25, break_minutes=5)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", use_container_width=True):
            st.session_state.pomodoro.start_session()
            st.rerun()
    with col2:
        if st.button("⏹️ Reset", use_container_width=True):
            if 'pomodoro_start' in st.session_state:
                del st.session_state.pomodoro_start
            if 'pomodoro_type' in st.session_state:
                del st.session_state.pomodoro_type
            st.rerun()
    
    if 'pomodoro_start' in st.session_state:
        st.session_state.pomodoro.display()
    
    st.divider()
    
    # Educational URL Analyzer
    st.subheader("🔗 URL Analyzer")
    
    url_input = st.text_input("Paste YouTube or Website URL:", placeholder="https://...")
    
    if st.button("🧠 Analyze URL", use_container_width=True) and url_input:
        with st.spinner("🔍 Analyzing URL..."):
            analysis = pipeline.gemini.analyze_url(url_input)
            st.session_state.url_analysis = analysis
    
    if 'url_analysis' in st.session_state:
        with st.expander("📊 URL Analysis Result", expanded=True):
            st.markdown(st.session_state.url_analysis)
            
            if st.button("🔊 Listen", key="speak_url"):
                tts.speak(st.session_state.url_analysis)
    
    st.divider()
    
    st.markdown("**Quick Links:**")
    if st.button("📺 YouTube", use_container_width=True):
        webbrowser.open("https://youtube.com")

# ==================== Main Content ====================
st.header("📤 Upload Study Materials")

upload_mode = st.radio(
    "Upload Mode:",
    ["Single File", "Multiple Files"],
    horizontal=True
)

if upload_mode == "Single File":
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "pptx", "txt", "png", "jpg", "jpeg"],
        help="Upload PDF, DOCX, PPTX, TXT, or image files"
    )
    uploaded_files = [uploaded_file] if uploaded_file else []
else:
    uploaded_files = st.file_uploader(
        "Choose multiple files",
        type=["pdf", "docx", "pptx", "txt", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Upload multiple files at once"
    )

# Process uploaded files
if uploaded_files:
    has_image = any(f.type.startswith("image/") for f in uploaded_files)
    
    with st.spinner("🔄 Processing files..."):
        if len(uploaded_files) == 1:
            text = pipeline.process_single_file(uploaded_files[0])
        else:
            text = pipeline.process_multiple_files(uploaded_files)
        
        st.session_state.current_text = text
        
        if has_image:
            st.session_state.uploaded_images = [f for f in uploaded_files if f.type.startswith("image/")]
    
    if text:
        st.success(f"✅ Processed {len(uploaded_files)} file(s)")
        
        # ==================== IMAGE ANALYSIS (OCR + AI) ====================
        if 'uploaded_images' in st.session_state and st.session_state.uploaded_images:
            st.divider()
            st.subheader("🖼️ Image Analysis (OCR + AI)")
            
            for img_file in st.session_state.uploaded_images:
                with st.expander(f"📸 Analyze: {img_file.name}", expanded=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(img_file, caption=img_file.name, use_container_width=True)
                    
                    with col2:
                        if st.button(f"🤖 Explain Image (OCR + AI)", key=f"explain_{img_file.name}", use_container_width=True):
                            with st.spinner("🔍 Extracting text and analyzing..."):
                                explanation = pipeline.gemini.explain_image_with_ocr(img_file)
                                
                                if 'image_explanations' not in st.session_state:
                                    st.session_state.image_explanations = {}
                                st.session_state.image_explanations[img_file.name] = explanation
                        
                        if 'image_explanations' in st.session_state and img_file.name in st.session_state.image_explanations:
                            explanation = st.session_state.image_explanations[img_file.name]
                            
                            st.markdown("### 📝 Analysis Result")
                            st.info(explanation)
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("🔊 Listen", key=f"speak_img_{img_file.name}", use_container_width=True):
                                    tts.speak(explanation)
                            with col_b:
                                if st.button("📋 Copy", key=f"copy_img_{img_file.name}", use_container_width=True):
                                    st.code(explanation, language=None)
                                    st.success("✅ Select & press Ctrl+C")
        
        st.divider()
        
        # Preview - ONLY for non-image files with cleanup option
        if not has_image and text and "[IMAGE_CONTENT:" not in text:
            with st.expander("👁️ Preview Extracted Text"):
                # Text cleanup option
                cleanup_mode = st.checkbox("🧹 Clean-up Mode (remove headers/footers)", value=False)
                
                if cleanup_mode:
                    display_text = clean_extracted_text(text)
                else:
                    display_text = text
                
                # Fast preview - only first 500 characters
                st.markdown("**Fast Preview (first 500 characters):**")
                st.text_area(
                    "Content Preview",
                    display_text[:500] + ("..." if len(display_text) > 500 else ""),
                    height=150,
                    disabled=True
                )
                
                # Show full text option
                if st.checkbox("📄 Show Full Text", value=False):
                    st.text_area("Full Text", display_text, height=400, disabled=True)
        
        # Add to Knowledge Base
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("🧠 Add to Knowledge Base (RAG)")
            st.info("Add this document to the vector database for intelligent Q&A")
        with col2:
            st.write("")
            st.write("")
            if st.button("➕ Add to KB", type="primary"):
                source_name = uploaded_files[0].name if len(uploaded_files) == 1 else "multiple_files"
                pipeline.add_to_vectorstore(text, source_name)
                st.rerun()
        
        st.divider()
        
        # ==================== Feature Tabs ====================
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📝 Summary", 
            "❓ Quiz", 
            "💡 Flashcards", 
            "🧠 AI Tutor",
            "🔍 Semantic Search"
        ])
        
        # ==================== SUMMARY TAB ====================
        with tab1:
            st.header("📝 Generate Summary")
            
            col1, col2 = st.columns(2)
            with col1:
                summary_style = st.selectbox(
                    "Summary Style",
                    ["Short", "Long", "Bullet Points", "Exam-style"]
                )
            with col2:
                summary_length = st.slider("Approximate Length (words)", 50, 500, 150)
            
            if st.button("✨ Generate Summary", key="gen_summary", use_container_width=True):
                with st.spinner("🤖 Generating summary..."):
                    summary = pipeline.generate_summary(text, summary_style, summary_length)
                    st.session_state.current_summary = summary
            
            if 'current_summary' in st.session_state and st.session_state.current_summary:
                summary = st.session_state.current_summary
                
                st.markdown("### 📄 Summary")
                st.markdown(f"**Style:** {summary_style} | **Length:** ~{summary_length} words")
                st.info(summary)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔊 Listen to Summary", key="speak_summary", use_container_width=True):
                        tts.speak(summary)
                with col2:
                    if st.button("📋 Copy", key="copy_summary", use_container_width=True):
                        st.code(summary, language=None)
                        st.success("✅ Select & press Ctrl+C")
                
                st.markdown("---")
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("👍 Helpful", key="summary_like", use_container_width=True):
                        st.success("Thanks for the feedback! 😊")
                with col4:
                    if st.button("👎 Not Helpful", key="summary_dislike", use_container_width=True):
                        st.info("We'll improve! 💪")
        
        # ==================== QUIZ TAB WITH TIMER ====================
        with tab2:
            st.header("❓ Interactive Quiz")
            
            col1, col2 = st.columns(2)
            with col1:
                num_questions = st.slider("Number of Questions", 1, 10, 5)
            with col2:
                difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            
            # Quiz Mode Selection
            st.markdown("### ⏱️ Quiz Mode")
            quiz_mode = st.radio(
                "Select Mode:",
                ["Practice Mode (No Timer)", "Exam Mode (Timed)"],
                horizontal=True
            )
            
            timer_duration = None
            if quiz_mode == "Exam Mode (Timed)":
                timer_duration = st.select_slider(
                    "Timer Duration:",
                    options=[2, 5, 10, 15, 20],
                    value=10,
                    help="Select quiz duration in minutes"
                )
                st.info(f"⏰ You'll have {timer_duration} minutes to complete the quiz")
            
            if st.button("🎯 Generate Quiz", key="gen_quiz"):
                with st.spinner("🤖 Creating quiz questions..."):
                    quiz_text = pipeline.generate_quiz(text, num_questions, difficulty)
                    questions = format_quiz_questions(quiz_text)
                    
                    if questions:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_score = 0
                        st.session_state.quiz_answers = {}
                        
                        # Initialize timer if exam mode
                        if timer_duration:
                            st.session_state.quiz_timer = QuizTimer(timer_duration)
                            st.session_state.quiz_timer.start()
                            if 'quiz_start_time' in st.session_state:
                                del st.session_state.quiz_start_time
                        
                        st.success(f"✅ Generated {len(questions)} questions!")
                        st.rerun()
            
            # Display Timer if in Exam Mode
            if 'quiz_timer' in st.session_state:
                timer = st.session_state.quiz_timer
                time_expired = timer.display()
                
                if time_expired:
                    st.error("⏰ Time's up! Quiz auto-submitted.")
                    st.session_state.quiz_time_expired = True
            
            # Display Quiz
            if 'quiz_questions' in st.session_state and st.session_state.quiz_questions:
                st.divider()
                st.subheader("📊 Quiz Time!")
                
                # Check if time expired
                time_expired = st.session_state.get('quiz_time_expired', False)
                
                for idx, q in enumerate(st.session_state.quiz_questions):
                    st.markdown(f"### Question {idx + 1}")
                    st.markdown(f"**{q['question']}**")
                    
                    answer_key = f"q_{idx}"
                    
                    # Disable options if time expired
                    if time_expired:
                        st.warning("⏰ Time expired - answers locked")
                        if answer_key in st.session_state:
                            st.info(f"Your answer: {st.session_state[answer_key]}")
                    else:
                        selected = st.radio(
                            "Select your answer:",
                            q['options'],
                            key=answer_key,
                            label_visibility="collapsed"
                        )
                    
                    if st.button(f"Check Answer ✓", key=f"check_{idx}", disabled=time_expired):
                        if answer_key not in st.session_state:
                            st.warning("Please select an answer first!")
                        else:
                            selected = st.session_state[answer_key]
                            correct_letter = q['answer'][0] if q['answer'] else ""
                            selected_letter = selected[0] if selected else ""
                            
                            if selected_letter == correct_letter:
                                st.success(f"✅ Correct! {q['explanation']}")
                                st.session_state.quiz_answers[idx] = True
                            else:
                                st.error(f"❌ Wrong! Correct answer: {q['answer']}")
                                st.info(f"💡 {q['explanation']}")
                                st.session_state.quiz_answers[idx] = False
                    
                    st.divider()
                
                # Calculate score
                score = sum(1 for v in st.session_state.quiz_answers.values() if v)
                total = len(st.session_state.quiz_questions)
                percentage = (score / total * 100) if total > 0 else 0
                
                st.markdown(f"""
                <div class="stat-box">
                    <h2>Score: {score}/{total}</h2>
                    <p>{percentage:.1f}% Correct</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Reset quiz button
                if st.button("🔄 New Quiz", key="reset_quiz"):
                    keys_to_delete = ['quiz_questions', 'quiz_answers', 'quiz_timer', 'quiz_start_time', 'quiz_time_expired']
                    for key in keys_to_delete:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
        
        # ==================== FLASHCARDS TAB ====================
        with tab3:
            st.header("💡 Study Flashcards")
            
            num_cards = st.slider("Number of Flashcards", 5, 20, 10)
            
            if st.button("🎴 Generate Flashcards", key="gen_flashcards"):
                with st.spinner("🤖 Creating flashcards..."):
                    flashcard_text = pipeline.generate_flashcards(text, num_cards)
                    cards = format_flashcards(flashcard_text)
                    
                    if cards:
                        st.session_state.flashcards = cards
                        st.success(f"✅ Generated {len(cards)} flashcards!")
            
            if 'flashcards' in st.session_state and st.session_state.flashcards:
                st.divider()
                st.subheader(f"📚 {len(st.session_state.flashcards)} Flashcards")
                
                # Progress tracker
                if 'cards_studied' not in st.session_state:
                    st.session_state.cards_studied = set()
                
                progress = len(st.session_state.cards_studied) / len(st.session_state.flashcards)
                st.progress(progress, text=f"Progress: {len(st.session_state.cards_studied)}/{len(st.session_state.flashcards)} cards studied")
                
                cols = st.columns(3)
                for idx, card in enumerate(st.session_state.flashcards):
                    with cols[idx % 3]:
                        with st.expander(f"🎴 Card {idx + 1}", expanded=False):
                            st.markdown(f"**Q:** {card['question']}")
                            st.markdown(f"**A:** {card['answer']}")
                            
                            # Mark as studied
                            if st.checkbox("✅ Studied", key=f"studied_{idx}"):
                                st.session_state.cards_studied.add(idx)
                            
                            speech_text = f"Question: {card['question']}. Answer: {card['answer']}"
                            
                            if st.button("🔊 Listen", key=f"speak_card_{idx}", use_container_width=True):
                                tts.speak(speech_text)
        
        # ==================== AI TUTOR TAB ====================
        with tab4:
            st.header("🧠 AI Tutor - Ask Questions")
            
            st.info("💡 Ask questions about your uploaded documents. The AI will use RAG to find relevant information!")
            
            use_rag = st.checkbox("🔍 Use RAG (Knowledge Base)", value=True, help="Search the knowledge base for context")
            use_self_correction = st.checkbox("✨ Enable Self-Correction", value=True, help="Refine answers for better accuracy")
            
            user_question = st.text_area(
                "Your Question:",
                placeholder="E.g., What are the main concepts discussed in this document?",
                height=100
            )
            
            if st.button("🚀 Get Answer", type="primary", use_container_width=True):
                if not user_question:
                    st.warning("⚠️ Please enter a question!")
                else:
                    with st.spinner("🤖 Thinking..."):
                        if use_rag and stats['total_chunks'] > 0:
                            answer = pipeline.rag_query(user_question, use_self_correction)
                        else:
                            answer = pipeline.gemini.tutor_mode(user_question, text[:8000])
                        
                        st.session_state.current_answer = answer
            
            if 'current_answer' in st.session_state and st.session_state.current_answer:
                answer = st.session_state.current_answer
                
                st.markdown("### 💬 Answer")
                st.success(answer)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔊 Listen to Answer", key="speak_tutor", use_container_width=True):
                        tts.speak(answer)
                with col2:
                    if st.button("📋 Copy", key="copy_tutor", use_container_width=True):
                        st.code(answer, language=None)
                        st.success("✅ Select & press Ctrl+C")
                
                st.markdown("---")
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("👍 Helpful", key="tutor_like", use_container_width=True):
                        st.success("Thanks for the feedback! 😊")
                with col4:
                    if st.button("👎 Not Helpful", key="tutor_dislike", use_container_width=True):
                        st.info("We'll improve! 💪")
        
        # ==================== SEMANTIC SEARCH TAB ====================
        with tab5:
            st.header("🔍 Semantic Search")
            
            st.info("Search through your knowledge base using natural language!")
            
            search_query = st.text_input(
                "Search Query:",
                placeholder="E.g., machine learning algorithms"
            )
            
            top_k = st.slider("Number of Results", 1, 10, 5)
            
            if st.button("🔎 Search", type="primary"):
                if not search_query:
                    st.warning("⚠️ Please enter a search query!")
                elif stats['total_chunks'] == 0:
                    st.warning("⚠️ Knowledge base is empty. Upload and add documents first!")
                else:
                    with st.spinner("🔍 Searching..."):
                        results = pipeline.semantic_search(search_query, top_k)
                        
                        if results:
                            st.success(f"✅ Found {len(results)} relevant chunks")
                            
                            for idx, result in enumerate(results, 1):
                                with st.expander(f"📄 Result {idx} - Relevance: {1 - result['distance']:.2%}"):
                                    st.markdown(result['content'])
                                    st.caption(f"Source: {result['metadata'].get('source', 'Unknown')}")
                        else:
                            st.warning("❌ No results found!")

# ==================== Footer ====================
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎓 <b>StudySphere AI</b> - Your 360° Learning Companion</p>
    <p>Study smarter, not harder 💡</p>
</div>
""", unsafe_allow_html=True)