# === app.py ===
import streamlit as st
from PIL import Image
import pandas as pd
import base64
from io import BytesIO
from data import players_dict as players

st.set_page_config(page_title="Player Stat Card", layout="wide")

def render_stat_card(title: str, stats: dict, order: list = None, round_digits: int = 3):
    stat_items = order if order else stats.keys()
    blocks = ""
    for key in stat_items:
        val = stats.get(key, "-")
        try:
            val_fmt = f"{float(val):.{round_digits}f}"
        except:
            val_fmt = str(val)
        blocks += f"""
<div style='flex:1; margin: 0.5rem; padding: 0.75rem; background-color:#ffffff; border:1px solid #ddd; border-radius:8px; text-align:center; color:#000000;'>
    <strong style='color:#000000;'>{key}</strong><br>
    <span style='color:#000000;'>{val_fmt}</span>
</div>"""

    st.markdown(f"""
<div style='background-color:#F9F9FF; padding:1rem; border-radius:10px; margin-bottom:1rem;'>
<h4 style='color:#000000;'>{title}</h4>
<div style='display: flex; justify-content: space-between; width: 100%;'>
{blocks}
</div>
</div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Select Player")
selected_player = st.sidebar.selectbox("Player", list(players.keys()))
data = players[selected_player]

# Image setup
img = Image.open("baseball_field_map.png")
buffer = BytesIO()
img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode()

col1, col2, col3 = st.columns([1.2, 1.8, 1.6])

# LEFT
with col1:
    st.image("mock_player_photo.png", use_container_width=True)
    st.markdown(f"## 🧍 {selected_player}")
    st.markdown(f"**#{data['Number']}**")
    st.markdown(f"**School:** {data['School']}")
    st.markdown(f"**Grade:** {data['Grade']}")

# MIDDLE
with col2:
    render_stat_card("📊 Key Stats", {
        "AVG": data["Batting"]["AVG"],
        "OPS": data["Batting"]["OPS"],
        "ERA": data["Pitching"]["ERA"],
        "WHIP": data["Pitching"]["WHIP"]
    }, order=["AVG", "OPS", "ERA", "WHIP"], round_digits=3)

    render_stat_card("🥎 Batting Breakdown", data["Batting"], order=["AVG", "OPS", "SLG", "OBP"], round_digits=3)
    render_stat_card("⚾ Pitching Breakdown", data["Pitching"], order=["IP", "GP", "ERA", "WHIP"], round_digits=2)
    render_stat_card("🧤 Fielding Summary", data["Fielding"], order=["TC", "FPCT", "Assists", "Errors"], round_digits=3)

# RIGHT
with col3:
    st.markdown(f"""
    <div style='background-color:#f0ffff; padding:1rem; border-radius:10px; text-align: center;'>
        <h4 style='color:#000000;'>🗺️ Batting Spray Chart</h4>
        <img src='data:image/png;base64,{img_b64}' alt='Defensive Positions'
             style='width:100%; border-radius:8px; margin-top:1rem;'>
        <div style='font-size: 0.9rem; color: #555;'>Defensive Positions</div>
    </div>
    """, unsafe_allow_html=True)

# Export CSV
st.markdown("---")
if st.button("📥 Export Player Stats as CSV"):
    df = pd.DataFrame({k: [v] for k, v in {
        "Name": selected_player,
        **data["Batting"],
        **data["Pitching"],
        **data["Fielding"]
    }.items()})
    filename = f"{selected_player.replace(' ', '_')}_stats.csv"
    df.to_csv(filename, index=False)
    st.success(f"Exported to `{filename}`")
