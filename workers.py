import subprocess
import threading
import time
from vision_worker import VisionTextWorker 

class Agent:
    def __init__(self, workers, api_provider="openai", model_name="gpt-4o"):
        self.workers = workers
        self.api_provider = api_provider
        self.model_name = model_name

    def run(self, launch_cmd, num_threads=1, concurrency_interval=1.0):
        print(f"[Agent] Launching command: {launch_cmd}")
        print(f"[Agent] Threads: {num_threads}, Interval: {concurrency_interval}")
        print(f"[Agent] Using model: {self.model_name} via {self.api_provider}")

        # 1) Start the game in a subprocess (non-blocking)
        proc = subprocess.Popen(launch_cmd, shell=True)

        # 2) Background thread to call each worker every interval
        def poll_loop():
            while proc.poll() is None:
                for worker in self.workers:
                    worker.process()
                time.sleep(concurrency_interval)

        thread = threading.Thread(target=poll_loop, daemon=True)
        thread.start()

        # 3) Wait for the game to finish
        proc.wait()
