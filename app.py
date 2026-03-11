import streamlit as st
import json

st.set_page_config(page_title="NotPhilSledge Leaderboard", page_icon="⚡")

# Avatar helper
def get_avatar(username):
    return f"https://unavatar.io/x/{username}?fallback=https://api.dicebear.com/7.x/initials/svg?seed={username}&backgroundColor=8B5CF6"

# Load data based on filter
def load_data(period):
    files = {
        "Today": "today.json",
        "This Week": "week.json", 
        "This Month": "month.json",
        "All Time": "alltime.json"
    }
    filename = files.get(period, "data.json")
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        with open('data.json', 'r') as f:
            return json.load(f)

st.title("🏆 NotPhilSledge Leaderboard")

# Filter selection
period = st.selectbox(
    "Time Period",
    ["Today", "This Week", "This Month", "All Time"],
    label_visibility="collapsed"
)

# Load data for selected period
data = load_data(period)

# Stats
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Replies Sent", t['repliesSent'])
col2.metric("Replies Received", t['repliesReceived'])
col3.metric("Unique Accounts", t['uniqueEngaged'])
col4.metric("Reply Rate", f"{rate}%")

st.markdown("---")

# Left column
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

# Right column
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
st.caption(f"Period: {period} | Updated: {data.get('lastUpdated', 'Unknown')}")
