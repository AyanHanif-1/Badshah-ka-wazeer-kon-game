import random

from database import (
    get_players,
    update_role,
    get_guess,
    get_player_by_role,
    get_player_role,
    add_score,
    next_round,
    update_phase,
    save_guess,
    get_round,
    reset_player_ready
)


# -------------------------
# ROLE ASSIGNMENT
# -------------------------

def assign_roles(room_code):

    players = get_players(room_code)

    names = [
        player[2]
        for player in players
    ]

    roles = [
        "Badshah",
        "Wazeer",
        "Chor",
        "Sipahi"
    ]

    random.shuffle(roles)

    for name, role in zip(names, roles):

        update_role(
            room_code,
            name,
            role
        )



# -------------------------
# ROUND SCORING
# -------------------------

def calculate_round(room_code):

    guessed_player = get_guess(room_code)

    guessed_role = get_player_role(
        room_code,
        guessed_player
    )


    # Wazeer guessed correctly
    if guessed_role == "Chor":

        badshah = get_player_by_role(
            room_code,
            "Badshah"
        )

        wazeer = get_player_by_role(
            room_code,
            "Wazeer"
        )

        sipahi = get_player_by_role(
            room_code,
            "Sipahi"
        )


        add_score(
            room_code,
            badshah,
            100
        )

        add_score(
            room_code,
            wazeer,
            50
        )

        add_score(
            room_code,
            sipahi,
            50
        )


        return True


    # Wazeer guessed wrong

    else:

        chor = get_player_by_role(
            room_code,
            "Chor"
        )

        add_score(
            room_code,
            chor,
            100
        )

        return False



# -------------------------
# NEXT ROUND
# -------------------------

def start_next_round(room_code):

    current_round = get_round(room_code)

    # Finish game after 5 rounds
    if current_round >= 5:

        update_phase(
            room_code,
            "game_over"
        )

        return


    # Go to next round
    next_round(
        room_code
    )


    players = get_players(room_code)

    for player in players:

        name = player[2]

        # Remove old role
        update_role(
            room_code,
            name,
            ""
        )

        # Reset ready button
        reset_player_ready(
            room_code,
            name
        )


    save_guess(
        room_code,
        ""
    )


    update_phase(
        room_code,
        "show_roles"
    )