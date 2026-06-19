# charts.py
# This file saves mood data and draws beautiful charts

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

# ─────────────────────────────────────────────
# WHERE WE SAVE MOOD DATA
# A simple CSV file — like a spreadsheet diary
# ─────────────────────────────────────────────

DATA_FILE = "mood_data.csv"


# ─────────────────────────────────────────────
# FUNCTION 1: Save a mood entry
# Called every time user submits how they feel
# ─────────────────────────────────────────────

def save_mood_entry(user_text, mood, score):
    """
    Saves one mood entry to mood_data.csv
    Columns: date, time, text, mood, score
    """

    # Create a new row of data
    new_entry = {
        "date":  datetime.now().strftime("%Y-%m-%d"),
        "time":  datetime.now().strftime("%H:%M"),
        "text":  user_text,
        "mood":  mood,
        "score": score
    }

    # If file exists, load it and add new row
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        new_row = pd.DataFrame([new_entry])
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        # If file doesn't exist yet, create it
        df = pd.DataFrame([new_entry])

    # Save back to CSV
    df.to_csv(DATA_FILE, index=False)
    return df


# ─────────────────────────────────────────────
# FUNCTION 2: Load all saved mood data
# Returns a DataFrame (like a spreadsheet)
# ─────────────────────────────────────────────

def load_mood_data():
    """Loads all saved mood entries from CSV"""

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if not df.empty:
            return df

    # Return empty DataFrame if no data yet
    return pd.DataFrame(
        columns=["date", "time", "text", "mood", "score"]
    )


# ─────────────────────────────────────────────
# MOOD COLORS (consistent across all charts)
# ─────────────────────────────────────────────

MOOD_COLORS = {
    "happy":   "#2ECC71",
    "sad":     "#3498DB",
    "anxious": "#F39C12",
    "angry":   "#E74C3C",
    "neutral": "#95A5A6"
}


# ─────────────────────────────────────────────
# CHART 1: Mood Timeline
# Shows how mood score changed over time
# ─────────────────────────────────────────────

def chart_mood_timeline(df):
    """
    Line chart showing sentiment score over time.
    Green = positive, Red = negative
    """

    if df.empty or len(df) < 2:
        return None

    # Map mood to color for each point
    df["color"] = df["mood"].map(MOOD_COLORS)

    fig = go.Figure()

    # Add the line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["score"],
        mode="lines+markers",
        line=dict(color="#7F8EF7", width=3),
        marker=dict(
            color=df["color"],
            size=12,
            line=dict(color="white", width=2)
        ),
        text=df["mood"],
        hovertemplate=(
            "<b>Mood:</b> %{text}<br>"
            "<b>Score:</b> %{y}<br>"
            "<b>Entry:</b> %{customdata}<extra></extra>"
        ),
        customdata=df["text"].str[:50] + "..."
    ))

    # Add a zero line (neutral baseline)
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        annotation_text="Neutral",
        annotation_position="right"
    )

    fig.update_layout(
        title="📈 Your Mood Journey Over Time",
        xaxis_title="Entry Number",
        yaxis_title="Sentiment Score",
        yaxis=dict(range=[-1.1, 1.1]),
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        title_font=dict(size=18),
        showlegend=False,
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig


# ─────────────────────────────────────────────
# CHART 2: Mood Distribution (Donut Chart)
# Shows how often each mood appears
# ─────────────────────────────────────────────

def chart_mood_distribution(df):
    """
    Donut chart showing percentage of each mood.
    """

    if df.empty:
        return None

    mood_counts = df["mood"].value_counts().reset_index()
    mood_counts.columns = ["mood", "count"]
    mood_counts["color"] = mood_counts["mood"].map(MOOD_COLORS)

    fig = go.Figure(data=[go.Pie(
        labels=mood_counts["mood"].str.capitalize(),
        values=mood_counts["count"],
        hole=0.55,
        marker=dict(colors=mood_counts["color"]),
        textinfo="label+percent",
        textfont=dict(size=14, color="white"),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Count: %{value}<br>"
            "Percentage: %{percent}<extra></extra>"
        )
    )])

    fig.update_layout(
        title="🍩 Mood Distribution",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        title_font=dict(size=18),
        showlegend=True,
        legend=dict(
            font=dict(color="white"),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(t=60, b=20, l=20, r=20),
        annotations=[dict(
            text=f"{len(df)}<br>entries",
            x=0.5, y=0.5,
            font=dict(size=16, color="white"),
            showarrow=False
        )]
    )

    return fig


# ─────────────────────────────────────────────
# CHART 3: Mood Frequency Bar Chart
# Simple bar chart counting each mood
# ─────────────────────────────────────────────

def chart_mood_bar(df):
    """
    Horizontal bar chart of mood frequency.
    """

    if df.empty:
        return None

    mood_counts = df["mood"].value_counts().reset_index()
    mood_counts.columns = ["mood", "count"]
    mood_counts["color"] = mood_counts["mood"].map(MOOD_COLORS)
    mood_counts["emoji"] = mood_counts["mood"].map({
        "happy":   "😊 Happy",
        "sad":     "😢 Sad",
        "anxious": "😰 Anxious",
        "angry":   "😠 Angry",
        "neutral": "😐 Neutral"
    })

    fig = go.Figure(go.Bar(
        x=mood_counts["count"],
        y=mood_counts["emoji"],
        orientation="h",
        marker=dict(
            color=mood_counts["color"],
            line=dict(color="white", width=1)
        ),
        text=mood_counts["count"],
        textposition="outside",
        textfont=dict(color="white", size=14),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Count: %{x}<extra></extra>"
        )
    ))

    fig.update_layout(
        title="📊 How Often Each Mood Appears",
        xaxis_title="Number of Entries",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        title_font=dict(size=18),
        xaxis=dict(gridcolor="#2D2D2D"),
        yaxis=dict(gridcolor="#2D2D2D"),
        margin=dict(t=60, b=40, l=120, r=60)
    )

    return fig


# ─────────────────────────────────────────────
# CHART 4: Daily Average Mood
# Shows average mood score per day
# ─────────────────────────────────────────────

def chart_daily_average(df):
    """
    Bar chart of average sentiment score per day.
    Green bars = positive days, Red bars = negative days.
    """

    if df.empty or "date" not in df.columns:
        return None

    daily = df.groupby("date")["score"].mean().reset_index()
    daily.columns = ["date", "avg_score"]
    daily["avg_score"] = daily["avg_score"].round(2)

    # Color each bar based on positive/negative
    daily["color"] = daily["avg_score"].apply(
        lambda s: "#2ECC71" if s >= 0.1
        else "#E74C3C" if s <= -0.1
        else "#95A5A6"
    )

    fig = go.Figure(go.Bar(
        x=daily["date"],
        y=daily["avg_score"],
        marker=dict(color=daily["color"]),
        text=daily["avg_score"],
        textposition="outside",
        textfont=dict(color="white"),
        hovertemplate=(
            "<b>Date:</b> %{x}<br>"
            "<b>Avg Score:</b> %{y}<extra></extra>"
        )
    ))

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray"
    )

    fig.update_layout(
        title="📅 Daily Average Mood Score",
        xaxis_title="Date",
        yaxis_title="Average Score",
        yaxis=dict(range=[-1.1, 1.1], gridcolor="#2D2D2D"),
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        title_font=dict(size=18),
        xaxis=dict(gridcolor="#2D2D2D"),
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig


# ─────────────────────────────────────────────
# FUNCTION: Get mood summary stats
# Shows quick numbers at the top of the app
# ─────────────────────────────────────────────

def get_mood_summary(df):
    """
    Returns a dictionary of summary statistics
    shown as metric cards in the app.
    """

    if df.empty:
        return None

    total    = len(df)
    avg      = round(df["score"].mean(), 2)
    dominant = df["mood"].value_counts().idxmax()
    latest   = df["mood"].iloc[-1]

    # Streak: count how many recent entries share the same mood
    streak = 1
    for i in range(len(df) - 2, -1, -1):
        if df["mood"].iloc[i] == latest:
            streak += 1
        else:
            break

    return {
        "total_entries": total,
        "average_score": avg,
        "dominant_mood": dominant,
        "latest_mood":   latest,
        "streak":        streak
    }


# ─────────────────────────────────────────────
# TEST: Run this file directly to test it
# Type in terminal: python charts.py
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n📊 MindPulse Charts Tester\n" + "─" * 40)

    # Create some fake test data
    test_entries = [
        ("I feel amazing today!", "happy", 0.8),
        ("Feeling a bit anxious", "anxious", -0.2),
        ("Really sad and lonely", "sad", -0.6),
        ("Just a normal day", "neutral", 0.0),
        ("So happy and grateful!", "happy", 0.9),
    ]

    for text, mood, score in test_entries:
        save_mood_entry(text, mood, score)
        print(f"✅ Saved: [{mood}] {text}")

    df = load_mood_data()
    print(f"\n📁 Total entries saved: {len(df)}")

    summary = get_mood_summary(df)
    print(f"\n📈 Summary Stats:")
    print(f"   Total entries : {summary['total_entries']}")
    print(f"   Average score : {summary['average_score']}")
    print(f"   Dominant mood : {summary['dominant_mood']}")
    print(f"   Latest mood   : {summary['latest_mood']}")
    print(f"   Current streak: {summary['streak']} entries")
    print("\n✅ Charts module working correctly!")