# Mukti - AI Journaling Assistant 🌟

Mukti is an AI-powered journaling companion that makes daily reflection engaging, meaningful, and insightful. Using advanced language models, it helps users maintain consistent journaling habits while providing valuable insights and analysis of their entries.

## Features ✨

- 📝 Interactive journaling sessions with AI guidance
- 🎯 Personalized prompts and reflections
- 📊 Mood analysis and tracking
- 🔤 Word cloud and theme analysis
- 💾 Persistent storage of entries
- 🎨 Beautiful terminal formatting
- 📈 Progress visualization

## Prerequisites 🛠️

- Docker
- Ollama server running with your preferred model
- Python 3.8+ (for development)

## Quick Start 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mukti-journal.git
   cd mukti-journal
   ```

2. Set up environment variables:
   ```bash
   cp .env.template .env
   # Edit .env file with your Ollama server details
   ```

3. Build the Docker image:
   ```bash
   docker build -t mukti-journal .
   ```

4. Run the container:
   ```bash
   docker run -it \
     --env-file .env \
     -v $(pwd)/journal_entries:/app/journal_entries \
     mukti-journal
   ```

## Usage 📖

Once started, Mukti provides an interactive interface where you can:

- Write journal entries with AI guidance
- Get personalized prompts
- View insights and patterns
- Analyze mood trends
- Generate word clouds
- Review past entries

### Commands

- Type your thoughts normally for journaling
- Use `help` for journaling tips and prompts
- Use `exit` to end the session

## Directory Structure 📁

```
mukti-journal/
├── main.py               # Main application
├── analysis_utils.py     # Analysis utilities
├── system_prompt.txt     # AI system prompt
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── entrypoint.sh        # Startup script
├── .env.template        # Environment template
└── journal_entries/     # Your journal entries
```

## Configuration ⚙️

Configure the application by setting these environment variables in your `.env` file:

- `OLLAMA_API_URL`: Your Ollama server URL
- `OLLAMA_MODEL`: The model to use (e.g., phi:14b)
- `JOURNAL_DIR`: Directory for storing entries (optional)
- `DEBUG`: Enable debug output (optional)

## Development 🔧

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run without Docker:
   ```bash
   python main.py
   ```

## Features in Detail 🔍

### Journal Analysis
- Sentiment analysis of entries
- Mood tracking over time
- Word frequency analysis
- Theme identification
- Progress visualization

### AI Interaction
- Contextual responses
- Personalized prompts
- Pattern recognition
- Growth tracking
- Engagement maintenance

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Built with Ollama
- Inspired by journaling and psychological best practices
- Uses various open-source Python libraries

## Support 💬

For issues and feature requests, please use the GitHub issues page.

## Disclaimer ⚠️

This is an AI assistant meant to enhance journaling practice. It is not a replacement for professional psychological or therapeutic services.