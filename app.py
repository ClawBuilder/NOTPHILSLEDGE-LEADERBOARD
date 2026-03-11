import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="NotPhilSledge Leaderboard", page_icon="🏆")

# Load data
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("data.json not found!")
    st.stop()

# Header
st.title("🏆 NotPhilSledge Engagement Leaderboard")

# Stats row
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Replies Sent", t['repliesSent'])
col2.metric("Replies Received", t['repliesReceived'])
col3.metric("Unique Accounts", t['uniqueEngaged'])
col4.metric("Reply Rate", f"{rate}%")

st.divider()

# You Replied To
st.subheader("📤 You Replied To")
replies_to = data.get('repliesTo', [])
for i, r in enumerate(replies_to[:15]):
    st.write(f"**#{i+1}** @{r['username']} — {r['count']} replies")

st.divider()

# Replied to You
st.subheader("📥 Replied to You")
replies_from = data.get('repliesFrom', [])
for i, r in enumerate(replies_from[:15]):
    st.write(f"**#{i+1}** @{r['username']} — {r['count']} replies")

# Footer
st.divider()
st.caption(f"Updated: {data.get('lastUpdated', 'Unknown')}")
