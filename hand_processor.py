# === LIBRARIES ===
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import hand_configurations
# =================

# detects the hand in the frame and processes it using mediapipe
class hand_detector:
    def __init__(self):
        self.result = None

        # initialize mediapipe
        base_options = python.BaseOptions(model_asset_path=hand_configurations.MODEL_PATH)
        options = vision.GestureRecognizerOptions(base_options=base_options, running_mode=vision.RunningMode.LIVE_STREAM, num_hands=2, result_callback=self._callback)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        return
    
    # internal callback to store the latest result asynchronously
    def _callback(self, result, output_image, timestamp_ms: int):
        self.result = result
        return
    
    # sends the frame to mediapipe for processing
    def process_frame(self, mp_frame, timestamp_ms: int):
        self.recognizer.recognize_async(mp_frame, timestamp_ms)
        return

    # returns a list of detected hands or nothing
    # parses the raw mediapipe result into a simpler formate for main.py
    def get_recent_hands(self):
        if ((not self.result) or (not self.result.handedness)):
            return []
        
        hands_data = []
        result = self.result

        for i in range(len(result.handedness)):
            # extract detected hand and gesture
            hand = result.handedness[i][0]
            gesture = result.gestures[i][0]

            # extract basic information
            name = hand.category_name
            gesture_name = gesture.category_name
            gesture_score = gesture.score

            # extract the hand landmarks
            landmarks = [[lm.x, lm.y] for lm in result.hand_landmarks[i]]

            # store the information into a dictionary for easy access
            hand_information = {
                "hand_name": name,
                "hand_gesture": gesture_name,
                "hand_gesture_score": gesture_score,
                "hand_landmarks": landmarks,
                "display_test": f"{name} hand: ({gesture_name}) - Confidence: ({gesture_score:.2f})"
            }

            hands_data.append(hand_information)

        return hands_data