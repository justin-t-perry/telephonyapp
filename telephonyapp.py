"""
Contact Center Call Summary Dashboard
Built with Streamlit + Claude AI

A demonstration application that processes contact center call transcripts
and presents AI-extracted insights to agents and supervisors.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from call_data import SAMPLE_CALLS
from analysis import analyze_call

# ─── Page Config ───
st.set_page_config(
    page_title="Call Summary Dashboard",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom Styling ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.3rem 0 0 0;
        opacity: 0.8;
        font-size: 0.95rem;
    }

    .metric-card {
        background: white;
        border: 1px solid #e8ecf1;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .metric-card .label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-top: 0.2rem;
    }

    .sentiment-positive { color: #059669; font-weight: 700; }
    .sentiment-negative { color: #dc2626; font-weight: 700; }
    .sentiment-neutral { color: #d97706; font-weight: 700; }

    .insight-box {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }

    .action-item {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 0.6rem 1rem;
        border-radius: 0 6px 6px 0;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }

    .compliance-item {
        padding: 0.3rem 0;
        font-size: 0.9rem;
    }

    .call-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .call-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 2px 8px rgba(59,130,246,0.15);
    }

    .tag {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 500;
        margin-right: 0.3rem;
        margin-top: 0.3rem;
    }

    .resolved-badge {
        display: inline-block;
        padding: 0.15rem 0.7rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .resolved-yes {
        background: #d1fae5;
        color: #065f46;
    }
    .resolved-no {
        background: #fee2e2;
        color: #991b1b;
    }

    div[data-testid="stSidebar"] {
        background: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ───
st.markdown("""
<div class="main-header">
    <h1>📞 Call Summary Dashboard</h1>
    <p>AI-powered call transcript analysis for contact center agents & supervisors</p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ───
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # API key: check Streamlit secrets first, then allow manual entry
    secret_key = st.secrets.get("ANTHROPIC_API_KEY", "") if hasattr(st, "secrets") else ""

    if secret_key:
        api_key = secret_key
        st.success("🤖 AI Analysis Enabled (via secrets)")
    else:
        api_key = st.text_input(
            "Claude API Key (optional)",
            type="password",
            help="Enter your Anthropic API key to enable AI-powered analysis. Leave blank to use rule-based analysis."
        )
        if api_key:
            st.success("🤖 AI Analysis Enabled")
        else:
            st.info("📊 Using Rule-Based Analysis\n\nAdd a Claude API key for AI-powered insights.")

    use_ai = bool(api_key)

    st.markdown("---")
    st.markdown("### 🔍 Filters")

    # Queue filter
    queues = list(set(c["queue"] for c in SAMPLE_CALLS))
    selected_queues = st.multiselect("Queue", queues, default=queues)

    # Agent filter
    agents = list(set(c["agent"] for c in SAMPLE_CALLS))
    selected_agents = st.multiselect("Agent", agents, default=agents)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#9ca3af; font-size:0.8rem;'>"
        "Built with Streamlit + Claude AI<br>Demo Application"
        "</div>",
        unsafe_allow_html=True
    )

# ─── Filter calls ───
filtered_calls = [
    c for c in SAMPLE_CALLS
    if c["queue"] in selected_queues and c["agent"] in selected_agents
]

# ─── Analyze all calls ───
@st.cache_data
def get_analyses(calls_json: str, use_ai: bool, api_key: str):
    import json
    calls = json.loads(calls_json)
    results = {}
    for call in calls:
        results[call["call_id"]] = analyze_call(call, use_ai=use_ai, api_key=api_key)
    return results

import json
analyses = get_analyses(json.dumps(filtered_calls), use_ai, api_key or "")

# ─── Top-Level Metrics ───
if filtered_calls:
    total_calls = len(filtered_calls)
    resolved_count = sum(1 for a in analyses.values() if a["is_resolved"])
    avg_duration = sum(a["duration_min"] for a in analyses.values()) / total_calls
    sentiment_counts = {}
    for a in analyses.values():
        s = a["sentiment"]
        sentiment_counts[s] = sentiment_counts.get(s, 0) + 1
    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{total_calls}</div>
            <div class="label">Total Calls</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        resolution_pct = round(resolved_count / total_calls * 100)
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{resolution_pct}%</div>
            <div class="label">Resolution Rate</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{avg_duration:.1f}m</div>
            <div class="label">Avg Duration</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        sentiment_class = f"sentiment-{dominant_sentiment.lower()}"
        st.markdown(f"""
        <div class="metric-card">
            <div class="value {sentiment_class}">{dominant_sentiment}</div>
            <div class="label">Dominant Sentiment</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Call List & Detail View ───
    col_list, col_detail = st.columns([1, 2])

    with col_list:
        st.markdown("### 📋 Call Queue")
        selected_call_id = None

        for call in filtered_calls:
            analysis = analyses[call["call_id"]]
            sentiment_emoji = {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}.get(analysis["sentiment"], "⚪")
            resolved_badge = "resolved-yes" if analysis["is_resolved"] else "resolved-no"
            resolved_text = "Resolved" if analysis["is_resolved"] else "Open"

            duration_str = f"{call['duration_seconds'] // 60}:{call['duration_seconds'] % 60:02d}"

            if st.button(
                f"{sentiment_emoji} {call['customer']}  ·  {call['queue']}  ·  {duration_str}",
                key=call["call_id"],
                use_container_width=True
            ):
                st.session_state["selected_call"] = call["call_id"]

        # Default selection
        if "selected_call" not in st.session_state and filtered_calls:
            st.session_state["selected_call"] = filtered_calls[0]["call_id"]

    with col_detail:
        selected_id = st.session_state.get("selected_call")
        if selected_id:
            call = next((c for c in filtered_calls if c["call_id"] == selected_id), None)
            if call:
                analysis = analyses[call["call_id"]]

                # Call header
                st.markdown(f"### 📞 {call['call_id']}")

                # Call metadata
                meta_col1, meta_col2, meta_col3, meta_col4 = st.columns(4)
                meta_col1.metric("Agent", call["agent"])
                meta_col2.metric("Customer", call["customer"])
                meta_col3.metric("Queue", call["queue"])
                meta_col4.metric("Duration", f"{analysis['duration_min']}m")

                st.markdown("---")

                # AI Summary
                st.markdown("#### 💡 AI Summary")
                st.markdown(f'<div class="insight-box">{analysis["summary"]}</div>', unsafe_allow_html=True)

                # Sentiment & Resolution
                sent_col, res_col, csat_col = st.columns(3)
                with sent_col:
                    sentiment_class = f"sentiment-{analysis['sentiment'].lower()}"
                    score_pct = round(analysis["sentiment_score"] * 100)
                    st.markdown(f"**Sentiment**")
                    st.markdown(f'<span class="{sentiment_class}">{analysis["sentiment"]} ({score_pct}%)</span>', unsafe_allow_html=True)
                with res_col:
                    badge_class = "resolved-yes" if analysis["is_resolved"] else "resolved-no"
                    badge_text = "✅ Resolved" if analysis["is_resolved"] else "❌ Unresolved"
                    st.markdown("**Resolution**")
                    st.markdown(f'<span class="resolved-badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)
                with csat_col:
                    st.markdown("**CSAT Prediction**")
                    st.markdown(f"**{analysis['csat_prediction']}**")

                st.markdown("---")

                # Categories
                st.markdown("#### 🏷️ Categories")
                tags_html = " ".join(f'<span class="tag">{cat}</span>' for cat in analysis["categories"])
                st.markdown(tags_html, unsafe_allow_html=True)

                st.markdown("")

                # Action Items
                st.markdown("#### ⚡ Action Items")
                for item in analysis["action_items"]:
                    st.markdown(f'<div class="action-item">→ {item}</div>', unsafe_allow_html=True)

                st.markdown("")

                # Compliance
                st.markdown("#### 🛡️ Compliance Check")
                for item in analysis["compliance"]:
                    st.markdown(f'<div class="compliance-item">{item}</div>', unsafe_allow_html=True)

                # Key Customer Phrases
                if analysis.get("key_phrases"):
                    st.markdown("")
                    st.markdown("#### 🗣️ Key Customer Statements")
                    for phrase in analysis["key_phrases"]:
                        st.markdown(f'> *"{phrase}"*')

                # Expandable transcript
                st.markdown("---")
                with st.expander("📝 View Full Transcript"):
                    lines = call["transcript"].strip().split("\n")
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("Agent:"):
                            st.markdown(f"**🎧 {line}**")
                        elif line.startswith("Customer:"):
                            st.markdown(f"*👤 {line}*")
                        else:
                            st.markdown(line)

else:
    st.warning("No calls match the selected filters. Adjust the filters in the sidebar.")
