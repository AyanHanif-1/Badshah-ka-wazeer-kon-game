import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


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
        id SERIAL PRIMARY KEY,
        room_code TEXT,
        player_name TEXT,
        role TEXT,
        score INTEGER,
        ready BOOLEAN DEFAULT FALSE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_state(
        room_code TEXT PRIMARY KEY,
        guess TEXT
    )
    """)

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



# -------------------
# ROOM FUNCTIONS
# -------------------

def create_room(room_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO rooms VALUES (%s, %s, %s)
        """,
        (room_code,"show_roles",1)
    )

    cursor.execute(
        """
        INSERT INTO game_state VALUES (%s,%s)
        """,
        (room_code,"")
    )

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



def room_exists(room_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT room_code
        FROM rooms
        WHERE room_code=%s
        """,
        (room_code,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None



def get_phase(room_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT phase
        FROM rooms
        WHERE room_code=%s
        """,
        (room_code,)
    )

    phase = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return phase



def update_phase(room_code,phase):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE rooms
        SET phase=%s
        WHERE room_code=%s
        """,
        (phase,room_code)
    )

    conn.commit()
    cursor.close()
    cursor.close()
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
        (room_code, player_name, role, score, ready)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (room_code, name, "", 0, False)
    )

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



def get_players(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM players
        WHERE room_code=%s
        """,
        (room_code,)
    )

    data=cursor.fetchall()

    cursor.close()
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
        WHERE room_code=%s
        AND player_name=%s
        """,
        (room_code,name)
    )

    result=cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]



def get_player_by_role(room_code,role):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT player_name
        FROM players
        WHERE room_code=%s
        AND role=%s
        """,
        (room_code,role)
    )

    result=cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]



def update_role(room_code,name,role):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET role=%s
        WHERE room_code=%s
        AND player_name=%s
        """,
        (role,room_code,name)
    )

    conn.commit()
    cursor.close()
    cursor.close()
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
        SET ready=TRUE
        WHERE room_code=%s
        AND player_name=%s
        """,
        (room_code,name)
    )

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



def all_players_ready(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM players
        WHERE room_code=%s
        AND ready=TRUE
        """,
        (room_code,)
    )

    ready=cursor.fetchone()[0]

    cursor.close()
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
        SET guess=%s
        WHERE room_code=%s
        """,
        (guess,room_code)
    )

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



def get_guess(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT guess
        FROM game_state
        WHERE room_code=%s
        """,
        (room_code,)
    )

    result=cursor.fetchone()

    cursor.close()
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
        SET score=score+%s
        WHERE room_code=%s
        AND player_name=%s
        """,
        (points,room_code,name)
    )

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



def get_scores(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT player_name,score
        FROM players
        WHERE room_code=%s
        ORDER BY score DESC
        """,
        (room_code,)
    )

    scores=cursor.fetchall()

    cursor.close()
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
        WHERE room_code=%s
        """,
        (room_code,)
    )

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



def get_round(room_code):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT round
        FROM rooms
        WHERE room_code=%s
        """,
        (room_code,)
    )

    result=cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0]

def reset_player_ready(room_code, name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET ready = FALSE
        WHERE room_code = %s
        AND player_name = %s
        """,
        (room_code, name)
    )

    conn.commit()
    cursor.close()
    cursor.close()
    conn.close()



