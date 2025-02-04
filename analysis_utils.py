import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from typing import List, Dict
import os
from datetime import datetime, timedelta

class JournalAnalyzer:
    def __init__(self, journal_dir: str):
        self.journal_dir = journal_dir

    def load_entries(self) -> List[Dict]:
        """Load and parse all journal entries."""
        entries = []
        for filename in os.listdir(self.journal_dir):
            if filename.startswith('entry_'):
                with open(os.path.join(self.journal_dir, filename), 'r') as f:
                    content = f.read()
                    timestamp = datetime.strptime(
                        filename[6:21], 
                        '%Y%m%d_%H%M%S'
                    )
                    entries.append({
                        'timestamp': timestamp,
                        'content': content
                    })
        return entries

    def generate_mood_analysis(self, entries: List[Dict]) -> str:
        """Analyze mood trends from entries."""
        moods = []
        for entry in entries:
            blob = TextBlob(entry['content'])
            mood = blob.sentiment.polarity
            moods.append({
                'timestamp': entry['timestamp'],
                'mood': mood
            })
        
        df = pd.DataFrame(moods)
        if df.empty:
            return "No entries to analyze yet."
            
        # Create mood trend analysis
        plt.figure(figsize=(10, 6))
        plt.plot(df['timestamp'], df['mood'])
        plt.title('Mood Trend Over Time')
        plt.xlabel('Date')
        plt.ylabel('Mood (Negative to Positive)')
        plt.grid(True)
        
        # Save plot
        plot_path = os.path.join(self.journal_dir, 'mood_trend.png')
        plt.savefig(plot_path)
        plt.close()
        
        # Generate summary
        avg_mood = df['mood'].mean()
        mood_trend = "positive" if avg_mood > 0 else "negative"
        
        return f"""
# 📊 Mood Analysis

## Overall Trend
Your average mood has been {mood_trend} ({avg_mood:.2f})

## Recent Pattern
{self._analyze_recent_pattern(df)}

## 🎯 Suggestion
{self._generate_mood_suggestion(avg_mood)}
"""

    def generate_word_cloud(self, entries: List[Dict]) -> str:
        """Generate word cloud from entries."""
        text = " ".join([entry['content'] for entry in entries])
        
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white'
        ).generate(text)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        
        # Save wordcloud
        cloud_path = os.path.join(self.journal_dir, 'wordcloud.png')
        plt.savefig(cloud_path)
        plt.close()
        
        # Find common themes
        word_freq = wordcloud.words_
        top_themes = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return f"""
# 🔤 Word Analysis

## Common Themes
{self._format_themes(top_themes)}

## 💭 Reflection
These themes might indicate areas of focus in your life.
Consider exploring these topics in your next entry.
"""

    def _analyze_recent_pattern(self, df: pd.DataFrame) -> str:
        """Analyze the pattern in recent entries."""
        recent = df.tail(3)
        if len(recent) < 3:
            return "Not enough entries for pattern analysis."
            
        trend = recent['mood'].diff().mean()
        if trend > 0.1:
            return "Your mood has been improving recently."
        elif trend < -0.1:
            return "Your mood has been slightly declining."
        else:
            return "Your mood has been relatively stable."

    def _generate_mood_suggestion(self, avg_mood: float) -> str:
        """Generate a suggestion based on mood analysis."""
        if avg_mood < -0.2:
            return "Consider focusing on gratitude in your next entries."
        elif avg_mood < 0:
            return "Try reflecting on positive moments, no matter how small."
        elif avg_mood < 0.2:
            return "You're maintaining balance. Consider exploring new perspectives."
        else:
            return "Great positive outlook! Document what's working well."

    def _format_themes(self, themes: List[tuple]) -> str:
        """Format themes for display."""
        return "\n".join([
            f"* **{theme[0]}** - appears frequently in your entries"
            for theme in themes
        ])