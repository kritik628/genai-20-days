## Day 01 – LLM Basics & JSON Control

### What I learned
- How Large Language Models generate text (token-based prediction)
- Difference between system prompts and user prompts
- Role of temperature in controlling randomness
- Why LLMs struggle with strict JSON output

### What I built
- Connected to Google Gemini using the latest `google.genai` SDK
- Implemented a reusable LLM function in Python
- Enforced strict JSON output
- Handled markdown-wrapped JSON responses
- Added robust error handling for invalid outputs

### Key Engineering Insight
LLMs generate text probabilistically and do not enforce syntax rules, so structured outputs like JSON must be validated programmatically.
