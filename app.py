import streamlit as st
import json

st.set_page_config(page_title="NotPhilSledge Analytics", page_icon="⚡")

# Custom CSS - polished dark theme
st.markdown("""
<style>
    .stApp { background: #0D0D0F; }
    h1 { background: linear-gradient(90deg, #fff, #ccc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #71717A !important; text-transform: uppercase; font-size: 0.7rem !important; }
    [data-testid="stMetricValue"] { color: #fff !important; font-weight: 600 !important; }
    h2, h3 { color: #fff !important; font-weight: 600 !important; }
    .leaderboard-row { display: flex; align-items: center; padding: 12px 16px; background: #18181B; border-radius: 12px; margin-bottom: 8px; border: 1px solid #27272A; }
    .leaderboard-row:hover { border-color: #3F3F46; transform: translateX(4px); }
    .rank-badge { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin-right: 12px; }
    .rank-1 { background: linear-gradient(135deg, #F59E0B, #D97706); color: #000; }
    .rank-2 { background: linear-gradient(135deg, #9CA3AF, #6B7280); color: #000; }
    .rank-3 { background: linear-gradient(135deg, #CD7F32, #B45309); color: #000; }
    .rank-other { background: #27272A; color: #A1A1AA; }
    .user-avatar { width: 40px; height: 40px; border-radius: 50%; margin-right: 12px; object-fit: cover; }
    .username { flex: 1; font-weight: 500; color: #E4E4E7; }
    .count { color: #8B5CF6; font-weight: 700; font-size: 1.1rem; }
    .post-card { background: #18181B; border: 1px solid #27272A; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    .post-text { color: #E4E4E7; font-size: 0.95rem; margin-bottom: 8px; }
    .post-stats { display: flex; gap: 16px; color: #71717A; font-size: 0.85rem; }
    .post-stat { color: #8B5CF6; font-weight: 600; }
    .share-btn { display: inline-block; background: #8B5CF6; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; }
    .share-btn:hover { background: #7C3AED; }
    .section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #27272A; }
    footer { text-align: center; padding: 20px; color: #52525B; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

def get_avatar(username):
    return f"https://unavatar.io/x/{username}?fallback=https://api.dicebear.com/7.x/initials/svg?seed={username}&backgroundColor=8B5CF6"

def load_data(period):
    files = {"Today": "today.json", "This Week": "week.json", "This Month": "month.json", "All Time": "alltime.json"}
    try:
        with open(files.get(period, 'data.json'), 'r') as f:
            return json.load(f)
    except:
        with open('data.json', 'r') as f:
            return json.load(f)

st.title("⚡ NotPhilSledge Analytics")

# Filter
period = st.selectbox("", ["Today", "This Week", "This Month", "All Time"], label_visibility="collapsed")
data = load_data(period)

# Stats
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Replies Sent", t['repliesSent'])
col2.metric("Replies Received", t['repliesReceived'])
col3.metric("Unique Accounts", t['uniqueEngaged'])
col4.metric("Reply Rate", f"{rate}%")

st.markdown("---")

# Two columns - Top Replies
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📤 You Replied To")
    for i, r in enumerate(data.get('repliesTo', [])[:10]):
        rank_class = f"rank-{i+1}" if i < 3 else "rank-other"
        st.markdown(f"""
        <div class="leaderboard-row">
            <div class="rank-badge {rank_class}">{i+1}</div>
            <img class="user-avatar" src="{get_avatar(r['username'])}" onerror="this.src='https://api.dicebear.com/7.x/initials/svg?seed={r['username']}&backgroundColor=8B5CF6'">
            <span class="username">@{r['username']}</span>
            <span class="count">{r['count']}</span>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 🔄 Reply Reciprocity")
    st.caption("People who reply back to you")
    for i, r in enumerate(data.get('repliesFrom', [])[:10]):
        rank_class = f"rank-{i+1}" if i < 3 else "rank-other"
        st.markdown(f"""
        <div class="leaderboard-row">
            <div class="rank-badge {rank_class}">{i+1}</div>
            <img class="user-avatar" src="{get_avatar(r['username'])}" onerror="this.src='https://api.dicebear.com/7.x/initials/svg?seed={r['username']}&backgroundColor=8B5CF6'">
            <span class="username">@{r['username']}</span>
            <span class="count">{r['count']}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Top Posts by Impressions
st.markdown("### 📊 Top Posts by Impressions")
for i, post in enumerate(data.get('topPosts', [])[:5]):
    st.markdown(f"""
    <div class="post-card">
        <div class="post-text">{post.get('text', '')[:80]}...</div>
        <div class="post-stats">
            <span>👁️ <span class="post-stat">{post.get('impressions', 0)}</span> impressions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Share Button
st.markdown("### 🚀 Share Your Stats")
st.markdown(f"""
<a href="https://twitter.com/intent/tweet?text=Check+out+my+X+analytics!+%23NotPhilSledge&url=https://notphilsledge-leaderboard-wzkcjnvi7sgexabgeg82p7.streamlit.app" 
   target="_blank" 
   class="share-btn">
   Share on X →
</a>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f'<footer>Period: {period} | Updated: {data.get("lastUpdated", "N/A")}</footer>', unsafe_allow_html=True)
