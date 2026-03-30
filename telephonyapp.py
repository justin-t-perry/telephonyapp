"""
Contact Center Call Summary Dashboard
Built with Streamlit + Claude AI

A demonstration application that processes contact center call transcripts
and presents AI-extracted insights to agents and supervisors.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

from telephonyappcall_data import SAMPLE_CALLS
from telephonyappanalysis import analyze_call

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

    .stApp { font-family: 'DM Sans', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; }
    .main-header p { margin: 0.3rem 0 0 0; opacity: 0.8; font-size: 0.95rem; }

    .metric-card {
        background: white; border: 1px solid #e8ecf1; border-radius: 10px;
        padding: 1.2rem; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .metric-card .value { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; }
    .metric-card .label { font-size: 0.82rem; color: #6b7280; margin-top: 0.2rem; }

    .sentiment-positive { color: #059669; font-weight: 700; }
    .sentiment-negative { color: #dc2626; font-weight: 700; }
    .sentiment-neutral { color: #d97706; font-weight: 700; }

    .insight-box {
        background: #f8fafc; border-left: 4px solid #3b82f6;
        padding: 1rem 1.2rem; border-radius: 0 8px 8px 0; margin: 0.5rem 0;
    }
    .action-item {
        background: #fffbeb; border-left: 4px solid #f59e0b;
        padding: 0.6rem 1rem; border-radius: 0 6px 6px 0; margin: 0.3rem 0; font-size: 0.9rem;
    }
    .tag {
        display: inline-block; background: #e0e7ff; color: #3730a3;
        padding: 0.15rem 0.6rem; border-radius: 20px; font-size: 0.78rem;
        font-weight: 500; margin-right: 0.3rem; margin-top: 0.3rem;
    }
    .tag-urgent {
        display: inline-block; background: #fee2e2; color: #991b1b;
        padding: 0.15rem 0.6rem; border-radius: 20px; font-size: 0.78rem;
        font-weight: 600; margin-right: 0.3rem; margin-top: 0.3rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    .tag-revenue {
        display: inline-block; padding: 0.15rem 0.6rem; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600; margin-right: 0.3rem; margin-top: 0.3rem;
    }
    .tag-upsell { background: #d1fae5; color: #065f46; }
    .tag-churn { background: #fee2e2; color: #991b1b; }
    .tag-recovery { background: #fef3c7; color: #92400e; }

    .resolved-badge {
        display: inline-block; padding: 0.15rem 0.7rem; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600;
    }
    .resolved-yes { background: #d1fae5; color: #065f46; }
    .resolved-no { background: #fee2e2; color: #991b1b; }

    .star-filled { color: #f59e0b; }
    .star-empty { color: #d1d5db; }

    .transcript-agent {
        background: #eff6ff; padding: 0.5rem 0.8rem; border-radius: 8px;
        margin: 0.3rem 0; border-left: 3px solid #3b82f6;
    }
    .transcript-customer {
        background: #f0fdf4; padding: 0.5rem 0.8rem; border-radius: 8px;
        margin: 0.3rem 0; border-left: 3px solid #22c55e;
    }

    div[data-testid="stSidebar"] { background: #f8fafc; }
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

    secret_key = ""
    try:
        secret_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        pass

    if secret_key:
        api_key = secret_key
        st.success("🤖 AI Analysis Enabled (via secrets)")
    else:
        api_key = st.text_input(
            "Claude API Key (optional)", type="password",
            help="Enter your Anthropic API key for AI-powered analysis. Leave blank for rule-based analysis."
        )
        if api_key:
            st.success("🤖 AI Analysis Enabled")
        else:
            st.info("📊 Rule-Based Analysis\n\nAdd a Claude API key for AI-powered insights.")

    use_ai = bool(api_key)

    st.markdown("---")
    st.markdown("### 🔍 Filters")

    queues = sorted(set(c["queue"] for c in SAMPLE_CALLS))
    selected_queues = st.multiselect("Queue", queues, default=queues)

    agents = sorted(set(c["agent"] for c in SAMPLE_CALLS))
    selected_agents = st.multiselect("Agent", agents, default=agents)

    sentiment_filter = st.multiselect(
        "Sentiment", ["Positive", "Neutral", "Negative"],
        default=["Positive", "Neutral", "Negative"]
    )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#9ca3af; font-size:0.8rem;'>"
        "Built with Streamlit + Claude AI<br>Demo Application v2.0"
        "</div>", unsafe_allow_html=True
    )

# ─── Analyze all calls (cached) ───
@st.cache_data
def get_all_analyses(calls_json: str, use_ai: bool, api_key: str):
    calls = json.loads(calls_json)
    results = {}
    for call in calls:
        results[call["call_id"]] = analyze_call(call, use_ai=use_ai, api_key=api_key)
    return results

all_analyses = get_all_analyses(json.dumps(SAMPLE_CALLS), use_ai, api_key or "")

# ─── Apply filters ───
filtered_calls = [
    c for c in SAMPLE_CALLS
    if c["queue"] in selected_queues
    and c["agent"] in selected_agents
    and all_analyses[c["call_id"]]["sentiment"] in sentiment_filter
]
analyses = {c["call_id"]: all_analyses[c["call_id"]] for c in filtered_calls}

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT AREA — TABS
# ═══════════════════════════════════════════════════════════════

tab_calls, tab_analytics, tab_agents, tab_try = st.tabs([
    "📋 Call Review", "📊 Analytics", "👥 Agent Leaderboard", "🧪 Try It Yourself"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1: CALL REVIEW
# ═══════════════════════════════════════════════════════════════
with tab_calls:
    if not filtered_calls:
        st.warning("No calls match the selected filters.")
    else:
        # ─── Top metrics ───
        total = len(filtered_calls)
        resolved = sum(1 for a in analyses.values() if a["is_resolved"])
        avg_dur = sum(a["duration_min"] for a in analyses.values()) / total
        avg_csat = sum(a["csat_prediction"] for a in analyses.values()) / total
        high_urgency = sum(1 for a in analyses.values() if a.get("urgency") == "High")

        c1, c2, c3, c4, c5 = st.columns(5)
        for col, val, label in [
            (c1, str(total), "Total Calls"),
            (c2, f"{round(resolved/total*100)}%", "Resolution Rate"),
            (c3, f"{avg_dur:.1f}m", "Avg Duration"),
            (c4, f"{'⭐' * round(avg_csat)}", "Avg CSAT"),
            (c5, str(high_urgency), "🔴 Urgent"),
        ]:
            with col:
                st.markdown(f'<div class="metric-card"><div class="value">{val}</div>'
                           f'<div class="label">{label}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ─── Call list + detail ───
        col_list, col_detail = st.columns([1, 2])

        with col_list:
            st.markdown("#### Select a Call")
            for call in filtered_calls:
                a = analyses[call["call_id"]]
                emoji = {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}.get(a["sentiment"], "⚪")
                dur = f"{call['duration_seconds']//60}:{call['duration_seconds']%60:02d}"
                urgent = " 🚨" if a.get("urgency") == "High" else ""
                label = f"{emoji} {call['customer']}  ·  {call['queue']}  ·  {dur}{urgent}"
                if st.button(label, key=call["call_id"], use_container_width=True):
                    st.session_state["selected_call"] = call["call_id"]

            if "selected_call" not in st.session_state and filtered_calls:
                st.session_state["selected_call"] = filtered_calls[0]["call_id"]

        with col_detail:
            sel_id = st.session_state.get("selected_call")
            call = next((c for c in filtered_calls if c["call_id"] == sel_id), None)
            if call:
                a = analyses[call["call_id"]]

                st.markdown(f"### 📞 {call['call_id']}")

                # Metadata row
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("Agent", call["agent"])
                m2.metric("Customer", call["customer"])
                m3.metric("Queue", call["queue"])
                m4.metric("Duration", f"{a['duration_min']}m")
                m5.metric("Tier", call.get("customer_tier", "—"))

                # Tags row
                tags = ""
                for cat in a["categories"]:
                    tags += f'<span class="tag">{cat}</span> '
                if a.get("urgency") == "High":
                    tags += '<span class="tag-urgent">🚨 URGENT</span> '
                if a.get("revenue_impact"):
                    ri = a["revenue_impact"]
                    cls = {"Upsell Opportunity": "tag-upsell", "Churn Risk": "tag-churn",
                           "Revenue Recovery": "tag-recovery"}.get(ri, "")
                    tags += f'<span class="tag-revenue {cls}">💰 {ri}</span>'
                st.markdown(tags, unsafe_allow_html=True)

                st.markdown("---")

                # AI Summary
                st.markdown("#### 💡 AI Summary")
                st.markdown(f'<div class="insight-box">{a["summary"]}</div>', unsafe_allow_html=True)

                # Sentiment / Resolution / CSAT row
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    s_class = f"sentiment-{a['sentiment'].lower()}"
                    pct = round(a["sentiment_score"] * 100)
                    st.markdown("**Sentiment**")
                    st.markdown(f'<span class="{s_class}">{a["sentiment"]} ({pct}%)</span>', unsafe_allow_html=True)
                    st.progress(a["sentiment_score"])
                with sc2:
                    badge = "resolved-yes" if a["is_resolved"] else "resolved-no"
                    txt = "✅ Resolved" if a["is_resolved"] else "❌ Unresolved"
                    st.markdown("**Resolution**")
                    st.markdown(f'<span class="resolved-badge {badge}">{txt}</span>', unsafe_allow_html=True)
                with sc3:
                    stars = '<span class="star-filled">★</span>' * a["csat_prediction"] + \
                            '<span class="star-empty">★</span>' * (5 - a["csat_prediction"])
                    st.markdown("**Predicted CSAT**")
                    st.markdown(stars, unsafe_allow_html=True)

                st.markdown("---")

                # Action items + Compliance side by side
                ac1, ac2 = st.columns(2)
                with ac1:
                    st.markdown("#### ⚡ Action Items")
                    for item in a["action_items"]:
                        st.markdown(f'<div class="action-item">→ {item}</div>', unsafe_allow_html=True)
                with ac2:
                    st.markdown("#### 🛡️ Compliance")
                    for c_item in a["compliance"]:
                        icon = "✅" if c_item["passed"] else "⚠️"
                        st.markdown(f"{icon} {c_item['check']}")

                # Key phrases
                if a.get("key_phrases"):
                    st.markdown("---")
                    st.markdown("#### 🗣️ Key Customer Statements")
                    for phrase in a["key_phrases"]:
                        st.markdown(f'> *"{phrase}"*')

                # Transcript
                st.markdown("---")
                with st.expander("📝 View Full Transcript", expanded=False):
                    lines = call["transcript"].strip().split("\n")
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("Agent:"):
                            st.markdown(f'<div class="transcript-agent"><strong>🎧 Agent:</strong> {line[6:].strip()}</div>',
                                       unsafe_allow_html=True)
                        elif line.startswith("Customer:"):
                            st.markdown(f'<div class="transcript-customer"><strong>👤 Customer:</strong> {line[9:].strip()}</div>',
                                       unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2: ANALYTICS
# ═══════════════════════════════════════════════════════════════
with tab_analytics:
    if not filtered_calls:
        st.warning("No calls match the selected filters.")
    else:
        st.markdown("### 📊 Call Analytics Overview")
        st.markdown("")

        chart1, chart2 = st.columns(2)

        with chart1:
            # Sentiment distribution
            st.markdown("#### Sentiment Distribution")
            sent_data = {"Positive": 0, "Neutral": 0, "Negative": 0}
            for a in analyses.values():
                sent_data[a["sentiment"]] += 1
            df_sent = pd.DataFrame({
                "Sentiment": list(sent_data.keys()),
                "Count": list(sent_data.values())
            })
            st.bar_chart(df_sent.set_index("Sentiment"), color="#3b82f6")

        with chart2:
            # Calls by queue
            st.markdown("#### Calls by Queue")
            queue_counts = {}
            for c in filtered_calls:
                queue_counts[c["queue"]] = queue_counts.get(c["queue"], 0) + 1
            df_queue = pd.DataFrame({
                "Queue": list(queue_counts.keys()),
                "Count": list(queue_counts.values())
            })
            st.bar_chart(df_queue.set_index("Queue"), color="#8b5cf6")

        chart3, chart4 = st.columns(2)

        with chart3:
            # Duration per call
            st.markdown("#### Call Duration (minutes)")
            dur_data = pd.DataFrame({
                "Call": [c["call_id"].split("-")[-1] for c in filtered_calls],
                "Duration": [analyses[c["call_id"]]["duration_min"] for c in filtered_calls]
            })
            st.bar_chart(dur_data.set_index("Call"), color="#10b981")

        with chart4:
            # CSAT predictions
            st.markdown("#### Predicted CSAT Scores")
            csat_data = pd.DataFrame({
                "Call": [c["customer"].split()[0] for c in filtered_calls],
                "CSAT": [analyses[c["call_id"]]["csat_prediction"] for c in filtered_calls]
            })
            st.bar_chart(csat_data.set_index("Call"), color="#f59e0b")

        # Category breakdown
        st.markdown("---")
        st.markdown("#### 🏷️ Issue Category Breakdown")
        cat_counts = {}
        for a in analyses.values():
            for cat in a["categories"]:
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
        df_cats = pd.DataFrame({
            "Category": list(cat_counts.keys()),
            "Count": list(cat_counts.values())
        }).sort_values("Count", ascending=False)
        st.bar_chart(df_cats.set_index("Category"), color="#ec4899")

        # Revenue impact summary
        st.markdown("---")
        st.markdown("#### 💰 Revenue Impact Summary")
        ri_c1, ri_c2, ri_c3 = st.columns(3)
        upsell = sum(1 for a in analyses.values() if a.get("revenue_impact") == "Upsell Opportunity")
        churn = sum(1 for a in analyses.values() if a.get("revenue_impact") == "Churn Risk")
        recovery = sum(1 for a in analyses.values() if a.get("revenue_impact") == "Revenue Recovery")
        ri_c1.metric("📈 Upsell Opportunities", upsell)
        ri_c2.metric("⚠️ Churn Risks", churn)
        ri_c3.metric("💵 Revenue Recovery", recovery)

# ═══════════════════════════════════════════════════════════════
# TAB 3: AGENT LEADERBOARD
# ═══════════════════════════════════════════════════════════════
with tab_agents:
    st.markdown("### 👥 Agent Performance Leaderboard")
    st.markdown("")

    # Aggregate per agent
    agent_stats = {}
    for call in SAMPLE_CALLS:
        agent = call["agent"]
        a = all_analyses[call["call_id"]]
        if agent not in agent_stats:
            agent_stats[agent] = {
                "calls": 0, "resolved": 0, "total_duration": 0,
                "total_csat": 0, "compliance_passed": 0, "compliance_total": 0,
                "sentiments": []
            }
        s = agent_stats[agent]
        s["calls"] += 1
        s["resolved"] += 1 if a["is_resolved"] else 0
        s["total_duration"] += a["duration_min"]
        s["total_csat"] += a["csat_prediction"]
        s["sentiments"].append(a["sentiment"])
        for c_item in a["compliance"]:
            s["compliance_total"] += 1
            s["compliance_passed"] += 1 if c_item["passed"] else 0

    # Build leaderboard
    for rank, (agent, s) in enumerate(
        sorted(agent_stats.items(), key=lambda x: x[1]["total_csat"]/x[1]["calls"], reverse=True), 1
    ):
        avg_csat = s["total_csat"] / s["calls"]
        resolution_rate = round(s["resolved"] / s["calls"] * 100)
        avg_dur = round(s["total_duration"] / s["calls"], 1)
        compliance_rate = round(s["compliance_passed"] / s["compliance_total"] * 100) if s["compliance_total"] else 0
        pos = s["sentiments"].count("Positive")
        neg = s["sentiments"].count("Negative")

        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")

        with st.container():
            col_rank, col_name, col_calls, col_res, col_csat, col_comp, col_dur = st.columns([0.5, 2, 1, 1, 1.5, 1, 1])
            col_rank.markdown(f"### {medal}")
            col_name.markdown(f"**{agent}**")
            col_calls.metric("Calls", s["calls"])
            col_res.metric("Resolution", f"{resolution_rate}%")
            stars_html = '<span style="color:#f59e0b;">★</span>' * round(avg_csat) + \
                        '<span style="color:#d1d5db;">★</span>' * (5 - round(avg_csat))
            col_csat.markdown(f"**CSAT**\n\n{stars_html}", unsafe_allow_html=True)
            col_comp.metric("Compliance", f"{compliance_rate}%")
            col_dur.metric("Avg Time", f"{avg_dur}m")

        st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# TAB 4: TRY IT YOURSELF
# ═══════════════════════════════════════════════════════════════
with tab_try:
    st.markdown("### 🧪 Paste Your Own Transcript")
    st.markdown("Paste a call transcript below to see it analyzed in real-time.")
    st.markdown("")

    tc1, tc2 = st.columns(2)

    with tc1:
        custom_agent = st.text_input("Agent Name", value="Jane Doe")
        custom_customer = st.text_input("Customer Name", value="John Smith")
        custom_queue = st.selectbox("Queue", ["Billing", "Technical Support", "Sales", "General"])

        custom_transcript = st.text_area(
            "Transcript",
            height=300,
            placeholder="""Agent: Thank you for calling, how can I help?
Customer: I'm having trouble with my account...
Agent: I'd be happy to help with that..."""
        )

        analyze_btn = st.button("🔍 Analyze Transcript", type="primary", use_container_width=True)

    with tc2:
        if analyze_btn and custom_transcript.strip():
            custom_call = {
                "call_id": "CUSTOM-001",
                "agent": custom_agent,
                "customer": custom_customer,
                "customer_tier": "—",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%I:%M %p"),
                "duration_seconds": 0,
                "queue": custom_queue,
                "phone": "—",
                "previous_calls": 0,
                "transcript": custom_transcript
            }
            with st.spinner("Analyzing transcript..."):
                result = analyze_call(custom_call, use_ai=use_ai, api_key=api_key or None)

            st.markdown("#### 💡 Analysis Results")
            st.markdown(f'<div class="insight-box">{result["summary"]}</div>', unsafe_allow_html=True)

            r1, r2, r3 = st.columns(3)
            with r1:
                s_class = f"sentiment-{result['sentiment'].lower()}"
                st.markdown("**Sentiment**")
                st.markdown(f'<span class="{s_class}">{result["sentiment"]}</span>', unsafe_allow_html=True)
                st.progress(result["sentiment_score"])
            with r2:
                badge = "resolved-yes" if result["is_resolved"] else "resolved-no"
                txt = "✅ Resolved" if result["is_resolved"] else "❌ Open"
                st.markdown("**Resolution**")
                st.markdown(f'<span class="resolved-badge {badge}">{txt}</span>', unsafe_allow_html=True)
            with r3:
                stars = '<span class="star-filled">★</span>' * result["csat_prediction"] + \
                        '<span class="star-empty">★</span>' * (5 - result["csat_prediction"])
                st.markdown("**Predicted CSAT**")
                st.markdown(stars, unsafe_allow_html=True)

            # Categories
            tags = " ".join(f'<span class="tag">{cat}</span>' for cat in result["categories"])
            st.markdown(tags, unsafe_allow_html=True)
            st.markdown("")

            # Action items
            st.markdown("**⚡ Action Items**")
            for item in result["action_items"]:
                st.markdown(f'<div class="action-item">→ {item}</div>', unsafe_allow_html=True)

            # Compliance
            st.markdown("")
            st.markdown("**🛡️ Compliance**")
            for c_item in result["compliance"]:
                icon = "✅" if c_item["passed"] else "⚠️"
                st.markdown(f"{icon} {c_item['check']}")

        elif analyze_btn:
            st.warning("Please paste a transcript first.")
        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem; color:#9ca3af;">
                <p style="font-size:3rem;">📝</p>
                <p>Paste a transcript on the left and click<br><strong>Analyze Transcript</strong> to see results here.</p>
            </div>
            """, unsafe_allow_html=True)
