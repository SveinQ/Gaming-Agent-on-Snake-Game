import subprocess
import time
from workers import VisionTextWorker

def main():
    # 1) Kick off the game in its own process
    p = subprocess.Popen(
        ["python", "games/snake/game_logic.py"],
        cwd=".", 
    )

    # 2) Create one VisionTextWorker
    worker = VisionTextWorker(modality="vision-text")

    # 3) Loop until the game quits
    try:
        while p.poll() is None:
            # Read the latest board.txt -> ask GPT -> write move.txt
            worker.process(image=None, text=None)
            # Sleep the same interval your game uses
            time.sleep(0.3)
    except KeyboardInterrupt:
        p.kill()

if __name__ == "__main__":
    main()
