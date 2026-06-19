# sentiment.py
# This file detects the user's mood from their text

from textblob import TextBlob
import nltk

# Download required language data (only runs once)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# ─────────────────────────────────────────────
# MOOD KEYWORDS
# We look for these words to detect specific emotions
# ─────────────────────────────────────────────

MOOD_KEYWORDS = {
    "anxious": [
        "anxious", "anxiety", "nervous", "worried", "panic",
        "stress", "stressed", "overwhelmed", "fear", "scared",
        "tense", "uneasy", "restless"
    ],
    "angry": [
        "angry", "anger", "furious", "annoyed", "irritated",
        "frustrated", "mad", "rage", "upset", "hate"
    ],
    "sad": [
        "sad", "unhappy", "depressed", "depression", "cry",
        "crying", "hopeless", "lonely", "alone", "miserable",
        "heartbroken", "grief", "empty", "numb"
    ],
    "happy": [
        "happy", "joy", "joyful", "excited", "grateful",
        "thankful", "amazing", "wonderful", "great", "fantastic",
        "love", "blessed", "cheerful", "good", "positive"
    ],
    "neutral": []
}


# ─────────────────────────────────────────────
# FUNCTION 1: Analyse sentiment score
# TextBlob gives a score from -1.0 (very negative)
# to +1.0 (very positive). 0 is neutral.
# ─────────────────────────────────────────────

def get_sentiment_score(text):
    """Returns a sentiment polarity score between -1.0 and 1.0"""
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)


# ─────────────────────────────────────────────
# FUNCTION 2: Detect the mood label
# Checks keywords first, then uses the score
# ─────────────────────────────────────────────

def detect_mood(text):
    """
    Returns one of: 'happy', 'sad', 'anxious', 'angry', 'neutral'
    """
    text_lower = text.lower()  # Make everything lowercase for easy matching

    # Step 1: Check for keyword matches
    for mood, keywords in MOOD_KEYWORDS.items():
        for word in keywords:
            if word in text_lower:
                return mood

    # Step 2: If no keywords matched, use the sentiment score
    score = get_sentiment_score(text)

    if score >= 0.3:
        return "happy"
    elif score <= -0.3:
        return "sad"
    else:
        return "neutral"


# ─────────────────────────────────────────────
# FUNCTION 3: Get mood emoji
# Makes the UI more friendly and visual
# ─────────────────────────────────────────────

def get_mood_emoji(mood):
    """Returns an emoji for each mood"""
    emojis = {
        "happy":   "😊",
        "sad":     "😢",
        "anxious": "😰",
        "angry":   "😠",
        "neutral": "😐"
    }
    return emojis.get(mood, "😐")


# ─────────────────────────────────────────────
# FUNCTION 4: Get mood color
# Used to color the charts and UI elements
# ─────────────────────────────────────────────

def get_mood_color(mood):
    """Returns a color for each mood (used in charts)"""
    colors = {
        "happy":   "#2ECC71",   # Green
        "sad":     "#3498DB",   # Blue
        "anxious": "#F39C12",   # Orange
        "angry":   "#E74C3C",   # Red
        "neutral": "#95A5A6"    # Grey
    }
    return colors.get(mood, "#95A5A6")


# ─────────────────────────────────────────────
# FUNCTION 5: Get a quick tip based on mood
# Short suggestion shown immediately to user
# ─────────────────────────────────────────────

def get_quick_tip(mood):
    """Returns a short supportive tip based on detected mood"""
    tips = {
        "happy": (
            "You're doing great! 🌟 Keep that positive energy going. "
            "Consider sharing your joy with someone you care about."
        ),
        "sad": (
            "It's okay to feel sad. 💙 Be gentle with yourself today. "
            "Try to do one small thing that usually comforts you."
        ),
        "anxious": (
            "Take a slow deep breath. 🌬️ Breathe in for 4 counts, "
            "hold for 4, out for 4. You are safe right now."
        ),
        "angry": (
            "Your feelings are valid. 🌊 Try stepping away for 5 minutes. "
            "A short walk or cold water can help reset your mind."
        ),
        "neutral": (
            "You seem balanced today. 🌿 A great time to reflect, "
            "journal, or set a small goal for yourself."
        ),
    }
    return tips.get(mood, "Take care of yourself today. 💚")


# ─────────────────────────────────────────────
# TEST: Run this file directly to test it
# Type in terminal: python sentiment.py
# ─────────────────────────────────────────────

if __name__ == "__main__":
    test_inputs = [
        "I am feeling really anxious about my exams",
        "Today was absolutely wonderful, I feel so happy!",
        "I feel so sad and alone lately",
        "I am furious about what happened",
        "Just another regular day, nothing special"
    ]

    print("\n🧠 MindPulse Sentiment Tester\n" + "─" * 40)
    for text in test_inputs:
        mood  = detect_mood(text)
        score = get_sentiment_score(text)
        emoji = get_mood_emoji(mood)
        print(f"\n📝 Input : {text}")
        print(f"🎭 Mood  : {emoji} {mood.upper()}")
        print(f"📊 Score : {score}")