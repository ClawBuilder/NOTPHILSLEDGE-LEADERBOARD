import streamlit as st
import json

st.set_page_config(page_title="NotPhilSledge Leaderboard", page_icon="⚡")

# Initialize session state for filter
if 'filter' not in st.session_state:
    st.session_state.filter = "All Time"

# Avatar helper
def get_avatar(username):
    return f"https://unavatar.io/x/{username}?fallback=https://api.dicebear.com/7.x/initials/svg?seed={username}&backgroundColor=8B5CF6"

# Load data
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("data.json not found!")
    st.stop()

st.title("🏆 NotPhilSledge Leaderboard")

# Filter buttons (using radio for single selection)
filter_option = st.radio(
    "Time Period",
    ["Today", "This Week", "This Month", "All Time"],
    horizontal=True,
    label_visibility="collapsed"
)

# Stats (same for now - would filter in full version)
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Replies Sent", t['repliesSent'])
col2.metric("Replies Received", t['repliesReceived'])
col3.metric("Unique Accounts", t['uniqueEngaged'])
col4.metric("Reply Rate", f"{rate}%")

st.markdown("---")

# Left column - You replied to
st.subheader("📤 You Replied To")
for i, r in enumerate(data.get('repliesTo', [])[:15]):
    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
    color = "#ffd700" if i == 0 else "#c0c0c0" if i == 1 else "#cd7f32" if i == 2 else "#666"
    st.markdown(f"""
    <div style="display:flex;align-items:center;padding:10px;border-bottom:1px solid #2a2a3a;">
        <span style="width:30px;font-weight:bold;color:{color};">{medal}</span>
        <img src="{get_avatar(r['username'])}" style="width:36px;height:36px;border-radius:50%;margin:0 12px;" onerror="this.src='https://api.dicebear.com/7.x/initials/svg?seed={r['username']}&backgroundColor=8B5CF6'">
        <span style="flex:1;font-weight:500;">@{r['username']}</span>
        <span style="color:#8B5CF6;font-weight:bold;font-size:1.1em;">{r['count']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Right column - Replied to you
st.subheader("📥 Replied to You")
for i, r in enumerate(data.get('repliesFrom', [])[:15]):
    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
    color = "#ffd700" if i == 0 else "#c0c0c0" if i == 1 else "#cd7f32" if i == 2 else "#666"
    st.markdown(f"""
    <div style="display:flex;align-items:center;padding:10px;border-bottom:1px solid #2a2a3a;">
        <span style="width:30px;font-weight:bold;color:{color};">{medal}</span>
        <img src="{get_avatar(r['username'])}" style="width:36px;height:36px;border-radius:50%;margin:0 12px;" onerror="this.src='https://api.dicebear.com/7.x/initials/svg?seed={r['username']}&backgroundColor=8B5CF6'">
        <span style="flex:1;font-weight:500;">@{r['username']}</span>
        <span style="color:#8B5CF6;font-weight:bold;font-size:1.1em;">{r['count']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"Updated: {data.get('lastUpdated', 'Unknown')}")
