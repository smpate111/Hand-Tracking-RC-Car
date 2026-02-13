# === LIBRARIES ===
from pathlib import Path
# =================

# === PATHS ===
CURRENT_DIRECTORY = Path(__file__).parent
MODEL_PATH = str(CURRENT_DIRECTORY / 'gesture_recognizer.task')
# =============

# === COLORS (IN BGR FORMAT) ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
# ==============================

# === HAND LANDMARKS' CONNECTIONS ===
HAND_LANDMARKS_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),            # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),            # index finger
    (5, 9), (9, 10), (10, 11), (11, 12),       # middle finger
    (9, 13), (13, 14), (14, 15), (15, 16),     # ring finger
    (13, 17), (17, 18), (18, 19), (19, 20),    # pinky
    (0, 17)                                    # palm
]
# ===================================

# === BOX COORDINATES ===
# define it here so that main.py and hand_visualizer.py can see them
LEFT_BOX = {"x1": 40, "y1": 80, "x2": 270, "y2": 320}
# the right box is calculated dynamically in main.py/hand_visualizer.py based on frame width
# can hardcode the right box here if the frame size is constant
# =======================