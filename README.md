# AutoThreatX
###Automated Automotive Cyber Attack Tree Generation & Validation System


AutoThreatX is a final-year academic project that automates the generation of structured
automotive cyber attack trees using controlled LLM assistance and explicit rule-based validation.

---

## What It Does

- Generates automotive attack trees from predefined surface goals
- Uses LLMs (GPT-4, LLaMA) to assist hierarchical expansion
- Applies deterministic rule-based validation with scoring
- Discards invalid or non-relevant attack nodes automatically
- Stores validated attack trees as structured JSON documents in MongoDB
- Visualizes attack trees using Mermaid.js (initial implementation)

---

## Key Design Choices

- LLMs are used **only for node expansion**, not decision-making
- All generated nodes are validated using explicit rules
- Validation score thresholds control node approval
- Focus on structured, goal-oriented, automotive-relevant attack trees

---

## Tech Stack

- Python
- GPT-4, LLaMA (Groq API)
- MongoDB
- Gradio, Streamlit
- Render (demo)

---

## Academic Context

Developed as a **final-year academic project**, extended from undergraduate research
on systematic and controlled attack tree modeling for automotive cybersecurity.
