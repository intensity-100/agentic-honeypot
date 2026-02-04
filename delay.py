import random
import time

STAGE_DELAYS = {
    "baiting": (3, 6),
    "trust": (5, 10),
    "extraction": (7, 15),
    "closing": (10, 20)
}

def human_delay(stage: str):
    low, high = STAGE_DELAYS.get(stage, (4, 8))
    delay = random.randint(low, high)
    time.sleep(delay)
