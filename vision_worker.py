import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Set API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY") #input your API Key

class VisionTextWorker:
    def __init__(self, modality="vision-text"):
        self.modality = modality

    def process(self, image=None, text=None):
        # 1) read the latest board
        try:
            board = open("board.txt").read()
        except FileNotFoundError:
            print("[VisionTextWorker] board.txt missing")
            return

        # 2) Prompting the AI
        prompt = (
            "You are an AI playing Snake on a 12x12 grid.\n"
            "Legend: S = Snake head, s = snake body, F = Food, . = empty space.\n"
            "You want to reach the food (F) without crashing into your body (s).\n"
            "Here is the current board:\n\n"
            """Avoid crashing into your body (s). If no safe move 
            exists, pick the direction with the most open space.\n"""
            + board +
            "\n\nRespond ONLY with one of: UP, DOWN, LEFT, RIGHT."
            
)

        # 3) call OpenAI
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o", # Change this to "gpt-4o" or "gpt-3.5-turbo"
                messages=[
                  {"role":"system","content":"You are a snake‐playing AI."},
                  {"role":"user","content":prompt}
                ],
                temperature=0.2,
                max_tokens=1
            )
            move = resp.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"[VisionTextWorker] API error: {e}")
            move = "RIGHT"

        if move not in ("UP","DOWN","LEFT","RIGHT"):
            print(f"[VisionTextWorker] Bad move '{move}', defaulting to RIGHT")
            move = "RIGHT"

        # 4) This outputs the moves the snake made to the txt file
        with open("move.txt", "w") as f:
            f.write(move)

        print(f"[VisionTextWorker] → {move}")

        with open("moves.txt", "a") as log:
            log.write(move + "\n")
