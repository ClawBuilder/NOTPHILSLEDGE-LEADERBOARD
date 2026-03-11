import streamlit as st
import json

st.set_page_config(page_title="NotPhilSledge Leaderboard", page_icon="⚡")

# Custom CSS for better look
st.markdown("""
<style>
    .stApp {
        background: #0D0D0F;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background: #18181B !important;
        border-color: #27272A !important;
    }
    div[data-test="stSelectbox"] label {
        display: none;
    }
    h1 {
        background: linear-gradient(90deg, #fff 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #71717A !important;
        text-transform: uppercase;
        font-size: 0.7rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #fff !important;
        font-weight: 600 !important;
    }
    h2 {
        color: #fff !important;
        font-weight: 600 !important;
    }
    .leaderboard-row {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: #18181B;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid #27272A;
        transition: all 0.2s;
    }
    .leaderboard-row:hover {
        border-color: #3F3F46;
        transform: translateX(4px);
    }
    .rank-badge {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        margin-right: 12px;
    }
    .rank-1 { background: linear-gradient(135deg, #F59E0B, #D97706); color: #000; }
    .rank-2 { background: linear-gradient(135deg, #9CA3AF, #6B7280); color: #000; }
    .rank-3 { background: linear-gradient(135deg, #CD7F32, #B45309); color: #000; }
    .rank-other { background: #27272A; color: #A1A1AA; }
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 12px;
        object-fit: cover;
    }
    .username {
        flex: 1;
        font-weight: 500;
        color: #E4E4E7;
    }
    .count {
        color: #8B5CF6;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .section-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #27272A;
    }
    .section-icon {
        font-size: 1.2rem;
    }
    footer {
        text-align: center;
        padding: 20px;
        color: #52525B;
        font-size: 0.8rem;
    }
    .stDivider {
        background: #27272A;
    }
</style>
""", unsafe_allow_html=True)

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
    try:
        with open(files.get(period, 'data.json'), 'r') as f:
            return json.load(f)
    except:
        try:
            with open('data.json', 'r') as f:
                return json.load(f)
        except:
            return {"repliesTo": [], "repliesFrom": [], "totals": {"repliesSent": 0, "repliesReceived": 0, "uniqueEngaged": 0}}

st.title("⚡ NotPhilSledge")

# Filter
period = st.selectbox(
    "",
    ["Today", "This Week", "This Month", "All Time"],
    label_visibility="collapsed"
)

data = load_data(period)

# Stats
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

st.markdown("### Engagement Stats")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Replies Sent", t['repliesSent'])
col2.metric("Replies Received", t['repliesReceived'])
col3.metric("Unique Accounts", t['uniqueEngaged'])
col4.metric("Reply Rate", f"{rate}%")

st.markdown("---")

# Two columns
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-header"><span class="section-icon">📤</span><h2>You Replied To</h2></div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-header"><span class="section-icon">📥</span><h2>Replied to You</h2></div>', unsafe_allow_html=True)
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
st.markdown(f'<footer>Period: {period} | Updated: {data.get("lastUpdated", "N/A")}</footer>', unsafe_allow_html=True)
