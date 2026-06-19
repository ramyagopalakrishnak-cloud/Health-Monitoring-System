# app.py
# MindPulse AI — Mental Health Sentiment Tracker
# Main application file — runs the entire app

import streamlit as st
from datetime import datetime
import time

# Import our own files
from sentiment import detect_mood, get_sentiment_score, get_mood_emoji, get_mood_color, get_quick_tip
from gemini_helper import get_ai_response, get_coping_strategies, get_daily_affirmation
from charts import save_mood_entry, load_mood_data, get_mood_summary
from charts import chart_mood_timeline, chart_mood_distribution, chart_mood_bar, chart_daily_average

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# Must be the very first Streamlit command!
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="MindPulse AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ─────────────────────────────────────────────
# CUSTOM CSS STYLING
# Makes the app look beautiful and professional
# ─────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 100%);
    }

    /* Header banner */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }

    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .main-header p {
        color: rgba(255,255,255,0.85);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }

    /* Mood result card */
    .mood-card {
        background: linear-gradient(135deg, #1e1e3f 0%, #2d2d5e 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* AI response box */
    .ai-response {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    /* Affirmation box */
    .affirmation-box {
        background: linear-gradient(135deg, #134e5e, #71b280);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        text-align: center;
        color: white;
        font-size: 1.1rem;
        font-style: italic;
        font-weight: 500;
    }

    /* Metric cards */
    .metric-card {
        background: #1e1e3f;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(102,126,234,0.2);
    }

    /* Tip box */
    .tip-box {
        background: rgba(46, 204, 113, 0.1);
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: #2ecc71;
    }

    /* Strategy box */
    .strategy-box {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: white;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: #1a1a2e;
    }

    /* Text area */
    .stTextArea textarea {
        background: #1e1e3f !important;
        color: white !important;
        border: 1px solid rgba(102,126,234,0.4) !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# Remembers data while the app is running
# ─────────────────────────────────────────────

if "history" not in st.session_state:
    st.session_state.history = []

if "last_mood" not in st.session_state:
    st.session_state.last_mood = None


# ─────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>🧠 MindPulse AI</h1>
    <p>Your personal mental health sentiment tracker — powered by AI 💚</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# Navigation and app info
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🧭 Navigation")

    page = st.radio(
        "Go to:",
        ["🏠 Home — Check In", "📊 My Mood Dashboard", "ℹ️ About MindPulse"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 💡 Did You Know?")
    facts = [
        "Writing about your feelings reduces stress by up to 30%.",
        "Tracking your mood daily improves emotional awareness.",
        "Deep breathing activates your body's calm response.",
        "Gratitude journaling increases happiness over time.",
        "1 in 4 people experience a mental health issue each year.",
    ]
    import random
    st.info(random.choice(facts))

    st.markdown("---")
    st.caption("MindPulse AI — Built with ❤️ for mental wellness")


# ═══════════════════════════════════════════════════════════
# PAGE 1: HOME — CHECK IN
# ═══════════════════════════════════════════════════════════

if page == "🏠 Home — Check In":

    col1, col2 = st.columns([3, 2], gap="large")

    # ── LEFT COLUMN: Input area ──
    with col1:
        st.markdown("### 💬 How are you feeling right now?")
        st.markdown(
            "Write freely — there's no right or wrong answer. "
            "This is your safe space. 🌿"
        )

        user_input = st.text_area(
            label="Your feelings",
            placeholder=(
                "Example: 'I've been feeling really overwhelmed lately "
                "with everything going on. My exams are coming up and "
                "I can't seem to focus...'"
            ),
            height=160,
            label_visibility="collapsed"
        )

        submit = st.button("🔍 Analyse My Mood")

    # ── RIGHT COLUMN: Live tip ──
    with col2:
        st.markdown("### ✨ Today's Affirmation")

        # Show affirmation for last mood or a default
        mood_for_affirmation = (
            st.session_state.last_mood
            if st.session_state.last_mood
            else "neutral"
        )

        with st.spinner("Loading affirmation..."):
            affirmation = get_daily_affirmation(mood_for_affirmation)

        st.markdown(
            f'<div class="affirmation-box">"{affirmation}"</div>',
            unsafe_allow_html=True
        )

        st.markdown("### 📋 Quick Stats")
        df = load_mood_data()
        if not df.empty:
            summary = get_mood_summary(df)
            emoji   = get_mood_emoji(summary["latest_mood"])
            st.markdown(
                f'<div class="metric-card">'
                f'<h3 style="color:white">{emoji} {summary["latest_mood"].capitalize()}</h3>'
                f'<p style="color:#aaa">Last recorded mood</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="metric-card" style="margin-top:0.5rem">'
                f'<h3 style="color:white">📝 {summary["total_entries"]}</h3>'
                f'<p style="color:#aaa">Total check-ins</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.info("No entries yet — do your first check-in! 👆")

    # ─────────────────────────────────────────
    # WHEN USER CLICKS ANALYSE
    # ─────────────────────────────────────────

    if submit:
        if not user_input.strip():
            st.warning("⚠️ Please write something before analysing!")

        else:
            st.markdown("---")

            # Step 1: Detect mood
            with st.spinner("🔍 Analysing your mood..."):
                mood  = detect_mood(user_input)
                score = get_sentiment_score(user_input)
                emoji = get_mood_emoji(mood)
                color = get_mood_color(mood)
                tip   = get_quick_tip(mood)
                time.sleep(0.5)  # Small pause for effect

            # Step 2: Show mood result
            st.markdown(
                f'<div class="mood-card">'
                f'<h2 style="color:{color}; margin:0">'
                f'{emoji} Detected Mood: {mood.upper()}</h2>'
                f'<p style="color:#aaa; margin:0.3rem 0 0 0">'
                f'Sentiment Score: <b style="color:white">{score}</b> '
                f'(scale: -1.0 = very negative → +1.0 = very positive)</p>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Step 3: Quick tip
            st.markdown(
                f'<div class="tip-box">💡 {tip}</div>',
                unsafe_allow_html=True
            )

            # Step 4: Get and show AI response
            with st.spinner("🤖 MindPulse AI is thinking..."):
                ai_response = get_ai_response(user_input, mood)

            st.markdown("### 🤖 MindPulse AI Says:")
            st.markdown(
                f'<div class="ai-response">{ai_response}</div>',
                unsafe_allow_html=True
            )

            # Step 5: Get and show coping strategies
            with st.spinner("🛠️ Generating personalised strategies..."):
                strategies = get_coping_strategies(mood)

            st.markdown("### 🛠️ Personalised Coping Strategies:")
            st.markdown(
                f'<div class="strategy-box">{strategies}</div>',
                unsafe_allow_html=True
            )

            # Step 6: Save entry and update state
            save_mood_entry(user_input, mood, score)
            st.session_state.last_mood = mood
            st.session_state.history.append({
                "mood": mood, "score": score, "text": user_input
            })

            # Step 7: Success message
            st.success(
                f"✅ Your mood entry has been saved! "
                f"Visit 📊 My Mood Dashboard to see your trends."
            )

            # Step 8: Encouraging footer
            st.markdown(
                f'<div class="affirmation-box" style="margin-top:1rem">'
                f'Remember: Tracking your feelings is an act of self-love. 💚'
                f'</div>',
                unsafe_allow_html=True
            )


# ═══════════════════════════════════════════════════════════
# PAGE 2: MOOD DASHBOARD
# ═══════════════════════════════════════════════════════════

elif page == "📊 My Mood Dashboard":

    st.markdown("### 📊 Your Mood Dashboard")

    df = load_mood_data()

    if df.empty:
        st.info(
            "📭 No mood data yet! Go to **🏠 Home** and do your "
            "first check-in to see your dashboard come alive."
        )

    else:
        summary = get_mood_summary(df)

        # ── Summary Metric Cards ──
        st.markdown("#### 📈 Your Stats at a Glance")
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                "Total Check-ins",
                summary["total_entries"],
                help="Number of mood entries recorded"
            )
        with m2:
            st.metric(
                "Avg Mood Score",
                summary["average_score"],
                help="Score from -1.0 (negative) to +1.0 (positive)"
            )
        with m3:
            emoji = get_mood_emoji(summary["dominant_mood"])
            st.metric(
                "Most Common Mood",
                f"{emoji} {summary['dominant_mood'].capitalize()}"
            )
        with m4:
            latest_emoji = get_mood_emoji(summary["latest_mood"])
            st.metric(
                "Latest Mood",
                f"{latest_emoji} {summary['latest_mood'].capitalize()}"
            )

        st.markdown("---")

        # ── Charts Row 1 ──
        chart_col1, chart_col2 = st.columns(2, gap="medium")

        with chart_col1:
            fig_timeline = chart_mood_timeline(df)
            if fig_timeline:
                st.plotly_chart(fig_timeline, use_container_width=True)
            else:
                st.info("Add at least 2 entries to see the timeline!")

        with chart_col2:
            fig_donut = chart_mood_distribution(df)
            if fig_donut:
                st.plotly_chart(fig_donut, use_container_width=True)

        # ── Charts Row 2 ──
        chart_col3, chart_col4 = st.columns(2, gap="medium")

        with chart_col3:
            fig_bar = chart_mood_bar(df)
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col4:
            fig_daily = chart_daily_average(df)
            if fig_daily:
                st.plotly_chart(fig_daily, use_container_width=True)
            else:
                st.info("Add entries on multiple days to see daily averages!")

        # ── Mood History Table ──
        st.markdown("---")
        st.markdown("#### 📋 Your Mood History")

        display_df = df[["date", "time", "mood", "score", "text"]].copy()
        display_df["mood"] = display_df["mood"].apply(
            lambda m: f"{get_mood_emoji(m)} {m.capitalize()}"
        )
        display_df.columns = ["Date", "Time", "Mood", "Score", "What you wrote"]
        st.dataframe(
            display_df.iloc[::-1],  # Show newest first
            use_container_width=True,
            hide_index=True
        )

        # ── Clear Data Button ──
        st.markdown("---")
        if st.button("🗑️ Clear All Mood Data"):
            import os
            if os.path.exists("mood_data.csv"):
                os.remove("mood_data.csv")
            st.session_state.history = []
            st.success("All data cleared!")
            st.rerun()


# ═══════════════════════════════════════════════════════════
# PAGE 3: ABOUT
# ═══════════════════════════════════════════════════════════

elif page == "ℹ️ About MindPulse":

    st.markdown("### ℹ️ About MindPulse AI")

    st.markdown("""
    <div class="mood-card">
        <h3 style="color:#667eea">🧠 What is MindPulse AI?</h3>
        <p style="color:#ccc; line-height:1.8">
        MindPulse AI is a mental health sentiment tracker that uses
        artificial intelligence to understand how you're feeling, provide
        empathetic support, and help you track your emotional wellbeing
        over time. It combines sentiment analysis with Google's Gemini AI
        to give you personalised, caring responses.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mood-card">
        <h3 style="color:#667eea">⚙️ How It Works</h3>
        <p style="color:#ccc; line-height:1.8">
        1. <b>You write</b> how you're feeling in your own words<br>
        2. <b>Sentiment Analysis</b> detects your mood (happy, sad, anxious, angry, neutral)<br>
        3. <b>Gemini AI</b> responds with empathy and personalised advice<br>
        4. <b>Charts</b> track your mood journey over time<br>
        5. <b>Data</b> is saved locally — your privacy is protected
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mood-card">
        <h3 style="color:#667eea">🛠️ Built With</h3>
        <p style="color:#ccc; line-height:1.8">
        🐍 Python &nbsp;|&nbsp;
        🎈 Streamlit &nbsp;|&nbsp;
        🤖 Google Gemini AI &nbsp;|&nbsp;
        💬 TextBlob NLP &nbsp;|&nbsp;
        📊 Plotly Charts &nbsp;|&nbsp;
        🐼 Pandas
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="affirmation-box">
        ⚠️ MindPulse AI is a wellness tool, not a replacement for
        professional mental health care. If you are in crisis,
        please contact a mental health professional or helpline. 💚
    </div>
    """, unsafe_allow_html=True)