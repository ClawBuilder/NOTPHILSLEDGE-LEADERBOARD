import streamlit as st
import json
import subprocess
from datetime import datetime, timedelta

st.set_page_config(page_title="NotPhilSledge Leaderboard", page_icon="⚡")

# Avatar helper
def get_avatar(username):
    return f"https://unavatar.io/x/{username}?fallback=https://api.dicebear.com/7.x/initials/svg?seed={username}&backgroundColor=8B5CF6"

# Fetch data from X API
def fetch_x_data(days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_time = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Get tweets from NotPhilSledge
    cmd = f'xurl -X GET "/2/users/1843995910545485824/tweets?tweet.fields=created_at&max_results=100&start_time={start_time}" 2>/dev/null'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        tweets = data.get('data', [])
        
        # Extract replies and their authors
        from collections import Counter
        replies_to = Counter()
        replies_from = Counter()
        
        # Get mentions (people who replied to NotPhilSledge)
        mentions_cmd = f'xurl mentions -n 100 2>/dev/null'
        mentions_result = subprocess.run(mentions_cmd, shell=True, capture_output=True, text=True)
        
        try:
            mentions_data = json.loads(mentions_result.stdout)
            mentions = mentions_data.get('data', [])
            for m in mentions:
                author = m.get('author_id', '')
                # Get username from includes
                includes = mentions_data.get('includes', {}).get('users', [])
                for u in includes:
                    if u.get('id') == author:
                        replies_from[u.get('username', '')] += 1
        except:
            pass
        
        # Count replies (tweets starting with @)
        for t in tweets:
            text = t.get('text', '')
            if text.startswith('@'):
                import re
                match = re.match(r'@(\w+)', text)
                if match:
                    replies_to[match.group(1)] += 1
        
        # Get top 15
        top_replies_to = [{"username": u, "count": c} for u, c in replies_to.most_common(15)]
        top_replies_from = [{"username": u, "count": c} for u, c in replies_from.most_common(15)]
        
        total_sent = sum(replies_to.values())
        total_received = sum(replies_from.values())
        unique = len(replies_to)
        
        return {
            "repliesTo": top_replies_to,
            "repliesFrom": top_replies_from,
            "totals": {
                "repliesSent": total_sent,
                "repliesReceived": total_received,
                "uniqueEngaged": unique
            }
        }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

st.title("🏆 NotPhilSledge Leaderboard")

# Filter buttons
filter_key = st.radio(
    "Time Period",
    ["Today", "This Week", "This Month", "All Time"],
    horizontal=True,
    label_visibility="collapsed"
)

# Map filter to days
days_map = {
    "Today": 1,
    "This Week": 7,
    "This Month": 30,
    "All Time": 365
}

# Fetch data based on filter
with st.spinner(f'Loading {filter_key} data from X...'):
    x_data = fetch_x_data(days_map[filter_key])

if x_data:
    t = x_data['totals']
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
    for i, r in enumerate(x_data.get('repliesTo', [])[:15]):
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
    for i, r in enumerate(x_data.get('repliesFrom', [])[:15]):
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
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
