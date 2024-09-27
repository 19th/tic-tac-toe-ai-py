import sqlite3

def execute(query, params=()):
    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.lastrowid

def select_all(query, params=()):
    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

def save_game(player_x, player_o, winner, is_finished=False):
    return execute("INSERT INTO game (player_x, player_o, winner, is_finished) VALUES (?, ?, ?, ?)", (player_x, player_o, winner, is_finished))

def update_game(game_id, winner, is_finished=True):
    return execute("UPDATE game SET winner = ?, is_finished = ? WHERE game_id = ?", (winner, is_finished, game_id))

def save_step(game_id, player, step_number, position):
    return execute("INSERT INTO game_step (game_id, player, step_number, position) VALUES (?, ?, ?, ?)", (game_id, player, step_number, position))

def get_history():
    return select_all("SELECT * FROM game")

def get_steps(game_id):
    return select_all("SELECT * FROM game_step WHERE game_id = ? ORDER BY step_number", (game_id,))

# Create the database
with open('db.sql', 'r') as f:
    for create_table_query in f.read().split('-- split'):
        execute(create_table_query)
