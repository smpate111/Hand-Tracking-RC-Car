# === LIBRARIES ===
import cv2
import hand_configurations
# =================

# displays cv2 objects in the frame
class display_objects:
    def __init__(self):
        self.left_box = hand_configurations.LEFT_BOX
        self.right_box = None   # will set this once we know the frame width
        self.frame = None
        self.f_height = None
        self.f_width = None
        self.f_channel = None
        self.hands_data = None
        return
    
    # calculate the hands' active states before drawing them
    def get_active_hand_states(self, frame, hands_data):
        self.frame = frame
        self.f_height, self.f_width, self.f_channel = frame.shape
        self.hands_data = hands_data

        # setup right hand box dynamically based on frame's size (mirroring the left hand box)
        if (self.right_box is None):
            self.right_box = {
                'x1': self.f_width - hand_configurations.LEFT_BOX['x2'],
                'y1': hand_configurations.LEFT_BOX['y1'],
                'x2': self.f_width - hand_configurations.LEFT_BOX['x1'],
                'y2': hand_configurations.LEFT_BOX['y2']
            }

        # track which hand boxes have a hand inside them
        left_hand_active = False
        right_hand_active = False

        for hand in self.hands_data:
             # check if the hand activates a hand box
            if (hand["hand_name"] == "Right"):
                if (self._is_hand_inside_hand_box(hand["hand_landmarks"], self.left_box)):
                    left_hand_active = True
            elif (hand["hand_name"] == "Left"):
                if (self._is_hand_inside_hand_box(hand["hand_landmarks"], self.right_box)):
                    right_hand_active = True

        return left_hand_active, right_hand_active
    
    # helper function that checks if all hand landmarks are inside the given hand box
    def _is_hand_inside_hand_box(self, landmarks, box):
        if (not box):
            return False
        
        points_in_box = 0
        total_points = len(landmarks)

        for (lx, ly) in landmarks:
            px, py = int(lx * self.f_width), int (ly * self.f_height)

            if ((box['x1'] <= px <= box['x2']) and (box['y1'] <= py <= box['y2'])):
                points_in_box = points_in_box + 1

        return points_in_box == total_points
    
    # draw in the frame
    def draw(self, left_motion, left_speed, left_hand_active, right_motion, right_speed, right_hand_active):
        # draw the hands
        for (i, hand) in enumerate(self.hands_data):
            # === NOTE: change this if you want to comment out the hand that you don't need to track, flipped hands due to mirrored frame ===
            # === NOTE: if you need both hands, remove this if statement ==
            #if (hand["hand_name"] == "Right"):
            if (hand["hand_name"] == "Left"):
                # convert the normalized landmarks to frame pixel coordinates
                pixel_landmarks = [(int(lm[0] * self.f_width), int(lm[1] * self.f_height)) for lm in hand["hand_landmarks"]]

                # draw the connections
                for (start_index, end_index) in hand_configurations.HAND_LANDMARKS_CONNECTIONS:
                    # outline line
                    cv2.line(self.frame, pixel_landmarks[start_index], pixel_landmarks[end_index], hand_configurations.BLACK, 10)

                    # colored line
                    cv2.line(self.frame, pixel_landmarks[start_index], pixel_landmarks[end_index], hand_configurations.BLUE, 6)

                # draw hand landmarks
                for (point_x, point_y) in pixel_landmarks:
                    # outline circle
                    cv2.circle(self.frame, (point_x, point_y), 8, hand_configurations.BLACK, -1)

                    # colored circle
                    cv2.circle(self.frame, (point_x, point_y), 6, hand_configurations.RED, -1)

        # === NOTE: comment out the hand that you don't need to track ===

        # draw the hands' boxes
        # === NOTE: green = active, red = not active, flipped target hands due to frame being mirrored ===
        #self._draw_hand_box(self.left_box, left_hand_active, "Right")
        self._draw_hand_box(self.right_box, right_hand_active, "Left")

        # draw the hands' text boxes
        # === NOTE: flipped target hands due to frame being mirrored ===
        #self._draw_text_box(self.left_box, left_hand_active, "Right", left_motion,  left_speed)
        self._draw_text_box(self.right_box, right_hand_active, "Left", right_motion, right_speed)
        
        return

    # helper function that draws hand boxes
    def _draw_hand_box(self, box, is_active, target_hand_name):
        # check if the corresponding hand is inside the frame
        hand_inside_frame = any(hand["hand_name"] == target_hand_name for hand in self.hands_data)

        # determine hand box color based on hand's presence in frame and position in frame
        if (hand_inside_frame == False):
            color = hand_configurations.BLACK
        else:
            if (is_active == True):
                color = hand_configurations.GREEN
            else:
                color = hand_configurations.RED

        # === NOTE: the hand box coordinates are top-left (x1, y1) and bottom-right (x2, y2) ===
        cv2.rectangle(self.frame, (box['x1'], box['y1']), (box['x2'], box['y2']), color, 2)
        return
    
    # helper function that draws text boxes
    def _draw_text_box(self, box, is_active, target_hand_name, motion, speed):
        # check if the corresponding hand is inside the frame
        hand_inside_frame = any(hand["hand_name"] == target_hand_name for hand in self.hands_data)

        # grab the recent hand gesture
        recent_hand_gesture = None

        for hand in self.hands_data:
            if (hand["hand_name"] == target_hand_name):
                #recent_hand_gesture = hand["hand_gesture"] + ' - ' + motion
                recent_hand_gesture = motion + ' - ' + str(speed)

        # determine hand gesture text based on hand's presence in frame and position in frame
        if (hand_inside_frame == True):
            if (is_active == True):
                # === NOTE: the hand box coordinates are top-left (x1, y1) and bottom-right (x2, y2) ===
                cv2.rectangle(self.frame, (box['x1'], box['y2'] + 10), (box['x2'], box['y2'] + 50), hand_configurations.BLACK, -1)
                cv2.putText(self.frame, recent_hand_gesture, (box['x1'] + 5, box['y2'] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45, hand_configurations.WHITE, 1, cv2.LINE_AA)

        return