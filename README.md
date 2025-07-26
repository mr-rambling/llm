An LLM using Google's Gemini with capabilities to call limited functions to read and edit files in its local ./calculator directory.

Called from the function line via uv run main "insert command here" with an optional --verbose tag.

A Gemini API key should be inserted to .env using the variable name 'GEMINI_API_KEY'.