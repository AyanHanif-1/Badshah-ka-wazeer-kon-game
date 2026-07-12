import sqlite3

DB_NAME = "game.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# -------------------
# TABLE CREATION
# -------------------

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms(
        room_code TEXT PRIMARY KEY,
        phase TEXT,
        round INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_code TEXT,
        player_name TEXT,
        role TEXT,
        score INTEGER,
        ready INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_state(
        room_code TEXT PRIMARY KEY,
        guess TEXT
    )
    """)

    conn.commit()
    conn.close()



# -------------------
# ROOM FUNCTIONS
# -------------------

def create_room(room_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO rooms VALUES (?, ?, ?)
        """,
        (
            room_code,
            "show_roles",
            1
        )
    )

    cursor.execute(
        """
        INSERT INTO game_state VALUES (?,?)
        """,
        (
            room_code,
            ""
        )
    )

    conn.commit()
    conn.close()



def room_exists(room_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT room_code
        FROM rooms
        WHERE room_code=?
        """,
        (room_code,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None



def get_phase(room_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT phase
        FROM rooms
        WHERE room_code=?
        """,
        (room_code,)
    )

    phase = cursor.fetchone()[0]

    conn.close()

    return phase



def update_phase(room_code,phase):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE rooms
        SET phase=?
        WHERE room_code=?
        """,
        (phase,room_code)
    )

    conn.commit()
    conn.close()



# -------------------
# PLAYER FUNCTIONS
# -------------------


def add_player(room_code,name):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        INSERT INTO players
        VALUES(NULL,?,?,?,?,?)
        """,
        (
            room_code,
            name,
            "",
            0,
            0
        )
    )

    conn.commit()
    conn.close()



def get_players(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM players
        WHERE room_code=?
        """,
        (room_code,)
    )

    data=cursor.fetchall()

    conn.close()

    return data



def get_player_names(room_code):

    return [
        player[2]
        for player in get_players(room_code)
    ]



def get_player_count(room_code):

    return len(get_players(room_code))



def player_exists(room_code,name):

    players=get_players(room_code)

    for player in players:

        if player[2]==name:
            return True

    return False



# -------------------
# ROLES
# -------------------


def get_player_role(room_code,name):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT role
        FROM players
        WHERE room_code=?
        AND player_name=?
        """,
        (room_code,name)
    )

    result=cursor.fetchone()

    conn.close()

    return result[0]



def get_player_by_role(room_code,role):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT player_name
        FROM players
        WHERE room_code=?
        AND role=?
        """,
        (room_code,role)
    )

    result=cursor.fetchone()

    conn.close()

    return result[0]



def update_role(room_code,name,role):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET role=?
        WHERE room_code=?
        AND player_name=?
        """,
        (role,room_code,name)
    )

    conn.commit()
    conn.close()



# -------------------
# READY
# -------------------


def set_player_ready(room_code,name):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET ready=1
        WHERE room_code=?
        AND player_name=?
        """,
        (room_code,name)
    )

    conn.commit()
    conn.close()



def all_players_ready(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM players
        WHERE room_code=?
        AND ready=1
        """,
        (room_code,)
    )

    ready=cursor.fetchone()[0]

    conn.close()

    return ready==4



# -------------------
# GUESSING
# -------------------


def save_guess(room_code,guess):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE game_state
        SET guess=?
        WHERE room_code=?
        """,
        (guess,room_code)
    )

    conn.commit()
    conn.close()



def get_guess(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT guess
        FROM game_state
        WHERE room_code=?
        """,
        (room_code,)
    )

    result=cursor.fetchone()

    conn.close()

    return result[0]



# -------------------
# SCORE
# -------------------


def add_score(room_code,name,points):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET score=score+?
        WHERE room_code=?
        AND player_name=?
        """,
        (points,room_code,name)
    )

    conn.commit()
    conn.close()



def get_scores(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT player_name,score
        FROM players
        WHERE room_code=?
        ORDER BY score DESC
        """,
        (room_code,)
    )

    scores=cursor.fetchall()

    conn.close()

    return scores



# -------------------
# ROUND
# -------------------


def next_round(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE rooms
        SET round=round+1
        WHERE room_code=?
        """,
        (room_code,)
    )

    conn.commit()
    conn.close()



def get_round(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT round
        FROM rooms
        WHERE room_code=?
        """,
        (room_code,)
    )

    result=cursor.fetchone()

    conn.close()

    return result[0]

def reset_player_ready(room_code, name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET ready = 0
        WHERE room_code = ?
        AND player_name = ?
        """,
        (room_code, name)
    )

    conn.commit()
    conn.close()

