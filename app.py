import streamlit as st
import json

st.set_page_config(
    page_title="NotPhilSledge",
    page_icon="⚡",
    layout="wide"
)

# Blackmagic-inspired dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: #0D0D0F;
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #8B5CF6, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    
    .subtitle {
        color: #71717A;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .stMetric {
        background: #18181B !important;
        border: 1px solid #27272A !important;
        padding: 1.25rem !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #A1A1AA !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
    }
    
    h2 {
        color: #E4E4E7 !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    .leaderboard-card {
        background: #18181B;
        border: 1px solid #27272A;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    
    .leaderboard-card:hover {
        background: #27272A;
        border-color: #3F3F46;
    }
    
    .rank {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.875rem;
        margin-right: 1rem;
    }
    
    .rank-1 { background: linear-gradient(135deg, #F59E0B, #D97706); color: #000; }
    .rank-2 { background: linear-gradient(135deg, #9CA3AF, #6B7280); color: #000; }
    .rank-3 { background: linear-gradient(135deg, #CD7F32, #B45309); color: #000; }
    .rank-other { background: #27272A; color: #A1A1AA; }
    
    .username {
        color: #E4E4E7;
        font-weight: 500;
        flex: 1;
    }
    
    .count {
        color: #8B5CF6;
        font-weight: 600;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .section-icon {
        font-size: 1.25rem;
    }
    
    .divider {
        background: linear-gradient(90deg, transparent, #27272A, transparent);
        height: 1px;
        margin: 2rem 0;
    }
    
    footer {
        color: #52525B;
        font-size: 0.75rem;
        text-align: center;
        margin-top: 2rem;
    }
    
    .stButton button {
        background: #8B5CF6 !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    
    .stButton button:hover {
        background: #7C3AED !important;
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
st.title("NotPhilSledge")
st.markdown("*X Engagement Analytics*")

# Stats row
t = data['totals']
rate = round((t['repliesReceived'] / t['repliesSent']) * 100) if t['repliesSent'] else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Replies Sent", t['repliesSent'])
with col2:
    st.metric("Replies Received", t['repliesReceived'])
with col3:
    st.metric("Unique Accounts", t['uniqueEngaged'])
with col4:
    st.metric("Reply Rate", f"{rate}%")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Two columns
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-header"><span class="section-icon">📤</span><h2>You Replied To</h2></div>', unsafe_allow_html=True)
    replies_to = data.get('repliesTo', [])
    for i, r in enumerate(replies_to[:10]):
        rank_class = f"rank-{i+1}" if i < 3 else "rank-other"
        st.markdown(f"""
        <div class="leaderboard-card">
            <div class="rank {rank_class}">{i+1}</div>
            <div class="username">@{r['username']}</div>
            <div class="count">{r['count']}</div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-header"><span class="section-icon">📥</span><h2>Replied to You</h2></div>', unsafe_allow_html=True)
    replies_from = data.get('repliesFrom', [])
    for i, r in enumerate(replies_from[:10]):
        rank_class = f"rank-{i+1}" if i < 3 else "rank-other"
        st.markdown(f"""
        <div class="leaderboard-card">
            <div class="rank {rank_class}">{i+1}</div>
            <div class="username">@{r['username']}</div>
            <div class="count">{r['count']}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown(f'<footer>Last updated: {data.get("lastUpdated", "Unknown")}</footer>', unsafe_allow_html=True)

if st.button("🔄 Refresh"):
    st.rerun()
