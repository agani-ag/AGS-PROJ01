"""
Answer Feedback Bot - Streamlit Application
Main application file for the Student Answer Feedback & Re-Evaluation Bot
"""

import streamlit as st
import os
from dotenv import load_dotenv
import uuid
import pandas as pd
from modules import AnswerEvaluator, DataStorage, AnalyticsEngine

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Answer Feedback Bot",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .strength-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .improvement-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .feedback-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .missing-concepts-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 12px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'evaluation_history' not in st.session_state:
    st.session_state.evaluation_history = []

if 'current_question' not in st.session_state:
    st.session_state.current_question = ""

if 'attempt_count' not in st.session_state:
    st.session_state.attempt_count = {}

# Initialize modules
@st.cache_resource
def initialize_modules():
    """Initialize application modules"""
    try:
        evaluator = AnswerEvaluator()
        storage = DataStorage()
        analytics = AnalyticsEngine()
        return evaluator, storage, analytics, None
    except Exception as e:
        return None, None, None, str(e)

# Always initialize storage and analytics
storage = DataStorage()
analytics = AnalyticsEngine()

# Try to initialize evaluator (may fail if API key not set)
evaluator, _, _, error = initialize_modules()

# Main title
st.title("📝 Answer Feedback Bot")
st.markdown("### Improve your answers with AI-powered feedback")

# Sidebar
with st.sidebar:
    st.header("📊 Session Info")
    st.write(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
    
    if st.button("🔄 New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.evaluation_history = []
        st.session_state.current_question = ""
        st.session_state.attempt_count = {}
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 How to Use")
    st.markdown("""
    1. Enter your question
    2. Enter your answer
    3. Click 'Evaluate Answer'
    4. Review feedback
    5. Improve and re-submit
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    api_key_set = os.getenv('OPENAI_API_KEY') is not None
    st.write(f"**API Key:** {'✅ Set' if api_key_set else '❌ Not Set'}")
    
    if not api_key_set:
        st.warning("⚠️ API key not configured. Evaluation feature will be disabled.")

# Create tabs for different sections
tab1, tab2 = st.tabs(["📝 Evaluation", "📈 Analytics & Graphs"])

# Tab 1: Evaluation
with tab1:
    st.header("Answer Evaluation")
    
    # Input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        question = st.text_area(
            "Enter the question:",
            height=120,
            placeholder="e.g., What is photosynthesis?",
            key="question_input"
        )
    
    with col2:
        answer = st.text_area(
            "Enter the student's answer:",
            height=120,
            placeholder="Enter your answer here...",
            key="answer_input"
        )
    
    # Optional human score input
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Optional: Teacher/Human Evaluation Score (0-10)**")
        st.caption("Enter your own score to compare with AI evaluation")
    with col2:
        human_score = st.number_input(
            "Human Score",
            min_value=0.0,
            max_value=10.0,
            value=None,
            step=0.5,
            format="%.1f",
            key="human_score_input",
            label_visibility="collapsed"
        )
    
    # Evaluate button
    if st.button("🎯 Evaluate Answer", type="primary"):
        if not question.strip():
            st.warning("⚠️ Please enter a question.")
        elif not answer.strip():
            st.warning("⚠️ Please enter an answer.")
        elif error or evaluator is None:
            st.error("❌ Cannot evaluate: OpenAI API key is not configured.")
            st.info("💡 Please set your OPENAI_API_KEY in the `.env` file to use the evaluation feature.")
        else:
            with st.spinner("🤔 Evaluating your answer..."):
                # Track attempt number
                if question not in st.session_state.attempt_count:
                    st.session_state.attempt_count[question] = 0
                
                st.session_state.attempt_count[question] += 1
                attempt_no = st.session_state.attempt_count[question]
                
                # Get evaluation
                try:
                    result = evaluator.evaluate_answer(question, answer)
                    
                    # Save to storage (including human score if provided)
                    storage.save_evaluation(
                        session_id=st.session_state.session_id,
                        question=question,
                        attempt_no=attempt_no,
                        evaluation_result=result,
                        answer_text=answer,
                        human_score=human_score
                    )
                    
                    # Store in session
                    st.session_state.evaluation_history.append({
                        'question': question,
                        'attempt_no': attempt_no,
                        'result': result,
                        'human_score': human_score
                    })
                    
                    success_msg = f"✅ Evaluation complete! (Attempt #{attempt_no})"
                    if human_score is not None:
                        success_msg += f" | Human Score: {human_score}/10 | AI Score: {result['score']}/10"
                    st.success(success_msg)
                    
                except Exception as e:
                    st.error(f"❌ Error during evaluation: {str(e)}")
    
    # Display latest evaluation if available
    if st.session_state.evaluation_history:
        latest = st.session_state.evaluation_history[-1]
        result = latest['result']
        attempt_no = latest['attempt_no']
        
        st.markdown("---")
        st.subheader(f"📊 Evaluation Results - Attempt #{attempt_no}")
        
        # Score with progress bar
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Score", f"{result['score']}/10")
        with col2:
            st.progress(result['score'] / 10)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Two-column layout for strengths and improvements
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Strengths")
            st.markdown('<div class="strength-box">', unsafe_allow_html=True)
            for strength in result.get('strengths', []):
                st.markdown(f"• {strength}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🔧 Areas for Improvement")
            st.markdown('<div class="improvement-box">', unsafe_allow_html=True)
            for area in result.get('areas_for_improvement', []):
                st.markdown(f"• {area}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Teacher's feedback
        st.markdown("### 👨‍🏫 Teacher's Feedback")
        st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
        st.write(result.get('feedback', 'No feedback available.'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Missing concepts
        if result.get('missing_concepts') and len(result['missing_concepts']) > 0:
            st.markdown("### 📚 Missing Concepts")
            st.markdown('<div class="missing-concepts-box">', unsafe_allow_html=True)
            for concept in result['missing_concepts']:
                st.markdown(f"• {concept}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show improvement message if this is not the first attempt
        if attempt_no > 1:
            st.info("💡 **Tip:** Compare your current score with previous attempts in the Analytics tab!")

# Tab 2: Analytics
with tab2:
    st.header("📈 Analytics & Graphs")
    
    # Get session data
    session_data = storage.get_session_data(st.session_state.session_id)
    
    if len(session_data) == 0:
        st.info("📭 No evaluation data yet. Complete at least one evaluation to see analytics.")
    else:
        # Calculate analytics
        analytics_df = analytics.calculate_session_analytics(session_data)
        overall_metrics = analytics.calculate_overall_metrics(analytics_df)
        
        # Overall metrics cards
        st.subheader("📊 Overall Performance")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Questions", overall_metrics['total_questions'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Improvement", f"{overall_metrics['avg_improvement_points']:.2f} pts")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Learning Gain", f"{overall_metrics['avg_learning_gain_pct']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Error Reduction", f"{overall_metrics['avg_error_reduction']:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Summary table
        st.subheader("📋 Question-wise Summary")
        st.dataframe(analytics_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Visualizations
        st.subheader("📊 Visualizations")
        
        # Before vs After chart
        st.markdown("#### Before vs After Score Comparison")
        fig1 = analytics.create_score_comparison_chart(analytics_df)
        st.pyplot(fig1)
        
        # Learning gain chart
        st.markdown("#### Learning Gain per Question")
        fig2 = analytics.create_learning_gain_chart(analytics_df)
        st.pyplot(fig2)
        
        # Error reduction chart
        st.markdown("#### Error Reduction per Question")
        fig3 = analytics.create_error_reduction_chart(analytics_df)
        st.pyplot(fig3)
        
        st.markdown("---")
        
        # Human vs AI Score Comparison Chart
        st.markdown("#### 🤖 Human vs AI Score Comparison")
        st.caption("This chart compares teacher/human scores with AI evaluation scores")
        fig_human_ai = analytics.create_human_vs_ai_comparison_chart(session_data)
        st.pyplot(fig_human_ai)
        
        st.markdown("---")
        
        # Detailed attempt history
        with st.expander("🔍 View Detailed Attempt History"):
            for idx, row in session_data.iterrows():
                st.markdown(f"**Question:** {row['question'][:100]}...")
                human_score_info = f" | **Human Score:** {row['human_score']}/10" if pd.notna(row.get('human_score')) and row.get('human_score') != '' else ""
                st.write(f"**Attempt:** {row['attempt_no']} | **AI Score:** {row['score']}/10{human_score_info} | **Time:** {row['timestamp']}")
                st.write(f"**Answer:** {row['answer_text'][:200]}...")
                st.markdown("---")
    
    # Global Analytics Section (ALL Sessions)
    st.markdown("---")
    st.markdown("---")
    st.header("🌍 Global Analytics (All Sessions)")
    st.info("📌 This section shows aggregate data from ALL sessions, not just the current one.")
    
    # Get all data
    all_data = storage.get_all_data()
    
    if len(all_data) == 0:
        st.warning("📭 No global data available yet.")
    else:
        # Calculate global analytics
        global_analytics = analytics.calculate_global_analytics(all_data)
        
        # Global metrics cards
        st.subheader("📊 Overall Statistics (All Time)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Sessions", global_analytics['total_sessions'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Evaluations", global_analytics['total_evaluations'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg First Score", f"{global_analytics['avg_first_score']:.2f}/10")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Last Score", f"{global_analytics['avg_last_score']:.2f}/10")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Second row of metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Questions", global_analytics['total_questions'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Improvement", f"{global_analytics['avg_improvement']:.2f} pts")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Learning Gain", f"{global_analytics['avg_learning_gain_pct']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Error Reduction", f"{global_analytics['avg_error_reduction']:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Global average chart
        st.subheader("📈 Global Average Score Progression")
        st.markdown("This chart shows how average scores change across attempt numbers, using data from all sessions.")
        fig_global = analytics.create_global_average_chart(global_analytics)
        st.pyplot(fig_global)
        
        st.markdown("---")
        
        # Global Human vs AI Comparison Chart
        st.subheader("🤖 Global Human vs AI Score Comparison")
        st.markdown("This chart compares average human scores with AI scores across all sessions and attempts.")
        fig_global_human_ai = analytics.create_global_human_vs_ai_chart(all_data)
        st.pyplot(fig_global_human_ai)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Answer Feedback Bot | Powered by OpenAI & Streamlit</div>",
    unsafe_allow_html=True
)
