import streamlit as st
import json

st.set_page_config(
    page_title="NotPhilSledge Leaderboard",
    page_icon="⚡",
    layout="wide"
)

# Load data
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("data.json not found!")
    st.stop()

# Helper for avatar
def get_avatar(username):
    return f"https://unavatar.io/x/{username}?fallback=https://api.dicebear.com/7.x/initials/svg?seed={username}&backgroundColor=8B5CF6"

# Header
st.title("🏆 NotPhilSledge")
st.markdown("### Engagement Leaderboard")

# Stats
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Replies Sent", t['repliesSent'])
col2.metric("Replies Received", t['repliesReceived'])
col3.metric("Unique Accounts", t['uniqueEngaged'])
col4.metric("Reply Rate", f"{rate}%")

st.divider()

# Two columns
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📤 You Replied To")
    for i, r in enumerate(data.get('repliesTo', [])[:10]):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
        avatar_url = get_avatar(r['username'])
        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #2a2a3a;">
            <span style="width:30px;font-weight:bold;color:{'#ffd700' if i==0 else '#c0c0c0' if i==1 else '#cd7f32' if i==2 else '#666'}">{medal}</span>
            <img src="{avatar_url}" style="width:32px;height:32px;border-radius:50%;margin:0 10px;" onerror="this.src='https://api.dicebear.com/7.x/initials/svg?seed={r['username']}&backgroundColor=8B5CF6'">
            <span style="flex:1;">@{r['username']}</span>
            <span style="color:#8B5CF6;font-weight:bold;">{r['count']}</span>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.subheader("📥 Replied to You")
    for i, r in enumerate(data.get('repliesFrom', [])[:10]):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
        avatar_url = get_avatar(r['username'])
        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #2a2a3a;">
            <span style="width:30px;font-weight:bold;color:{'#ffd700' if i==0 else '#c0c0c0' if i==1 else '#cd7f32' if i==2 else '#666'}">{medal}</span>
            <img src="{avatar_url}" style="width:32px;height:32px;border-radius:50%;margin:0 10px;" onerror="this.src='https://api.dicebear.com/7.x/initials/svg?seed={r['username']}&backgroundColor=8B5CF6'">
            <span style="flex:1;">@{r['username']}</span>
            <span style="color:#8B5CF6;font-weight:bold;">{r['count']}</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption(f"Last updated: {data.get('lastUpdated', 'Unknown')}")
