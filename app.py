# === app.py ===
import streamlit as st
from PIL import Image
import pandas as pd
import base64
from io import BytesIO
import os
from data import players_dict as players

st.set_page_config(page_title="Player Stat Card", layout="wide")

def smart_round(val, digits=3):
    try:
        f = float(val)
        rounded = round(f, digits)
        # Drop trailing zero if third decimal is zero
        if digits == 3 and str(rounded).endswith("0"):
            return round(f, 2)
        return rounded
    except:
        return val  # leave as-is if not a number

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
    number = data.get('Number', 'mock')
    img_path = f"img/{number}_player.png"
    if not os.path.exists(img_path):
        img_path = "img/mock.png"
    st.image(img_path, use_container_width=True)
    
    st.markdown(f"##  {selected_player}")
    st.markdown(f"**#{number}**")
    st.markdown(f"**School:** {data['School']}")
    st.markdown(f"**Grade:** {data['Grade']}")

# MIDDLE
with col2:
    # === Derived fields with substitution logic ===
    batting = data["Batting"]
    pitching = data["Pitching"]
    fielding = data["Fielding"]

    # Batting fallbacks
    hr = batting.get("HR") or batting.get("XBH") or batting.get("2B") or 0
    rbi = batting.get("RBI") or batting.get("R") or 0
    sb = batting.get("SB") if batting.get("SB") not in [None, ""] else (1 if batting.get("SB%") and float(batting.get("SB%") or 0) > 0 else 0)
    ops = batting.get("OPS") or round((float(batting.get("OBP") or 0) + float(batting.get("SLG") or 0)), 3)

    # Pitching fallbacks
    era = pitching.get("ERA") if pitching.get("ERA") not in [None, "-", ""] else pitching.get("FIP") or 0
    so = pitching.get("SO") or pitching.get("K-L") or 0
    bb = pitching.get("BB") or (
        (float(pitching.get("BB/INN") or 0) * float(pitching.get("IP") or 0)) if pitching.get("BB/INN") and pitching.get("IP") else 0
    )
    whip = pitching.get("WHIP")
    if whip in [None, "-", ""] and pitching.get("IP") not in [None, 0, "-", ""]:
        whip = (float(pitching.get("BB") or 0) + float(pitching.get("H") or 0)) / float(pitching.get("IP"))
    elif whip in [None, "-", ""]:
        whip = 0

    # Fielding fallbacks
    fpct = fielding.get("FPCT")
    if fpct in [None, "-", ""] and fielding.get("PO") and fielding.get("E") is not None:
        fpct = float(fielding.get("PO")) / (float(fielding.get("PO")) + float(fielding.get("E")) + 1e-6)  # prevent div0
    elif fpct in [None, "-", ""]:
        fpct = 0

    assists = fielding.get("Assists") or fielding.get("A") or 0
    po = fielding.get("PO") or 0
    errors = fielding.get("Errors") or fielding.get("E") or 0

    render_stat_card("📊 Key Stats", {
        "AVG": smart_round(batting.get("AVG", 0)),
        "OPS": smart_round(ops),
        "ERA": smart_round(era),
        "WHIP": smart_round(whip)
    }, order=["AVG", "OPS", "ERA", "WHIP"], round_digits=None)

    render_stat_card("🥎 Batting Breakdown", {
        "AVG": smart_round(batting.get("AVG", 0)),
        "HR": smart_round(hr),
        "RBI": smart_round(rbi),
        "SB": smart_round(sb)
    }, order=["AVG", "HR", "RBI", "SB"], round_digits=None)

    render_stat_card("⚾ Pitching Breakdown", {
        "ERA": smart_round(era),
        "SO": smart_round(so),
        "BB": smart_round(bb),
        "WHIP": smart_round(whip)
    }, order=["ERA", "SO", "BB", "WHIP"], round_digits=None)

    render_stat_card("🧤 Fielding Summary", {
        "FPCT": smart_round(fpct),
        "PO": smart_round(po),
        "Assists": smart_round(assists),
        "Errors": smart_round(errors)
    }, order=["FPCT", "PO", "Assists", "Errors"], round_digits=None)


# RIGHT
number = data.get('Number', 'mock')
spray_img_path = f"img/{number}_field.png"
if not os.path.exists(spray_img_path):
    spray_img_path = "img/mock_field.png"

spray_img = Image.open(spray_img_path)
buffer = BytesIO()
spray_img.save(buffer, format="PNG")
spray_img_b64 = base64.b64encode(buffer.getvalue()).decode()

# RIGHT
with col3:
    st.markdown(f"""
    <div style='background-color:#f0ffff; padding:1rem; border-radius:10px; text-align: center;'>
        <h4 style='color:#000000;'>🗺️ Batting Spray Chart</h4>
        <img src='data:image/png;base64,{spray_img_b64}' 
        style='width:100%; border-radius:8px; margin-top:1rem;'>
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
