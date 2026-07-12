import streamlit as st
from streamlit_autorefresh import st_autorefresh
from database import get_players, get_player_count

st.title("👥 Waiting Room")

# Check if the player has joined a room
if "player" not in st.session_state:
    st.error("Please create or join a room first.")
    st.stop()

# Refresh every 2 seconds
st_autorefresh(interval=2000, key="waiting_refresh")

player = st.session_state.player

room_code = player["room_code"]
player_name = player["name"]

st.subheader(f"Room Code: {room_code}")

players = get_players(room_code)

st.write(f"Players ({len(players)}/4)")

for player in players:
    st.write(f"✅ {player[2]}")

remaining = 4 - len(players)

if remaining > 0:
    st.info(f"Waiting for {remaining} more player(s)...")
else:
    st.success("🎉 All players have joined!")
    st.switch_page("pages/3_Game.py")