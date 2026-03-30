"""
AI-powered call analysis module.
Uses Claude API to extract insights from call transcripts.
Falls back to rule-based analysis if no API key is configured.
"""

import json
import re


def analyze_call_with_rules(call: dict) -> dict:
    """
    Rule-based fallback analysis when Claude API is not available.
    """
    transcript = call["transcript"].lower()

    # Sentiment detection
    negative_words = ["frustrated", "angry", "upset", "cancel", "problem", "broken",
                      "issue", "complaint", "terrible", "worst", "horrible", "annoying",
                      "nothing but problems", "gave up", "serious issue", "disappear",
                      "lose it", "can't"]
    positive_words = ["thank", "appreciate", "great", "perfect", "excellent", "happy",
                      "love", "wonderful", "good", "helpful", "best", "saved",
                      "reasonable", "exactly what"]
    neg_count = sum(1 for w in negative_words if w in transcript)
    pos_count = sum(1 for w in positive_words if w in transcript)

    if neg_count > pos_count + 2:
        sentiment = "Negative"
        sentiment_score = max(0.1, 0.5 - (neg_count - pos_count) * 0.1)
    elif pos_count > neg_count + 1:
        sentiment = "Positive"
        sentiment_score = min(0.95, 0.5 + (pos_count - neg_count) * 0.1)
    else:
        sentiment = "Neutral"
        sentiment_score = 0.5

    # Issue categorization
    categories = {
        "Billing Dispute": ["charge", "refund", "invoice", "payment", "duplicate", "double charge", "overcharg"],
        "Technical Issue": ["error", "bug", "broken", "can't log in", "doesn't work", "not working", "crash",
                           "session expired", "disappeared", "blank"],
        "Account Management": ["cancel", "upgrade", "downgrade", "plan", "subscription", "seats"],
        "Product Inquiry": ["how do i", "how to", "export", "feature", "setup", "configure"],
        "Retention / Save": ["cancel", "leaving", "competitor", "discount", "nothing but problems"],
        "Data Issue": ["data", "disappeared", "missing", "lost", "blank", "reports"],
        "Enterprise Sales": ["enterprise", "sso", "compliance", "procurement", "demo"],
    }
    detected_categories = []
    for cat, keywords in categories.items():
        if any(kw in transcript for kw in keywords):
            detected_categories.append(cat)

    # Resolution detection
    resolved_indicators = ["done", "processed", "i'll send", "that worked", "refund", "applied",
                          "removed", "resolved", "data is coming back", "i'm in now", "i see it now"]
    is_resolved = any(ind in transcript for ind in resolved_indicators)

    # Extract action items
    action_items = []
    if "refund" in transcript:
        action_items.append("Process refund for customer")
    if "email" in transcript or "send" in transcript:
        action_items.append("Send follow-up email/documentation to customer")
    if "escalat" in transcript:
        action_items.append("Escalate issue to relevant team")
    if "flag" in transcript or "review" in transcript:
        action_items.append("Flag account for internal review")
    if "discount" in transcript:
        action_items.append("Monitor discounted period and follow up")
    if "proposal" in transcript:
        action_items.append("Send pricing proposal to customer")
    if "demo" in transcript:
        action_items.append("Schedule demo call with stakeholders")
    if "calendar" in transcript:
        action_items.append("Send calendar invite to participants")
    if not action_items:
        action_items.append("No immediate follow-up required")

    # Generate summary
    agent = call["agent"]
    customer = call["customer"]
    queue = call["queue"]
    duration_min = call["duration_seconds"] / 60

    summary = f"Customer {customer} contacted {queue} support. "
    if detected_categories:
        summary += f"Primary issue: {detected_categories[0]}. "
    if is_resolved:
        summary += f"Agent {agent.split()[0]} resolved the issue during the call. "
    else:
        summary += f"Issue requires further follow-up. "

    # Compliance flags
    compliance = []
    if "understand" in transcript or "apologize" in transcript or "sorry" in transcript:
        compliance.append({"check": "Empathy expressed", "passed": True})
    else:
        compliance.append({"check": "Empathy expressed", "passed": False})

    if "anything else" in transcript or "is there anything" in transcript:
        compliance.append({"check": "Offered additional assistance", "passed": True})
    else:
        compliance.append({"check": "Offered additional assistance", "passed": False})

    if "thank" in transcript:
        compliance.append({"check": "Professional closing", "passed": True})
    else:
        compliance.append({"check": "Professional closing", "passed": False})

    if call.get("customer"):
        name_used = call["customer"].split()[-1].lower() in transcript
        compliance.append({"check": "Used customer name", "passed": name_used})

    # CSAT prediction
    if sentiment == "Positive" and is_resolved:
        csat_prediction = 5
    elif sentiment == "Negative" and not is_resolved:
        csat_prediction = 1
    elif sentiment == "Negative" and is_resolved:
        csat_prediction = 3
    elif is_resolved:
        csat_prediction = 4
    else:
        csat_prediction = 2

    # Urgency
    urgent_words = ["immediately", "urgent", "critical", "asap", "right away", "serious",
                    "board presentation", "lose it", "career"]
    urgency = "High" if any(u in transcript for u in urgent_words) else "Normal"

    # Revenue impact
    revenue_impact = None
    if "enterprise" in transcript or "upgrade" in transcript:
        revenue_impact = "Upsell Opportunity"
    elif "cancel" in transcript:
        revenue_impact = "Churn Risk"
    elif "refund" in transcript:
        revenue_impact = "Revenue Recovery"

    return {
        "summary": summary,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "categories": detected_categories if detected_categories else ["General Inquiry"],
        "is_resolved": is_resolved,
        "action_items": action_items,
        "compliance": compliance,
        "csat_prediction": csat_prediction,
        "key_phrases": extract_key_phrases(transcript),
        "duration_min": round(duration_min, 1),
        "urgency": urgency,
        "revenue_impact": revenue_impact,
    }


def extract_key_phrases(transcript: str) -> list:
    """Extract notable phrases from the transcript."""
    phrases = []
    lines = transcript.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("Customer:"):
            content = line.replace("Customer:", "").strip()
            if any(w in content.lower() for w in ["frustrated", "angry", "cancel", "problem",
                                                    "need", "want", "can't", "won't", "never",
                                                    "serious", "disappear", "critical", "urgent",
                                                    "interested", "looking into"]):
                phrases.append(content[:120])
    return phrases[:3]


def analyze_call(call: dict, use_ai: bool = False, api_key: str = None) -> dict:
    """
    Main analysis function. Uses AI if configured, otherwise falls back to rules.
    """
    if use_ai and api_key:
        try:
            return analyze_call_with_ai(call, api_key)
        except Exception as e:
            print(f"AI analysis failed, falling back to rules: {e}")
            return analyze_call_with_rules(call)
    return analyze_call_with_rules(call)


def analyze_call_with_ai(call: dict, api_key: str) -> dict:
    """
    Claude API-powered analysis (requires API key).
    """
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Analyze this contact center call transcript and return a JSON object with these fields:
- summary: 2-3 sentence summary of the call
- sentiment: "Positive", "Negative", or "Neutral"
- sentiment_score: float 0-1 (0=very negative, 1=very positive)
- categories: list of issue categories
- is_resolved: boolean
- action_items: list of follow-up actions needed
- compliance: list of objects with "check" (string) and "passed" (boolean) fields
- csat_prediction: integer 1-5
- key_phrases: list of 2-3 notable customer statements
- urgency: "High" or "Normal"
- revenue_impact: null or one of "Upsell Opportunity", "Churn Risk", "Revenue Recovery"

Call ID: {call['call_id']}
Agent: {call['agent']}
Customer: {call['customer']}
Queue: {call['queue']}
Duration: {call['duration_seconds']} seconds

Transcript:
{call['transcript']}

Return ONLY valid JSON, no markdown formatting."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    result = json.loads(response_text)
    result["duration_min"] = round(call["duration_seconds"] / 60, 1)
    return result
