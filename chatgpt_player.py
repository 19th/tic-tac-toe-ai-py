import re
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Load the API key from an environment variable
api_key = os.getenv("CHAT_GPT_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(
    api_key=api_key,
)

def get_gpt_move(board, player):
    global client

    # Convert the board to a string
    board_str = ",".join(board)
    
    # Create the input prompt
    non_ai_player = "O" if player == "X" else "X"

    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo-1106",
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a player in a game of Tic Tac Toe. You are '{player}' and other player is '{non_ai_player}'. The board is a 3x3 grid. Board positions are indexed from 0 to 8, starting from the top-left corner and moving left to right. Respond only with the index of the position you want to place your move."},
            {"role": "user", "content": f"Current board: [{board_str}]"},
        ]
    )
    
    reply = completion.choices[0].message.content
    print("AI move: ", reply)
    move_index = int(re.findall(r'\d+', reply)[0])
    
    return move_index