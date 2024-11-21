# --- FLASK ---#
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('pulse.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/results', methods=['GET'])
def get_results():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM results').fetchall()
    conn.close()
    return jsonify([dict(row) for row in results])



import sqlite3
import pathlib

# --- VARIABLES --- # [] around variables
FILENAME = "pulse.db"
FIRST_RUN = True

# TEST if the FILENAME already exists
if (pathlib.Path.cwd() / FILENAME).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(FILENAME)
CURSOR = CONNECTION.cursor()

# --- SUBROUTINES --- # need addUserPair, getPulses (arr), getScores (arr), insertMatch (actually edits match), insertScores, getIds (return 2 dimensional array) insertPulses
### inputs



def getID():
    global CURSOR, CONNECTION
    id = CURSOR.execute("""
        SELECT
            id
        FROM
            results
        WHERE
            rate IS NULL AND convo IS NULL AND total IS NULL and match IS NULL
    ;""").fetchone()
    CONNECTION.commit() # may need a new col in results
    id = id[0]
    return id

def getUnmatchedIDs():
    global CURSOR, CONNECTION
    ids = CURSOR.execute("""
        SELECT
            id
        FROM
            results
        WHERE
            match IS NULL
    ;""").fetchall()
    CONNECTION.commit() # may need a new col in results
    return ids

def insertPulses(id, time, heartrate1, heartrate2):
    arr = [id, time, heartrate1, heartrate2]

    CURSOR.execute("""
        INSERT INTO 
            heartrate (
                id,
                time,
                heartrate1,
                heartrate2
            )          

        VALUES (
            ?, ?, ?, ?
        )
    ;""", arr)

    CONNECTION.commit()

def addUserPair(): 
    global CURSOR, CONNECTION
    CURSOR.execute("""
        INSERT INTO
            results (
                rate,
                convo,
                total,
                match       
            )
        VALUES (
            NULL, NULL, NULL, NULL
        )   
    ;""")

    CONNECTION.commit()

def getScores(id):
    global CURSOR, CONNECTION
    scores = CURSOR.execute("""
        SELECT
            rate,
            convo,
            total
        FROM
            results
        WHERE
            id = ?
    ;""", [id]).fetchall()
    return scores

def getPulse(id):
    global CURSOR, CONNECTION
    pulses = CURSOR.execute("""
        SELECT
            heartrate1,
            heartrate2
        FROM
            heartrate
        WHERE
            id = ?
    ;""", [id]).fetchall()
    return pulses

def updateMatch(match, id): 
    arr = [match, id]
    CURSOR.execute("""
        UPDATE
            results
        SET
            match = ?
        WHERE
            id = ?
    ;""", arr)
    CONNECTION.commit()

def updateScores(rate, convo, total, id):
    global CURSOR, CONNECTION
    scores = [rate, convo, total, id]
    CURSOR.execute("""
        UPDATE
            results
        SET
            rate = ?,
            convo = ?,
            total = ?
        WHERE
            id = ?
    ;""", scores)

    CONNECTION.commit()

### processing
def setup():
    global CURSOR, CONNECTION  # CONNECTION only needs to be global when writing to the file

    CURSOR.execute("""
        CREATE TABLE
            results (
            id INTEGER PRIMARY KEY,
            rate INTEGER,
            convo INTEGER,
            total INTEGER,
            match INTEGER
            )
    ;""")

    CURSOR.execute("""
        CREATE TABLE
            heartrate (
                id INTEGER,
                time INTEGER,
                heartrate1 INTEGER,
                heartrate2 INTEGER
            )               
    ;""")

    CURSOR.execute("""
        CREATE TABLE
            users (
                id INTEGER PRIMARY KEY,
                password,
                first_name,
                last_name
            ) 

    ;""")

    CURSOR.execute("""
        CREATE TABLE
            pairs (
                pairid INTEGER PRIMARY KEY,
                id1 INTEGER,
                id2 INTEGER
            )     
    ;""")

    CONNECTION.commit()


def deletePair(id):
    """
    deletes a contact from the contact database
    :param CONTACT_ID: int -> primary key
    :return: None
    """
    global CURSOR, CONNECTION

    # DELETE
    CURSOR.execute("""
        DELETE FROM
            results
        WHERE
            id = ?
    ;""", [id])

    CURSOR.execute("""
        DELETE FROM
            heartrate
        WHERE
            id = ?
    ;""", [id])
    CONNECTION.commit()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # --- MAIN PROGRAM CODE --- #
    if FIRST_RUN:
        setup()
    addUserPair()
    id = getID()
    #print(id)
    insertPulses(id, 10, 60, 60)
    insertPulses(id, 20, 60, 60)
    updateScores(9, 8, 4, id)
    updateMatch(1, id)
    print(getPulse(id))
    print(getScores(id))
    print(getUnmatchedIDs)



       