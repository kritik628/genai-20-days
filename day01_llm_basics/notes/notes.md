### LLM Core Concepts
- LLMs predict the next token based on probability
- They do not reason or verify facts
- Context window limits how much information is remembered

### Why JSON is difficult for LLMs
- LLMs do not understand syntax rules
- Output is token-by-token, not schema-based
- Models may add markdown or extra text

### How I handled JSON issues
- Strict prompting
- Low temperature
- Markdown stripping
- JSON parsing with error handling

### Debugging lessons
- SDK deprecations require API changes
- Environment variables can override `.env`
- Always isolate and test authentication first
