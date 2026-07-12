import streamlit as st
from streamlit_autorefresh import st_autorefresh

from database import (
    get_phase,
    update_phase,
    get_player_role,
    set_player_ready,
    all_players_ready,
    get_player_by_role,
    get_player_names,
    save_guess,
    get_guess,
    get_scores,
    get_round
)

from game import (
    assign_roles,
    calculate_round,
    start_next_round
)


st.title("🎮 Badshah Ka Wazeer Kon")


# -------------------------
# CHECK PLAYER
# -------------------------

if "player" not in st.session_state:

    st.error(
        "Please create or join a room first."
    )

    st.stop()


player = st.session_state.player

room_code = player["room_code"]
player_name = player["name"]
round_number = get_round(room_code)

st.subheader(f"Round {round_number} / 5")


st_autorefresh(
    interval=2000,
    key="refresh"
)



# -------------------------
# ASSIGN ROLES
# -------------------------

phase = get_phase(room_code)

role = get_player_role(
    room_code,
    player_name
)


if phase == "show_roles" and not role:

    assign_roles(room_code)

    role = get_player_role(
        room_code,
        player_name
    )

# -------------------------
# SHOW ROLE
# -------------------------

if phase == "show_roles":

    st.success(
        f"Your role: {role}"
    )


    if role == "Badshah":

        st.header(
            "👑 You are the Badshah"
        )

    elif role == "Wazeer":

        st.header(
            "🧠 You are the Wazeer"
        )

    elif role == "Chor":

        st.header(
            "🕵️ You are the Chor"
        )

    else:

        st.header(
            "🛡️ You are the Sipahi"
        )


    if st.button("✅ I am Ready"):

        set_player_ready(
            room_code,
            player_name
        )


        if all_players_ready(room_code):

            update_phase(
                room_code,
                "ask_wazeer"
            )


        st.rerun()



# -------------------------
# BADSHAH ASKS WAZEER
# -------------------------

elif phase == "ask_wazeer":


    if role == "Badshah":

        st.header(
            "👑 Badshah"
        )


        if st.button(
            "Mera Wazeer Kon?"
        ):

            update_phase(
                room_code,
                "reveal_wazeer"
            )

            st.rerun()


    else:

        st.info(
            "Waiting for Badshah..."
        )



# -------------------------
# WAZEER REVEAL
# -------------------------

elif phase == "reveal_wazeer":


    if role == "Wazeer":

        st.header(
            "🧠 You are the Wazeer"
        )


        if st.button(
            "Main Hoon!"
        ):

            update_phase(
                room_code,
                "ask_guess"
            )

            st.rerun()


    else:

        st.info(
            "Waiting for Wazeer..."
        )



# -------------------------
# BADSHAH STARTS GUESS
# -------------------------

elif phase == "ask_guess":


    wazeer = get_player_by_role(
        room_code,
        "Wazeer"
    )


    st.success(
        f"🧠 Wazeer is {wazeer}"
    )


    if role == "Badshah":


        if st.button(
            "Chor Ka Pata Lagao"
        ):

            update_phase(
                room_code,
                "guessing"
            )

            st.rerun()


    else:

        st.info(
            "Waiting for Badshah..."
        )



# -------------------------
# WAZEER GUESS
# -------------------------

elif phase == "guessing":


    if role == "Wazeer":


        st.header(
            "🧠 Guess the Chor"
        )


        players = get_player_names(
            room_code
        )


        players.remove(
            player_name
        )


        guess = st.radio(
            "Select player:",
            players
        )


        if st.button(
            "Submit Guess"
        ):


            save_guess(
                room_code,
                guess
            )


            calculate_round(
                room_code
            )


            update_phase(
                room_code,
                "round_result"
            )


            st.rerun()



    else:

        st.info(
            "Waiting for Wazeer..."
        )



# -------------------------
# RESULT
# -------------------------

elif phase == "round_result":


    st.header(
        "🏁 Round Result"
    )


    guessed = get_guess(
        room_code
    )


    guessed_role = get_player_role(
        room_code,
        guessed
    )


    st.write(
        f"Wazeer guessed: {guessed}"
    )


    if guessed_role == "Chor":

        st.success(
            "✅ Correct Guess"
        )

    else:

        st.error(
            "❌ Wrong Guess"
        )


    st.divider()

    st.subheader(
        "Scores"
    )


    scores = get_scores(
        room_code
    )


    for name, score in scores:

        st.write(
            f"{name}: {score}"
        )



    if role == "Badshah":

        button_text = (
        "Finish Game"
        if round_number == 5
        else f"Start Round {round_number + 1}"
        )

        if st.button(button_text):
            start_next_round(
            room_code
        )
            st.rerun()



# -------------------------
# GAME OVER
# -------------------------

elif phase == "game_over":


    st.title(
        "🏆 Final Results"
    )


    scores = get_scores(
        room_code
    )


    for index, (name, score) in enumerate(
        scores,
        start=1
    ):

        st.write(
            f"{index}. {name} - {score}"
        )


    st.success(
        f"Winner: {scores[0][0]}"
    )