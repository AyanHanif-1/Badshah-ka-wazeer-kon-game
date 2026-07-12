import streamlit as st

from database import (
    create_room,
    room_exists,
    add_player,
    player_exists,
    get_player_count
)

from utils import generate_room_code

st.title("🎮 Create or Join a Room")

st.divider()

st.subheader("Create Room")

creator_name = st.text_input(
    "Enter Your Name",
    key="creator_name"
)

if st.button("Create Room"):

    if creator_name == "":
        st.error("Please enter your name.")

    else:

        room_code = generate_room_code()

        create_room(room_code)

        add_player(room_code, creator_name)

        st.session_state.room_code = room_code
        st.session_state.player_name = creator_name

        st.success(f"Room Created! Code: {room_code}")

        st.session_state.player = {
            "name": creator_name,
            "room_code": room_code
        }

        st.switch_page("pages/2_Waiting_Room.py")

st.subheader("Join Room")

player_name = st.text_input(
    "Your Name",
    key="join_name"
)

join_code = st.text_input(
    "Room Code",
    key="join_code"
)

if st.button("Join Room"):

    if player_name == "":
        st.error("Please enter your name.")

    elif join_code == "":
        st.error("Please enter a room code.")

    elif not room_exists(join_code):
        st.error("Room does not exist.")

    elif get_player_count(join_code) >= 4:
        st.error("This room is already full.")

    elif player_exists(join_code, player_name):
        st.error("A player with this name already exists in the room.")

    else:

        add_player(join_code, player_name)

        st.session_state.player = {
            "name": player_name,
            "room_code": join_code
        }

        st.success("Joined successfully!")

        st.switch_page("pages/2_Waiting_Room.py")