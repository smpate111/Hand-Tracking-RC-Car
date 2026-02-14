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
x1 = 40
y1 = 80
x2 = 270
y2 = 320
LEFT_BOX = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

# the frame's size (change these values whenever the size changes)
f_width = 640
f_height = 480

# change these to whatever values you want (these are set to mirror the left box)
new_x1 = f_width - x2
new_x2 = f_width - x1

# define it here so that main.py and hand_visualizer.py can see them
x1 = new_x1
y1 = y1
x2 = new_x2
y2 = y2
RIGHT_BOX = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
# the right box is calculated dynamically in main.py/hand_visualizer.py based on frame width
# can hardcode the right box here if the frame size is constant
# =======================