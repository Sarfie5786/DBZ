import socket
import ssl
import re
import time
import sqlite3

SERVER = "irc.esper.net"
PORT = 6697
NICK = "Shenron"
CHANNELS = [
    "#DBZ-OOC",
    "#DBZ-RPG",
    "#DBZ-Saga",
    "#DBZ-OPs",
    "#DBZ-TrainingWorld",
    "#ShenronTest"
]
REGULAR_RP_CHANNEL = "#DBZ-RPG"
TRAINING_RP_CHANNEL = "#DBZ-TrainingWorld"
SAGA_RP_CHANNEL = "#DBZ-Saga"
TEST_CHANNEL = "#ShenronTest"
POST_TIMEOUT = 1.0
OWNER_NICK = "`Sara"
DATABASE = "dragonballs.db"
VALID_RACES = {
    "human": "Human",
    "kurin": "Kurin",
    "saiyan": "Saiyan",
    "dark_saiyan": "Dark Saiyan",
    "android": "Android",
    "namekian": "Namekian",
    "wearl_wolf": "Wearl - Wolf",
    "wearl_bear": "Wearl - Bear",
    "wearl_hawk": "Wearl - Hawk",
    "wearl_dragon": "Wearl - Dragon",
    "custom": "Custom",
    "halfling": "Halfling"
}
TRANSFORMATIONS = {
    # =========================
    # HUMAN
    # =========================

    "Human_Extreme_Rage": {
        "name": "Extreme Rage",
        "race": "Human",
        "required_pl": 0,
        "power_multiplier": 2,
        "speed_multiplier": 1
    },

    "Awakened": {
        "name": "Awakened",
        "race": "Human",
        "required_pl": 30000,
        "power_multiplier": 4,
        "speed_multiplier": 4
    },

    "Enlightened": {
        "name": "Enlightened",
        "race": "Human",
        "required_pl": 60000,
        "power_multiplier": 6,
        "speed_multiplier": 6
    },

    "Transcendant": {
        "name": "Transcendant",
        "race": "Human",
        "required_pl": 90000,
        "power_multiplier": 8,
        "speed_multiplier": 8
    },

    "Ascended": {
        "name": "Ascended",
        "race": "Human",
        "required_pl": 130000,
        "power_multiplier": 10,
        "speed_multiplier": 10
    },


    # =========================
    # KURIN
    # =========================

    "Kurin_Extreme_Rage": {
        "name": "Extreme Rage",
        "race": "Kurin",
        "required_pl": 0,
        "power_multiplier": 2,
        "speed_multiplier": 1
    },

    "Rabid_Beast": {
        "name": "Rabid Beast",
        "race": "Kurin",
        "required_pl": 30000,
        "power_multiplier": 4,
        "speed_multiplier": 4
    },

    "Beast_Form": {
        "name": "Beast Form",
        "race": "Kurin",
        "required_pl": 60000,
        "power_multiplier": 6,
        "speed_multiplier": 6
    },

    "Dire_Form": {
        "name": "Dire Form",
        "race": "Kurin",
        "required_pl": 90000,
        "power_multiplier": 8,
        "speed_multiplier": 8
    },

    "Mythical_Form": {
        "name": "Mythical Form",
        "race": "Kurin",
        "required_pl": 130000,
        "power_multiplier": 10,
        "speed_multiplier": 10
    },


    # =========================
    # DARK SAIYAN
    # =========================

    "Dark_Oozaru": {
        "name": "Dark Oozaru",
        "race": "Dark Saiyan",
        "required_pl": 0,
        "power_multiplier": 2,
        "speed_multiplier": 3
    },

    "Dark_Super_Saiyan": {
        "name": "Dark Super Saiyan",
        "race": "Dark Saiyan",
        "required_pl": 35000,
        "power_multiplier": 3,
        "speed_multiplier": 5
    },

    "Dark_Super_Saiyan_2": {
        "name": "Dark Super Saiyan 2",
        "race": "Dark Saiyan",
        "required_pl": 65000,
        "power_multiplier": 5,
        "speed_multiplier": 7
    },

    "Dark_Super_Saiyan_3": {
        "name": "Dark Super Saiyan 3",
        "race": "Dark Saiyan",
        "required_pl": 95000,
        "power_multiplier": 7,
        "speed_multiplier": 9
    },

    "Dark_Saiyan_God": {
        "name": "Dark Saiyan God",
        "race": "Dark Saiyan",
        "required_pl": 140000,
        "power_multiplier": 9,
        "speed_multiplier": 11
    },


    # =========================
    # ANDROID
    # =========================

    "Limiter_Release": {
        "name": "Limiter Release",
        "race": "Android",
        "required_pl": 30000,
        "power_multiplier": 3,
        "speed_multiplier": 5
    },

    "Power_Surge": {
        "name": "Power Surge",
        "race": "Android",
        "required_pl": 60000,
        "power_multiplier": 6,
        "speed_multiplier": 6
    },

    "Overdrive_Mode": {
        "name": "Overdrive Mode",
        "race": "Android",
        "required_pl": 90000,
        "power_multiplier": 8,
        "speed_multiplier": 7
    },

    "System_Overload": {
        "name": "System Overload",
        "race": "Android",
        "required_pl": 130000,
        "power_multiplier": 10,
        "speed_multiplier": 10
    },


    # =========================
    # NAMEKIAN
    # =========================

    "Expansion": {
        "name": "Expansion",
        "race": "Namekian",
        "required_pl": 0,
        "power_multiplier": 3,
        "speed_multiplier": 1
    },

    "Mystic_Namekian": {
        "name": "Mystic Namekian",
        "race": "Namekian",
        "required_pl": 35000,
        "power_multiplier": 3,
        "speed_multiplier": 5
    },

    "Enlightened_Namekian": {
        "name": "Enlightened Namekian",
        "race": "Namekian",
        "required_pl": 65000,
        "power_multiplier": 5,
        "speed_multiplier": 7
    },

    "Divine_Namekian": {
        "name": "Divine Namekian",
        "race": "Namekian",
        "required_pl": 90000,
        "power_multiplier": 7,
        "speed_multiplier": 9
    },

    "Namekian_God": {
        "name": "Namekian God",
        "race": "Namekian",
        "required_pl": 135000,
        "power_multiplier": 9,
        "speed_multiplier": 11
    },


    # =========================
    # WEARL - WOLF
    # =========================

    "Lycan": {
        "name": "Lycan",
        "race": "Wearl - Wolf",
        "required_pl": 0,
        "power_multiplier": 3,
        "speed_multiplier": 2
    },

    "Grey_Wolf": {
        "name": "Grey Wolf",
        "race": "Wearl - Wolf",
        "required_pl": 35000,
        "power_multiplier": 5,
        "speed_multiplier": 3
    },

    "Red_Wolf": {
        "name": "Red Wolf",
        "race": "Wearl - Wolf",
        "required_pl": 65000,
        "power_multiplier": 7,
        "speed_multiplier": 5
    },

    "Dire_Wolf": {
        "name": "Dire Wolf",
        "race": "Wearl - Wolf",
        "required_pl": 100000,
        "power_multiplier": 9,
        "speed_multiplier": 7
    },

    "God_of_Wolves": {
        "name": "God of Wolves",
        "race": "Wearl - Wolf",
        "required_pl": 140000,
        "power_multiplier": 11,
        "speed_multiplier": 9
    },


    # =========================
    # WEARL - BEAR
    # =========================

    "Ursus": {
        "name": "Ursus",
        "race": "Wearl - Bear",
        "required_pl": 0,
        "power_multiplier": 3,
        "speed_multiplier": 2
    },

    "Sun_Bear": {
        "name": "Sun Bear",
        "race": "Wearl - Bear",
        "required_pl": 30000,
        "power_multiplier": 6,
        "speed_multiplier": 2
    },

    "Grizzled_Bear": {
        "name": "Grizzled Bear",
        "race": "Wearl - Bear",
        "required_pl": 65000,
        "power_multiplier": 8,
        "speed_multiplier": 4
    },

    "Dire_Bear": {
        "name": "Dire Bear",
        "race": "Wearl - Bear",
        "required_pl": 100000,
        "power_multiplier": 10,
        "speed_multiplier": 6
    },

    "Great_Bear_Spirit": {
        "name": "Great Bear Spirit",
        "race": "Wearl - Bear",
        "required_pl": 140000,
        "power_multiplier": 12,
        "speed_multiplier": 8
    },


    # =========================
    # WEARL - HAWK
    # =========================

    "Hawk_Spirit": {
        "name": "Hawk Spirit",
        "race": "Wearl - Hawk",
        "required_pl": 35000,
        "power_multiplier": 3,
        "speed_multiplier": 5
    },

    "Grey_Spirit": {
        "name": "Grey Spirit",
        "race": "Wearl - Hawk",
        "required_pl": 65000,
        "power_multiplier": 5,
        "speed_multiplier": 7
    },

    "Dire_Hawk": {
        "name": "Dire Hawk",
        "race": "Wearl - Hawk",
        "required_pl": 100000,
        "power_multiplier": 7,
        "speed_multiplier": 9
    },

    "God_of_Hawks": {
        "name": "God of Hawks",
        "race": "Wearl - Hawk",
        "required_pl": 140000,
        "power_multiplier": 9,
        "speed_multiplier": 11
    },
    #=======================
    # Wearl - Dragon
    #=======================

    "Draconian_Aspect": {
        "name": "Draconian Aspect",
        "race": "Wearl - Dragon",
        "required_pl": 30000,
        "power_multiplier": 5,
        "speed_multiplier": 5
    },

    "Draconic_Visage": {
        "name": "Draconic Visage",
        "race": "Wearl - Dragon",
        "required_pl": 65000,
        "power_multiplier": 7,
        "speed_multiplier": 7
    },

    "True_Dragon": {
        "name": "True Dragon",
        "race": "Wearl - Dragon",
        "required_pl": 100000,
        "power_multiplier": 9,
        "speed_multiplier": 9
    },

    "Divine_Wyrm": {
        "name": "Divine Wyrm",
        "race": "Wearl - Dragon",
        "required_pl": 140000,
        "power_multiplier": 11,
        "speed_multiplier": 11
    },

    #=======================
    # Saiyan
    #=======================

    "Oozaru": {
    "name": "Oozaru",
    "race": "Saiyan",
    "required_pl": 0,
    "power_multiplier": 3,
    "speed_multiplier": 2
    },

    "Super_Saiyan_1": {
        "name": "Super Saiyan 1",
        "race": "Saiyan",
        "required_pl": 35000,
        "power_multiplier": 5,
        "speed_multiplier": 3
    },

    "Super_Saiyan_2": {
        "name": "Super Saiyan 2",
        "race": "Saiyan",
        "required_pl": 65000,
        "power_multiplier": 7,
        "speed_multiplier": 5
    },

    "Super_Saiyan_3": {
        "name": "Super Saiyan 3",
        "race": "Saiyan",
        "required_pl": 100000,
        "power_multiplier": 9,
        "speed_multiplier": 7
    },

    "Saiyan_God": {
        "name": "Saiyan God",
        "race": "Saiyan",
        "required_pl": 140000,
        "power_multiplier": 11,
        "speed_multiplier": 9
    }
}

            # Character tags Shenron knows about.
characters = {
"<<Loralei Kassell>>": "Loralei Kassell",
"{:==Aurica==o": "Aurica",
"§Verge§": "Verge",
"[Ruco]:": "Ruco"
}

last_message_time={}

# Create a normal network connection.
sock = socket.create_connection((SERVER, PORT))

def setup_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character TEXT NOT NULL,
            sender TEXT NOT NULL,
            channel TEXT NOT NULL,
            mode TEXT NOT NULL,
            words INTEGER NOT NULL,
            rp_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
            character_name TEXT NOT NULL UNIQUE,
            base_pl INTEGER NOT NULL DEFAULT 10000,
            base_speed INTEGER NOT NULL DEFAULT 100,
            tech_points INTEGER NOT NULL DEFAULT 0,
            regular_checkpoint INTEGER NOT NULL DEFAULT 0,
            training_checkpoint INTEGER NOT NULL DEFAULT 0,
            saga_checkpoint INTEGER NOT NULL DEFAULT 0,
            active INTEGER NOT NULL DEFAULT 1,
            tp_checkpoint INTEGER NOT NULL DEFAULT 0,
            race TEXT NOT NULL DEFAULT 'Unassigned',
            racial_pl_bonus INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL UNIQUE COLLATE NOCASE
            )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transformations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER NOT NULL,
            transformation TEXT NOT NULL,
            UNIQUE(character_id, transformation),
            FOREIGN KEY(character_id) REFERENCES characters(id)
        )
    """)
     # Add stat columns to older databases if they do not exist yet.
    cursor.execute("PRAGMA table_info(characters)")
    character_columns = [row[1] for row in cursor.fetchall()]

    if "base_pl" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN base_pl INTEGER NOT NULL DEFAULT 10000
        """)

    if "base_speed" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN base_speed INTEGER NOT NULL DEFAULT 100
        """)

    if "tech_points" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN tech_points INTEGER NOT NULL DEFAULT 0
        """)

    if "regular_checkpoint" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN regular_checkpoint INTEGER NOT NULL DEFAULT 0
        """)

    if "training_checkpoint" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN training_checkpoint INTEGER NOT NULL DEFAULT 0
        """)

    if "saga_checkpoint" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN saga_checkpoint INTEGER NOT NULL DEFAULT 0
        """)

    if "active" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN active INTEGER NOT NULL DEFAULT 1
        """)

    if "tp_checkpoint" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN tp_checkpoint INTEGER NOT NULL DEFAULT 0
        """)

    if "race" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN race TEXT NOT NULL DEFAULT 'Unassigned'
        """)

    if "racial_pl_bonus" not in character_columns:
        cursor.execute("""
            ALTER TABLE characters
            ADD COLUMN racial_pl_bonus INTEGER NOT NULL DEFAULT 0
        """)
    connection.commit()
    connection.close()

    print("Database ready.")

def get_character_stats(character):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            base_pl,
            base_speed,
            tech_points,
            regular_checkpoint,
            training_checkpoint,
            saga_checkpoint,
            race,
            racial_pl_bonus
        FROM characters
        WHERE character_name = ?
    """, (character,))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return None

    return {
        "base_pl": result[0],
        "base_speed": result[1],
        "tech_points": result[2],
        "regular_checkpoint": result[3],
        "training_checkpoint": result[4],
        "saga_checkpoint": result[5],
        "race": result[6],
        "racial_pl_bonus": result[7]
    }

def calculate_tp_gain(old_earned_pl, new_earned_pl, tp_multiplier=1):
    if new_earned_pl <= old_earned_pl:
        return 0

    tp_gained = 0

    old_milestone = old_earned_pl // 1000
    new_milestone = new_earned_pl // 1000

    for milestone in range(old_milestone + 1, new_milestone + 1):
        milestone_pl = milestone * 1000

        if milestone_pl % 5000 == 0:
            tp_gained += 5
        else:
            tp_gained += 1 * tp_multiplier

    return tp_gained

def get_tp_checkpoint(character):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT tp_checkpoint
        FROM characters
        WHERE character_name = ?
          AND active = 1
    """, (character,))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return None

    return result[0]


def award_tech_points(character, amount, new_checkpoint):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE characters
        SET tech_points = tech_points + ?,
            tp_checkpoint = ?
        WHERE character_name = ?
          AND active = 1
    """, (
        amount,
        new_checkpoint,
        character
    ))

    connection.commit()
    connection.close()

def set_character_pl(character, amount):
    regular_words = get_word_total(character, "REGULAR")
    training_words = get_word_total(character, "TRAINING")
    saga_words = get_word_total(character, "SAGA")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE characters
        SET base_pl = ?,
            regular_checkpoint = ?,
            training_checkpoint = ?,
            saga_checkpoint = ?,
            tp_checkpoint = 0
        WHERE character_name = ?
    """, (
        amount,
        regular_words,
        training_words,
        saga_words,
        character
    ))

    connection.commit()
    connection.close()

def set_character_race(character, race):
    if race == "Wearl - Bear":
        racial_pl_bonus = 2000
    else:
        racial_pl_bonus = 0

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE characters
        SET race = ?,
            racial_pl_bonus = ?
        WHERE character_name = ?
          AND active = 1
    """, (
        race,
        racial_pl_bonus,
        character
    ))

    connection.commit()
    connection.close()

def set_character_speed(character, amount):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE characters
        SET base_speed = ?
        WHERE character_name = ?
    """, (amount, character))

    connection.commit()
    connection.close()


def set_character_tp(character, amount):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE characters
        SET tech_points = ?
        WHERE character_name = ?
    """, (amount, character))

    connection.commit()
    connection.close()

def add_character(command_name, character_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO characters (
            command_name,
            character_name,
            base_pl,
            base_speed,
            tech_points
        )
        VALUES (?, ?, 10000, 100, 0)
    """, (command_name, character_name))

    added = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return added

def delete_character(command_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE characters
        SET active = 0
        WHERE command_name = ?
          AND active = 1
    """, (command_name,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted

def restore_character(command_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT character_name
        FROM characters
        WHERE command_name = ?
          AND active = 0
    """, (command_name,))

    result = cursor.fetchone()

    if result is None:
        connection.close()
        return None

    character_name = result[0]

    cursor.execute("""
        UPDATE characters
        SET active = 1
        WHERE command_name = ?
          AND active = 0
    """, (command_name,))

    connection.commit()
    connection.close()

    return character_name

def get_character(command_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT character_name
        FROM characters
        WHERE command_name = ?
          AND active = 1
    """, (command_name,))

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return result[0]

def is_operator(nickname):
    # The owner always has permission.
    if nickname.lower() == OWNER_NICK.lower():
        return True

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM operators
        WHERE nickname = ?
    """, (nickname,))

    result = cursor.fetchone()
    connection.close()

    return result is not None


def add_operator(nickname):
    # Owner doesn't need to be stored in the table.
    if nickname.lower() == OWNER_NICK.lower():
        return False

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO operators (nickname)
        VALUES (?)
    """, (nickname,))

    added = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return added


def delete_operator(nickname):
    # Nobody gets to delete the owner.
    if nickname.lower() == OWNER_NICK.lower():
        return False

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM operators
        WHERE nickname = ?
    """, (nickname,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted

def save_activity(character, sender, channel, mode, words, rp_text):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO activity (
            character,
            sender,
            channel,
            mode,
            words,
            rp_text
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (character, sender, channel, mode, words, rp_text))

    connection.commit()
    connection.close()

    print(f"ACTIVITY SAVED: {character} | {mode} | {words} words")

def show_activity():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, character, sender, channel, mode, words, rp_text, timestamp
        FROM activity
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    for row in rows:
        print(row)

def get_word_total(character, mode):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(words), 0)
        FROM activity
        WHERE character = ? AND mode = ?
    """, (character, mode))

    total = cursor.fetchone()[0]

    connection.close()

    return total

def calculate_pl(character):
    character_stats = get_character_stats(character)

    if character_stats is None:
        return None

    regular_words = get_word_total(character, "REGULAR")
    training_words = get_word_total(character, "TRAINING")
    saga_words = get_word_total(character, "SAGA")

    regular_progress_words = max(
        0,
        regular_words - character_stats["regular_checkpoint"]
    )

    training_progress_words = max(
        0,
        training_words - character_stats["training_checkpoint"]
    )

    saga_progress_words = max(
        0,
        saga_words - character_stats["saga_checkpoint"]
    )

    regular_blocks = regular_progress_words // 100
    training_blocks = training_progress_words // 100
    saga_blocks = saga_progress_words // 100

    regular_earned_pl = regular_blocks * 10
    training_earned_pl = training_blocks * 12
    saga_earned_pl = saga_blocks * 15

    earned_pl = regular_earned_pl + training_earned_pl + saga_earned_pl

    raw_pl = (
        character_stats["base_pl"]
        + character_stats["racial_pl_bonus"]
        + earned_pl
    )

    usable_pl = max(
        100,
        (raw_pl // 100) * 100
    )

    # Speed increases by 1 for every 100 PL earned
    # through RP progression.
    earned_speed = earned_pl // 100
    speed = character_stats["base_speed"] + earned_speed

    return {
        "raw_pl": raw_pl,
        "usable_pl": usable_pl,
        "speed": speed,
        "tech_points": character_stats["tech_points"],
        "race": character_stats["race"],
        "earned_pl": earned_pl,
        "regular_progress": regular_progress_words % 100,
        "training_progress": training_progress_words % 100,
        "saga_progress": saga_progress_words % 100
    }

def send_message(target, message):
    send(f"PRIVMSG {target} :{message}")

def unlock_transformation(character, transformation):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM characters
        WHERE character_name = ?
          AND active = 1
    """, (character,))

    result = cursor.fetchone()

    if result is None:
        connection.close()
        return False

    character_id = result[0]

    cursor.execute("""
        INSERT OR IGNORE INTO transformations (
            character_id,
            transformation
        )
        VALUES (?, ?)
    """, (character_id, transformation))

    unlocked = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return unlocked


def get_transformations(character):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT t.transformation
        FROM transformations t
        JOIN characters c
            ON t.character_id = c.id
        WHERE c.character_name = ?
          AND c.active = 1
        ORDER BY t.id
    """, (character,))

    results = cursor.fetchall()
    connection.close()

    return [row[0] for row in results]

setup_database()

# Wrap it in SSL/TLS so we're using EsperNet's secure connection.
context = ssl.create_default_context()
irc = context.wrap_socket(sock, server_hostname=SERVER)
irc.settimeout(0.1)

def send(message):
    """Send a raw IRC command to EsperNet."""
    print(">>>", message)
    irc.sendall((message + "\r\n").encode("utf-8"))

def strip_irc_formatting(text):
    # Remove mIRC color codes
    text = re.sub(r'\x03(?:\d{1,2}(?:,\d{1,2})?)?', '', text)

    # Remove other IRC formatting codes
    text = re.sub(r'[\x02\x0f\x16\x1d\x1e\x1f\x11]', '', text)

    return text


# Introduce Shenron to the server.
send(f"NICK {NICK}")
send(f"USER {NICK} 0 * :Shenron")

buffer = ""

post_buffers = {}

def finish_post(sender):
    post = post_buffers.pop(sender, None)

    if post is None:
        return

    character = post["character"]
    rp_text = post["text"]
    word_count = len(rp_text.split())
    channel = post["channel"]

    if channel.lower() == REGULAR_RP_CHANNEL.lower():
        rp_mode = "REGULAR"
    elif channel.lower() == TRAINING_RP_CHANNEL.lower():
        rp_mode = "TRAINING"
    elif channel.lower() == SAGA_RP_CHANNEL.lower():
        rp_mode = "SAGA"
    elif channel.lower() == TEST_CHANNEL.lower():
        rp_mode = "TEST"
    else:
        rp_mode = "NONE"

    if rp_mode in ("REGULAR", "TRAINING", "SAGA", "TEST"):
        save_activity(
            character,
            sender,
            channel,
            rp_mode,
            word_count,
            rp_text
        )

    if rp_mode in ("REGULAR", "TRAINING", "SAGA"):
        stats = calculate_pl(character)

        if stats is not None:
            earned_pl = stats["earned_pl"]
            tp_checkpoint = get_tp_checkpoint(character)

            race = stats["race"]

            if race in ("Human", "Wearl - Hawk"):
                tp_multiplier = 2
            else:
                tp_multiplier = 1

            if tp_checkpoint is not None:
                tp_gained = calculate_tp_gain(
                    tp_checkpoint,
                    earned_pl,
                    tp_multiplier
                )

            if tp_gained > 0:
                new_checkpoint = (earned_pl // 1000) * 1000

                award_tech_points(
                    character,
                    tp_gained,
                    new_checkpoint
                )

    print("=== POST COMPLETE ===")
    print(f"CHARACTER: {character}")
    print(f"CHANNEL: {channel}")
    print(f"MODE: {rp_mode}")
    print(f"RP TEXT: {rp_text!r}")
    print(f"WORDS: {word_count}")
    print("=====================")

while True:
    try:
        data = irc.recv(4096)
    except socket.timeout:
        data = None

    if data == b"":
        print("Disconnected from EsperNet.")
        break

    if data:
        buffer += data.decode("utf-8", errors="ignore")

    # IRC messages end with CRLF.
    now = time.time()

    for buffered_sender, post in list(post_buffers.items()):
        if now - post["last_time"] >= POST_TIMEOUT:
            finish_post(buffered_sender)

    while "\r\n" in buffer:
        line, buffer = buffer.split("\r\n", 1)

        print("<<<", line)

        # EsperNet periodically sends PING.
        # We MUST answer or it'll disconnect Shenron.
        if line.startswith("PING "):
            send("PONG " + line[5:])

        # Numeric 001 means registration succeeded.
        if " 001 " in line:
            for channel in CHANNELS:
                send(f"JOIN {channel}")

        # Listen for messages sent to a channel or directly to Shenron.
        if " PRIVMSG " in line:
            prefix, rest = line.split(" PRIVMSG ", 1)
            sender = prefix.split("!")[0][1:]
            target, message = rest.split(" :", 1)

            if message.startswith("!"):
                parts = message.split()

                transformation_key = parts[0][1:]

                if transformation_key in TRANSFORMATIONS:
                    if not is_operator(sender):
                        send_message(
                            target,
                            "You do not have permission to use that command."
                        )
                        continue

                    if len(parts) != 2:
                        send_message(
                            target,
                            f"Usage: !{transformation_key} <character>"
                        )
                        continue

                    command_name = parts[1]
                    character = get_character(command_name)

                    if character is None:
                        send_message(
                            target,
                            f"I don't know a character named {command_name}."
                        )
                        continue

                    stats = calculate_pl(character)
                    transformation = TRANSFORMATIONS[transformation_key]

                    if stats["race"] != transformation["race"]:
                        send_message(
                            target,
                            f"{character} cannot unlock "
                            f"{transformation['name']}."
                        )
                        continue

                    if stats["usable_pl"] < transformation["required_pl"]:
                        send_message(
                            target,
                            f"{character} needs "
                            f"{transformation['required_pl']:,} PL "
                            f"to unlock {transformation['name']}."
                        )
                        continue

                    if unlock_transformation(
                        character,
                        transformation_key
                    ):
                        send_message(
                            target,
                            f"{character} has unlocked "
                            f"{transformation['name']}!"
                        )
                    else:
                        send_message(
                            target,
                            f"{character} already has "
                            f"{transformation['name']} unlocked."
                        )

                    continue

            if message.lower() == "!help":
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                send_message(
                    sender,
                    "Shenron Admin Commands:"
                )

                send_message(
                    sender,
                    "!addchar <key> <character name> | "
                    "!delchar <key> | "
                    "!restorechar <key>"
                )

                send_message(
                    sender,
                    "!setpl <key> <amount> | "
                    "!setsp <key> <amount> | "
                    "!settp <key> <amount> | "
                    "!setrace <key> <race>"
                )

                send_message(
                    sender,
                    "Transformation Commands: "
                    "!<transformation key> <character key>"
                )

                send_message(
                    sender,
                    "Human: "
                    "Human_Extreme_Rage, Awakened, Enlightened, "
                    "Transcendant, Ascended"
                )

                send_message(
                    sender,
                    "Kurin: "
                    "Kurin_Extreme_Rage, Rabid_Beast, Beast_Form, "
                    "Dire_Form, Mythical_Form"
                )

                send_message(
                    sender,
                    "Saiyan: "
                    "Oozaru, Super_Saiyan_1, Super_Saiyan_2, "
                    "Super_Saiyan_3, Saiyan_God"
                )

                send_message(
                    sender,
                    "Dark Saiyan: "
                    "Dark_Oozaru, Dark_Super_Saiyan, "
                    "Dark_Super_Saiyan_2, Dark_Super_Saiyan_3, "
                    "Dark_Saiyan_God"
                )

                send_message(
                    sender,
                    "Android: "
                    "Limiter_Release, Power_Surge, Overdrive_Mode, "
                    "System_Overload"
                )

                send_message(
                    sender,
                    "Namekian: "
                    "Expansion, Mystic_Namekian, "
                    "Enlightened_Namekian, Divine_Namekian, "
                    "Namekian_God"
                )

                send_message(
                    sender,
                    "Wearl - Wolf: "
                    "Lycan, Grey_Wolf, Red_Wolf, Dire_Wolf, "
                    "God_of_Wolves"
                )

                send_message(
                    sender,
                    "Wearl - Bear: "
                    "Ursus, Sun_Bear, Grizzled_Bear, Dire_Bear, "
                    "Great_Bear_Spirit"
                )

                send_message(
                    sender,
                    "Wearl - Hawk: "
                    "Hawk_Spirit, Grey_Spirit, Dire_Hawk, "
                    "God_of_Hawks"
                )

                send_message(
                    sender,
                    "Wearl - Dragon: "
                    "Draconian_Aspect, Draconic_Visage, True_Dragon, "
                    "Divine_Wyrm"
                )

                if sender.lower() == OWNER_NICK.lower():
                    send_message(
                        sender,
                        "!addop <nick> | "
                        "!delop <nick> | "
                        "!shutdown"
                    )

                continue

            if message.lower().startswith("!addop "):
                if sender.lower() != OWNER_NICK.lower():
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                nickname = message[7:].strip()

                if not nickname:
                    send_message(
                        target,
                        "Usage: !addop <nickname>"
                    )
                    continue

                if add_operator(nickname):
                    send_message(
                        target,
                        f"{nickname} has been granted OP permissions."
                    )
                else:
                    send_message(
                        target,
                        f"{nickname} already has OP permissions."
                    )

                continue

            if message.lower().startswith("!delop "):
                if sender.lower() != OWNER_NICK.lower():
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                nickname = message[7:].strip()

                if not nickname:
                    send_message(
                        target,
                        "Usage: !delop <nickname>"
                    )
                    continue

                if nickname.lower() == OWNER_NICK.lower():
                    send_message(
                        target,
                        "The owner cannot be removed."
                    )
                    continue

                if delete_operator(nickname):
                    send_message(
                        target,
                        f"{nickname}'s OP permissions have been removed."
                    )
                else:
                    send_message(
                        target,
                        f"{nickname} does not have OP permissions."
                    )

                continue

            if message.lower().startswith("!restorechar "):
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                command_name = message[13:].strip()

                if not command_name:
                    send_message(
                        target,
                        "Usage: !restorechar <character key>"
                    )
                    continue

                character = restore_character(command_name)

                if character is None:
                    send_message(
                        target,
                        f"I don't know an archived character named {command_name}."
                    )
                else:
                    send_message(
                        target,
                        f"Character restored: {character}"
                    )

                continue

            
            if message.lower().startswith("!addchar "):
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue
            
                parts = message.split(" ", 2)

                if len(parts) < 3:
                    send_message(
                        target,
                        "Usage: !addchar <command name> <character name>"
                    )
                    continue

                command_name = parts[1].strip()
                character_name = parts[2].strip()

                if add_character(command_name, character_name):
                    send_message(
                        target,
                        f"Character registered: {character_name}"
                    )
                else:
                    send_message(
                        target,
                        "That character name or character key is already registered."
                    )

                continue

            if message.lower().startswith("!delchar "):
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                command_name = message[9:].strip()

                if not command_name:
                    send_message(
                        target,
                        "Usage: !delchar <character>"
                    )
                    continue

                character = get_character(command_name)

                if character is None:
                    send_message(
                        target,
                        f"I don't know an active character named {command_name}."
                    )
                    continue

                delete_character(command_name)

                send_message(
                    target,
                    f"Character removed: {character}"
                )

                continue
            
            if message.lower().startswith("!stats "):
                command_name = message[7:].strip()
                character = get_character(command_name)

                if character is None:
                    send_message(
                        target,
                        f"I don't know a character named {command_name}."
                    )
                    continue

                stats = calculate_pl(character)

                send_message(
                    target,
                    f"{character} | "
                    f"Race: {stats['race']} | "
                    f"PL: {stats['usable_pl']:,} | "
                    f"Speed: {stats['speed']:,} | "
                    f"TP: {stats['tech_points']:,}"
                )

                unlocked_transformations = get_transformations(character)

                for transformation_key in unlocked_transformations:
                    transformation = TRANSFORMATIONS.get(
                        transformation_key
                    )

                    if transformation is None:
                        continue

                    transformed_pl = (
                        stats["usable_pl"]
                        * transformation["power_multiplier"]
                    )

                    transformed_speed = (
                        stats["speed"]
                        * transformation["speed_multiplier"]
                    )

                    send_message(
                        target,
                        f"{transformation['name']} | "
                        f"PL: {transformed_pl:,} | "
                        f"Speed: {transformed_speed:,}"
                    )

                continue

            if message.lower().startswith("!setsp "):
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                parts = message.split()

                if len(parts) != 3:
                    send_message(
                        target,
                        "Usage: !setsp <character> <amount>"
                    )
                    continue

                command_name = parts[1]
                amount_text = parts[2]

                character = get_character(command_name)

                if character is None:
                    send_message(
                        target,
                        f"I don't know a character named {command_name}."
                    )
                    continue

                try:
                    amount = int(amount_text)
                except ValueError:
                    send_message(
                        target,
                        "Speed must be a whole number."
                    )
                    continue

                if amount < 0:
                    send_message(
                        target,
                        "Speed cannot be negative."
                    )
                    continue

                set_character_speed(character, amount)

                send_message(
                    target,
                    f"{character}'s Speed has been set to {amount:,}."
                )

                continue

            if message.lower().startswith("!setpl "):
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                parts = message.split()

                if len(parts) != 3:
                    send_message(
                        target,
                        "Usage: !setpl <character> <amount>"
                    )
                    continue

                command_name = parts[1]
                amount_text = parts[2]

                character = get_character(command_name)

                if character is None:
                    send_message(
                        target,
                        f"I don't know a character named {command_name}."
                    )
                    continue

                try:
                    amount = int(amount_text)
                except ValueError:
                    send_message(
                        target,
                        "PL must be a whole number."
                    )
                    continue

                if amount < 100:
                    send_message(
                        target,
                        "PL cannot be lower than 100."
                    )
                    continue

                set_character_pl(character, amount)

                send_message(
                    target,
                    f"{character}'s PL has been set to {amount:,}."
                )

                continue

            if message.lower().startswith("!setrace "):
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                parts = message.split()

                if len(parts) != 3:
                    send_message(
                        target,
                        "Usage: !setrace <character> <race>"
                    )
                    continue

                command_name = parts[1]
                race_key = parts[2].lower()

                character = get_character(command_name)

                if character is None:
                    send_message(
                        target,
                        f"I don't know a character named {command_name}."
                    )
                    continue

                if race_key not in VALID_RACES:
                    send_message(
                        target,
                        "Unknown race. Valid races: "
                        + ", ".join(VALID_RACES.keys())
                    )
                    continue

                race = VALID_RACES[race_key]

                set_character_race(character, race)

                send_message(
                    target,
                    f"{character}'s race has been set to {race}."
                )

                continue

            if message.lower().startswith("!settp "):
                if not is_operator(sender):
                    send_message(
                        target,
                        "You do not have permission to use that command."
                    )
                    continue

                parts = message.split()

                if len(parts) != 3:
                    send_message(
                        target,
                        "Usage: !settp <character> <amount>"
                    )
                    continue

                command_name = parts[1]
                amount_text = parts[2]

                character = get_character(command_name)

                if character is None:
                    send_message(
                        target,
                        f"I don't know a character named {command_name}."
                    )
                    continue

                try:
                    amount = int(amount_text)
                except ValueError:
                    send_message(
                        target,
                        "TP must be a whole number."
                    )
                    continue

                if amount < 0:
                    send_message(
                        target,
                        "TP cannot be negative."
                    )
                    continue

                set_character_tp(character, amount)

                send_message(
                    target,
                    f"{character}'s TP has been set to {amount:,}."
                )

                continue
        # Get the nickname from the IRC prefix.

            now = time.time()

            if sender in last_message_time:
                gap = now - last_message_time[sender]
                print(f"GAP FROM {sender}: {gap:.3f} seconds")

            last_message_time[sender] = now

            print(f"MESSAGE: {sender} -> {target}: {message}")

            clean_message = strip_irc_formatting(message)

            print(f"CLEAN: {clean_message!r}")
            print(f"STARTS WITH: {clean_message[:30]!r}")

            found_character = False

            for tag, character in characters.items():
                if clean_message.startswith(tag):
                    found_character = True

                    # A new tagged message means a new logical post.
                    # Finish any previous post from this sender first.
                    if sender in post_buffers:
                        finish_post(sender)

                    rp_text = clean_message[len(tag):].strip()

                    post_buffers[sender] = {
                        "character": character,
                        "text": rp_text,
                        "channel": target,
                        "last_time": time.time()
                    }

                    print(f"POST STARTED: {character}")
                    print(f"FIRST CHUNK: {rp_text!r}")

                    break

            if not found_character and sender in post_buffers:
                post_buffers[sender]["text"] += " " + clean_message.strip()
                post_buffers[sender]["last_time"] = time.time()

                print(
                    f"CONTINUATION: "
                    f"{post_buffers[sender]['character']} <- {clean_message!r}"
                )

            if message.lower() == "!shutdown":
                if sender.lower() == OWNER_NICK.lower():
                    send("QUIT :The Dragon Balls have scattered...")
                    irc.close()
                    raise SystemExit