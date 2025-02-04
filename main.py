import os
import json
import requests
import datetime
from typing import Dict, List, Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv
from analysis_utils import JournalAnalyzer

# Load environment variables
load_dotenv()

class JournalAssistant:
    def __init__(self):
        """Initialize the journal assistant with configuration."""
        # Load configuration from environment variables
        self.base_url = os.getenv('OLLAMA_API_URL')
        self.model_name = os.getenv('OLLAMA_MODEL')
        self.journal_dir = os.getenv('JOURNAL_DIR', 'journal_entries')
        
        # Validate required configuration
        if not self.base_url or not self.model_name:
            raise ValueError("OLLAMA_API_URL and OLLAMA_MODEL must be set in .env file")
        
        # Initialize Rich console for formatting
        self.console = Console()
        
        # Create journal directory if it doesn't exist
        os.makedirs(self.journal_dir, exist_ok=True)
        
        # Initialize analyzer
        self.analyzer = JournalAnalyzer(self.journal_dir)
        
        # Load system prompt
        self._load_system_prompt()

    def _load_system_prompt(self):
        """Load the system prompt from file."""
        try:
            with open("system_prompt.txt", "r") as f:
                self.system_prompt = f.read()
        except Exception as e:
            self.console.print("[yellow]Warning: Could not load system prompt file[/yellow]")
            self.system_prompt = "You are a journaling assistant."

    def save_entry(self, content: str):
        """Save a journal entry with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.journal_dir}/entry_{timestamp}.md"
        
        try:
            with open(filename, "w") as f:
                f.write(content)
            return filename
        except Exception as e:
            self.console.print(f"[red]Error saving entry: {e}[/red]")
            return None

    def generate_response(self, user_input: str) -> str:
        """Generate AI response using Ollama."""
        try:
            # Prepare the prompt
            prompt = f"""{self.system_prompt}

User: {user_input}
Assistant:"""

            # Make API request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return "I'm having trouble connecting to the AI model. Let's try again."
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def format_response(self, response: str):
        """Format and display the AI response."""
        try:
            # Create panel with markdown content
            md = Markdown(response)
            panel = Panel(
                md,
                title="🌟 Mukti's Response",
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print(panel)
        except Exception as e:
            # Fallback to simple printing if formatting fails
            print(response)

    def show_help(self):
        """Display help information."""
        help_text = """
# 📝 Journaling Commands and Tips

## Available Commands
* `help` - Show this help message
* `analyze` - Analyze your journal entries
* `exit` - End the journaling session

## Journaling Tips
1. Write freely - there's no "wrong" way to journal
2. Be honest with yourself
3. Don't worry about grammar or spelling
4. Write as much or as little as you want
5. Focus on what matters to you

## Prompt Ideas
* What's on your mind right now?
* What made today special?
* What would you like to achieve tomorrow?
* What are you grateful for?
* What's challenging you lately?
"""
        self.console.print(Markdown(help_text))

    def analyze_entries(self):
        """Analyze journal entries and show insights."""
        entries = self.analyzer.load_entries()
        if not entries:
            self.console.print("[yellow]No entries found for analysis yet.[/yellow]")
            return

        # Generate and display mood analysis
        mood_analysis = self.analyzer.generate_mood_analysis(entries)
        self.console.print(Markdown(mood_analysis))

        # Generate and display word cloud analysis
        word_analysis = self.analyzer.generate_word_cloud(entries)
        self.console.print(Markdown(word_analysis))

    def run(self):
        """Run the interactive journaling session."""
        # Display welcome message
        welcome_panel = Panel(
            "[bold cyan]Welcome to Mukti - Your AI Journaling Companion![/bold cyan]\n\n"
            "🌟 Let's make today's reflection meaningful and insightful.\n"
            "💭 Type 'help' for commands and tips.\n"
            "✨ Type 'exit' to end the session.",
            title="✍️ Journal Time",
            border_style="cyan"
        )
        self.console.print(welcome_panel)
        
        # Main interaction loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold green]Your thoughts[/bold green]")
                
                # Process commands
                if user_input.lower() == 'exit':
                    self.console.print("\n[bold cyan]Thank you for sharing your thoughts today. Take care! 🌟[/bold cyan]")
                    break
                    
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                    
                elif user_input.lower() == 'analyze':
                    self.analyze_entries()
                    continue
                
                elif not user_input.strip():
                    continue
                
                # Generate and display AI response
                response = self.generate_response(user_input)
                self.format_response(response)
                
                # Save the entry
                entry_content = f"""# Journal Entry

## Your Reflection
{user_input}

## Mukti's Response
{response}

## Timestamp
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
                self.save_entry(entry_content)
                
            except KeyboardInterrupt:
                self.console.print("\n[bold cyan]Goodbye! Keep reflecting and growing! 🌱[/bold cyan]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
                self.console.print("[yellow]Let's continue our conversation...[/yellow]")

if __name__ == "__main__":
    try:
        assistant = JournalAssistant()
        assistant.run()
    except Exception as e:
        Console().print(f"[red]Failed to start Journal Assistant: {str(e)}[/red]")