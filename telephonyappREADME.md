# 📞 Contact Center Call Summary Dashboard

An AI-powered dashboard that processes contact center call transcripts and presents actionable insights to agents and supervisors. Built with **Python**, **Streamlit**, and **Claude AI**.

---

## What It Does

This application takes telephone call transcripts and extracts:

- **AI Summaries** — Concise 2-3 sentence call summaries
- **Sentiment Analysis** — Customer sentiment scoring (Positive / Neutral / Negative)
- **Issue Categorization** — Automatic tagging (Billing, Technical, Sales, etc.)
- **Action Items** — Follow-up tasks extracted from the conversation
- **Compliance Checks** — Empathy statements, professional closing, verification
- **CSAT Prediction** — Predicted customer satisfaction score
- **Key Customer Phrases** — Notable statements flagged for review

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
streamlit run app.py

# 3. (Optional) Add your Claude API key in the sidebar for AI-powered analysis
```

The app runs out of the box with **rule-based analysis** using sample call data. Add a Claude API key in the sidebar to enable full AI-powered analysis.

## Project Structure

```
├── app.py              # Main Streamlit dashboard
├── analysis.py         # AI + rule-based call analysis engine
├── call_data.py        # Sample call transcript data
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## How It Was Built

This project was built using **Claude Code**, Anthropic's command-line agentic coding tool. The workflow:

1. Described the application requirements to Claude Code
2. Claude Code generated the project structure, sample data, analysis engine, and UI
3. Iterated on the design and features through conversation
4. Final output: a working, production-style dashboard

## Architecture Highlights

- **Dual analysis modes**: Rule-based (no API key needed) and AI-powered (with Claude API)
- **Cached analysis**: Uses `@st.cache_data` to avoid re-processing
- **Modular design**: Data, analysis, and UI are cleanly separated
- **Extensible**: Easy to add new analysis dimensions or connect to real telephony data

## Connecting to Real Data

In production, `call_data.py` would be replaced with connectors to:
- Call recording platforms (e.g., NICE, Genesys, Five9)
- Speech-to-text services (e.g., AWS Transcribe, Google Speech-to-Text)
- CRM systems (e.g., Salesforce, HubSpot)

---

*Built as a demonstration of Claude Code for rapid AI application development.*
