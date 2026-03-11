import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="NotPhilSledge Leaderboard",
    page_icon="🏆",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
    }
    h1 {
        color: #ff6b35 !important;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 2rem !important;
    }
    .stMetric {
        background: #12121a;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a3a;
    }
    .stMarkdown, .stText, p, div {
        color: #fff !important;
    }
    .stMarkdown p {
        color: #fff !important;
    }
    [data-testid="stMetricValue"] {
        color: #ff6b35 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #8a8a9a !important;
    }
    h2 {
        color: #fff !important;
        border-bottom: 2px solid #ff6b35;
        padding-bottom: 0.5rem;
    }
    .stDataFrame {
        background: #12121a;
        border-radius: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("data.json not found!")
    st.stop()

# Header
st.title("🏆 NotPhilSledge")

st.markdown("### Engagement Leaderboard")
st.markdown("*Tracking interactions with the X AI community*")

# Stats row
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📤 Replies Sent", t['repliesSent'])
with col2:
    st.metric("📥 Replies Received", t['repliesReceived'])
with col3:
    st.metric("👥 Unique Accounts", t['uniqueEngaged'])
with col4:
    st.metric("📊 Reply Rate", f"{rate}%")

st.divider()

# Two columns for leaderboards
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📤 You Replied To")
    replies_to = data.get('repliesTo', [])
    for i, r in enumerate(replies_to[:10]):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
        st.markdown(f"{medal} **#{i+1}** @{r['username']} — {r['count']} reply(s)")

with col_right:
    st.subheader("📥 Replied to You")
    replies_from = data.get('repliesFrom', [])
    for i, r in enumerate(replies_from[:10]):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
        st.markdown(f"{medal} **#{i+1}** @{r['username']} — {r['count']} reply(s)")

# Footer
st.divider()
st.caption(f"🕐 Last updated: {data.get('lastUpdated', 'Unknown')}")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()
