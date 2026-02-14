# === LIBRARIES ===
import cv2
import hand_configurations
# =================

# displays cv2 objects in the frame
class display_objects:
    def __init__(self, frame):
        # === FRAME VARIABLES ===
        self.f_height, self.f_width, self.f_channel = frame.shape
        # =======================
        return
    

    # draw the hand
    def draw_hand(self, frame, hand_landmarks):
        # translate the landmark into the frame's 2D coordinates
        frame_landmarks = [(int(lm[0] * self.f_width), int(lm[1] * self.f_height)) for lm in hand_landmarks]

        self._draw_landmark_connections(frame, frame_landmarks)
        self._draw_hand_landmarks(frame, frame_landmarks)

        return
    

    # helper function that draws the connections between the hand landmarks
    def _draw_landmark_connections(self, frame, frame_landmarks):
        for (start_index, end_index) in hand_configurations.HAND_LANDMARKS_CONNECTIONS:
            # outline line
            cv2.line(frame, frame_landmarks[start_index], frame_landmarks[end_index], hand_configurations.BLACK, 10)

            # colored line
            cv2.line(frame, frame_landmarks[start_index], frame_landmarks[end_index], hand_configurations.BLUE, 6)
        return
    

    # helper function that draws the hand landmarks
    def _draw_hand_landmarks(self, frame, frame_landmarks):
        for (point_x, point_y) in frame_landmarks:
            # outline circle
            cv2.circle(frame, (point_x, point_y), 8, hand_configurations.BLACK, -1)

            # colored circle
            cv2.circle(frame, (point_x, point_y), 6, hand_configurations.RED, -1)
        return


    # draw hand box
    def draw_hand_box(self, frame, hands_data, box, target_hand_name, is_active):
        # check if the corresponding hand is in the frame
        hand_in_frame = any(hand["hand_name"] == target_hand_name for hand in hands_data)

        # determine hand box color based on hand's presence in frame and position in frame
        color = self._change_box_color(hand_in_frame, is_active)

        # === NOTE: the hand box coordinates are top-left (x1, y1) and bottom-right (x2, y2) ===
        cv2.rectangle(frame, (box['x1'], box['y1']), (box['x2'], box['y2']), color, 2)
        return
    

    # helper function that returns color based on hand's presence and position in frame
    def _change_box_color(self, hand_in_frame, is_active):
        if (hand_in_frame == True):
            if (is_active == True):
                return hand_configurations.GREEN
            else:
                return hand_configurations.RED
        else:
            return hand_configurations.BLACK
    

    # draw text box
    def draw_text_box(self, frame, hands_data, box, target_hand_name, is_active, motion, speed):
        # check if the corresponding hand is in the frame
        hand_in_frame = any(hand["hand_name"] == target_hand_name for hand in hands_data)

        # determine hand gesture text based on hand's presence in frame and position in frame
        if ((hand_in_frame == True) and (is_active == True)):
            #recent_hand_gesture = hand["hand_gesture"] + ' - ' + motion
            recent_hand_gesture = motion + ' - ' + str(speed)

            # === NOTE: the hand box coordinates are top-left (x1, y1) and bottom-right (x2, y2) ===
            cv2.rectangle(frame, (box['x1'], box['y2'] + 10), (box['x2'], box['y2'] + 50), hand_configurations.BLACK, -1)
            cv2.putText(frame, recent_hand_gesture, (box['x1'] + 5, box['y2'] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45, hand_configurations.WHITE, 1, cv2.LINE_AA)

        return