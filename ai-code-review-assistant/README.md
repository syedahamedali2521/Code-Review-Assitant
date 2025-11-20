# AI-Powered Code Review Assistant

A Streamlit application that provides static code analysis and AI-powered code reviews for Python and JavaScript files.

## Features

- Upload or paste code for Python (.py) or JavaScript (.js) files
- Static analysis: Detects unused variables/imports, code complexity, and common JS issues
- AI-powered review: Uses OpenAI API to suggest improvements
- Modern UI with animations, gradients, and glassmorphism effects
- Downloadable reports
- Confetti celebration for high-quality code

## Setup

1. Clone or download the project.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up OpenAI API key:
   - Get your API key from [OpenAI](https://platform.openai.com/account/api-keys)
   - Set it as an environment variable: `OPENAI_API_KEY=your_key_here`
   - Or edit `functions/ai_review.py` to include your key directly (not recommended for security).

## Running the App

Run the Streamlit app:
```
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Usage

1. Upload a .py or .js file or paste code in the text area.
2. Select the language.
3. Click "Analyze Code" for static analysis.
4. Click "Get AI Review" for AI suggestions (requires API key).
5. View results in tabs.
6. Download the report if desired.

## Dependencies

- streamlit: Web app framework
- radon: Code complexity analysis for Python
- openai: AI API client
- streamlit-lottie: Lottie animations
- requests: HTTP requests (for confetti)
- fpdf: PDF report generation
- esprima: JavaScript parsing (optional, used for advanced JS analysis)

## Notes

- For JS analysis, basic regex checks are used; esprima can be integrated for deeper analysis.
- Lottie animations are placeholders; replace with custom JSON files for better visuals.
- Ensure Python 3.7+ for compatibility.
