# gemini_helper.py
# This file connects to Gemini AI and gets caring responses

import google.generativeai as genai
from dotenv import load_dotenv
import os

# ─────────────────────────────────────────────
# LOAD YOUR SECRET API KEY
# This reads the key from your .env file safely
# ─────────────────────────────────────────────

load_dotenv()  # Loads the .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Reads the key

# Configure Gemini with your API key
genai.configure(api_key=GOOGLE_API_KEY)

# ─────────────────────────────────────────────
# SET UP THE GEMINI MODEL
# We use gemini-1.5-flash — it's fast and free!
# ─────────────────────────────────────────────

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.85,      # 0 = very factual, 1 = very creative
        "top_p": 0.95,            # Controls response variety
        "max_output_tokens": 500, # Max length of response
    }
)


# ─────────────────────────────────────────────
# THE SYSTEM PERSONALITY
# This tells Gemini HOW to behave — like a
# caring mental health companion, not a robot
# ─────────────────────────────────────────────

SYSTEM_PERSONALITY = """
You are MindPulse AI — a warm, empathetic, and supportive mental health companion.

Your role:
- Listen carefully to how the user is feeling
- Respond with genuine empathy and compassion
- Offer practical, science-backed coping strategies
- Keep responses warm, human, and conversational
- Never be clinical, cold, or robotic
- Always validate the user's feelings first before giving advice
- Keep responses concise (3-5 sentences max) unless the user needs more

Important rules:
- You are NOT a replacement for professional therapy
- If someone mentions self-harm or crisis, always recommend professional help
- Never diagnose any mental health condition
- Always end with one gentle, actionable suggestion

Tone: Warm, caring, like a wise and kind friend.
"""


# ─────────────────────────────────────────────
# FUNCTION 1: Get AI response for a mood entry
# This is called when user submits how they feel
# ─────────────────────────────────────────────

def get_ai_response(user_text, detected_mood):
    """
    Takes the user's text and detected mood,
    returns a caring AI response from Gemini.
    """

    # Build a detailed prompt for Gemini
    prompt = f"""
{SYSTEM_PERSONALITY}

---

The user has shared how they are feeling today.
Their detected mood is: {detected_mood.upper()}

What they wrote:
\"{user_text}\"

Please respond to them in a warm, supportive way based on their mood.
Acknowledge their feelings, then offer one gentle helpful suggestion.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # If something goes wrong, return a safe fallback message
        return (
            "I'm here for you. 💚 Whatever you're feeling right now is valid. "
            "Take a moment to breathe and be kind to yourself. "
            f"\n\n_(Note: AI connection issue — {str(e)})_"
        )


# ─────────────────────────────────────────────
# FUNCTION 2: Get coping strategies by mood
# Returns a structured list of tips for the mood
# ─────────────────────────────────────────────

def get_coping_strategies(mood):
    """
    Returns a list of 4 coping strategies
    tailored to the user's current mood.
    """

    prompt = f"""
{SYSTEM_PERSONALITY}

---

A user is feeling: {mood.upper()}

Give exactly 4 short, practical coping strategies for this mood.
Format your response EXACTLY like this (no extra text):
1. [strategy one]
2. [strategy two]
3. [strategy three]
4. [strategy four]

Each strategy should be one sentence, warm and actionable.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # Fallback strategies if API fails
        fallback = {
            "happy": (
                "1. Share your positivity with someone you love\n"
                "2. Write down what made you happy today\n"
                "3. Do something creative to celebrate\n"
                "4. Set a new goal while your energy is high"
            ),
            "sad": (
                "1. Allow yourself to feel without judgment\n"
                "2. Reach out to a trusted friend or family member\n"
                "3. Take a gentle walk outside for 10 minutes\n"
                "4. Write your feelings in a journal"
            ),
            "anxious": (
                "1. Try box breathing — 4 counts in, hold, out, hold\n"
                "2. Ground yourself — name 5 things you can see\n"
                "3. Write down your worries to get them out of your head\n"
                "4. Limit caffeine and drink a glass of cold water"
            ),
            "angry": (
                "1. Step away from the situation for 5 minutes\n"
                "2. Do 10 jumping jacks to release physical tension\n"
                "3. Write an unsent letter expressing your feelings\n"
                "4. Splash cold water on your face to reset your nervous system"
            ),
            "neutral": (
                "1. Use this calm moment to reflect on your week\n"
                "2. Try a 5-minute meditation or breathing exercise\n"
                "3. Do something small that brings you joy\n"
                "4. Connect with a friend or family member today"
            ),
        }
        return fallback.get(mood, fallback["neutral"])


# ─────────────────────────────────────────────
# FUNCTION 3: Generate a daily affirmation
# A positive message to encourage the user
# ─────────────────────────────────────────────

def get_daily_affirmation(mood):
    """Returns a short positive affirmation based on mood"""

    prompt = f"""
Write ONE short, powerful affirmation (1-2 sentences) for someone feeling {mood}.
Make it warm, genuine, and uplifting. No quotation marks. Just the affirmation.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception:
        affirmations = {
            "happy":   "Your joy is contagious and you deserve every good thing coming your way.",
            "sad":     "This feeling is temporary. You are stronger than you know, and brighter days are ahead.",
            "anxious": "You have survived every hard moment so far. You are safe, capable, and enough.",
            "angry":   "Your feelings are valid. You have the wisdom to respond, not react.",
            "neutral": "Every day is a fresh start. Small steps forward still count as progress.",
        }
        return affirmations.get(mood, "You are enough, exactly as you are. 💚")


# ─────────────────────────────────────────────
# TEST: Run this file directly to test it
# Type in terminal: python gemini_helper.py
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🤖 MindPulse Gemini AI Tester\n" + "─" * 40)

    test_text = "I have been feeling really anxious about my hackathon presentation"
    test_mood = "anxious"

    print(f"\n📝 Input : {test_text}")
    print(f"🎭 Mood  : {test_mood}")

    print("\n💬 AI Response:")
    print(get_ai_response(test_text, test_mood))

    print("\n🛠️ Coping Strategies:")
    print(get_coping_strategies(test_mood))

    print("\n✨ Daily Affirmation:")
    print(get_daily_affirmation(test_mood))