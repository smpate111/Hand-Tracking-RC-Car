# === LIBRARIES ===
import time
import math
# =================

# tie hand gesture to a command to send to the arduino to perform an action
class hand_to_command:
    def __init__(self):
        self.hands_data = None
        self.COMMAND_DELAY = 1.0    # seconds to hold before sending

        # === LEFT HAND VARIABLES ===
        self.left_motion = "IDLE"
        self.left_speed = 0.0
        self.previous_left_motion = "IDLE"
        self.last_left_start_time = 0.0
        # ===========================

        # === RIGHT HAND VARIABLES ===
        self.right_motion = "IDLE"
        self.right_speed = 0.0
        self.previous_right_motion = "IDLE"
        self.last_right_start_time = 0.0
        # ============================
        return
    
    # dummy function
    def _testing_(self):
        print("qwe")
        print("123")
        return
    
    # determine the command based on which hand is active inside the hand box
    def get_command(self, hands_data, left_hand_active, right_hand_active):
        self.hands_data = hands_data

        # initially set these commands to IDLE in case the hands are out of the frame
        self.left_motion = "IDLE"
        self.right_motion = "IDLE"

        for hand in self.hands_data:
            hand_name = hand["hand_name"]
            landmarks = hand["hand_landmarks"]

            # calculate the hand's geometry
            angle, pf_extension, pinky_extension = self._calculate_hand_geometry(landmarks)

            # calculate command
            reverse_command = False
            if (pinky_extension >= 1.5):
                reverse_command = True

            current_speed_command = pf_extension
            current_motion_command = self._calculate_command(angle, reverse_command)

            # === NOTE: comment out the hand that you don't need to track ===

            # process logic based on which control box the hand is controlling
            # using the same mirrored logic in frame_visualizer.py
            """
            if (hand_name == "Right"):
                (
                    self.left_motion,
                    self.left_speed,
                    self.previous_left_motion,
                    self.last_left_start_time
                ) = self._process_hand_gesture(
                        current_motion_command,
                        current_speed_command,
                        self.previous_left_motion,
                        self.last_left_start_time,
                        left_hand_active
                    )
                # debug statement
                print(f"Left Hand: Angle={angle:.0f} | PF={pf_extension} | Pinky={pinky_extension} | Cmd={current_motion_command}")
            """
            
            if (hand_name == "Left"):
                (
                    self.right_motion,
                    self.right_speed,
                    self.previous_right_motion,
                    self.last_right_start_time
                ) = self._process_hand_gesture(
                        current_motion_command,
                        current_speed_command,
                        self.previous_right_motion,
                        self.last_right_start_time,
                        right_hand_active
                    )
                # debug statement
                print(f"Right Hand: Angle={angle:.0f} | PF={pf_extension} | Pinky={pinky_extension} | Cmd={current_motion_command}")
            #"""

        return self.left_motion, self.left_speed, self.right_motion, self.right_speed

    # helper function that finds the hand's gesture using geometry
    def _calculate_hand_geometry(self, landmarks):
        # get specific landmarks for geometry calculation
        wrist = landmarks[0]
        index_knuckle = landmarks[5]
        index_tip = landmarks[8]
        pinky_knuckle = landmarks[17]
        pinky_tip = landmarks[20]

        # calculate steering angle
        # === NOTE: invert Y because the frame's Y-plane is mirrored
        angle_radians = math.atan2(wrist[1] - index_tip[1], index_tip[0] - wrist[0])
        angle_degrees = math.degrees(angle_radians)

        # calculate pointer finger extension
        pf_tip_distance = math.sqrt((index_tip[0] - wrist[0])**2 + (index_tip[1] - wrist[1])**2)
        pf_knuckle_distance = math.sqrt((index_knuckle[0] - wrist[0])**2 + (index_knuckle[1] - wrist[1])**2)
        
        pf_extension = 0
        if (pf_knuckle_distance != 0):
            pf_extension = pf_tip_distance / pf_knuckle_distance

        # calculate pinky finger extension
        pinky_tip_distance = math.sqrt((pinky_tip[0] - wrist[0])**2 + (pinky_tip[1] - wrist[1])**2)
        pinky_knuckle_distance = math.sqrt((pinky_knuckle[0] - wrist[0])**2 + (pinky_knuckle[1] - wrist[1])**2)

        pinky_extension = 0
        if (pinky_knuckle_distance != 0):
            pinky_extension = pinky_tip_distance / pinky_knuckle_distance

        return angle_degrees, float(format(pf_extension, ".2f")), float(format(pinky_extension, ".2f"))
    
    # helper function that determines which command to send to the car based on the hand gesture
    def _calculate_command(self, angle, reverse_command):
        # base command settings
        command_map = {
            "STRAIGHT": "FORWARD",
            "S_R": "SLIGHT RIGHT",
            "H_R": "HARD RIGHT",
            "S_L": "SLIGHT LEFT",
            "H_L": "HARD LEFT"
        }

        # calculate direction based on angle
        direction = "IDLE"
        if (75 <= angle <= 105):
            direction = command_map["STRAIGHT"]
        elif (45 <= angle < 75):
            direction = command_map["S_R"]
        elif (0 <= angle < 45):
            direction = command_map["H_R"]
        elif(105 < angle <= 135):
            direction = command_map["S_L"]
        elif(135 < angle <= 180):
            direction = command_map["H_L"]

        # apply reverse logic
        if (reverse_command == True):
            if (direction == "FORWARD"):
                return "REVERSE"
            elif (direction != "IDLE"):
                return f"REVERSE {direction}"
            
        return direction
    
    # helper function that validates the hand gesture command before sending it to the car
    def _process_hand_gesture(self, current_motion, current_speed, prev_motion, last_start_time, is_active):
        current_time = time.time()
        final_motion = "IDLE"
        final_speed = 0.0

        # return the state variables so they can be saved back to self
        updated_prev_motion = prev_motion
        updated_start_time = last_start_time

        # if the hand is inside the frame
        if (is_active == True):
            # the gesture changed since the last frame
            if (current_motion != prev_motion):
                updated_prev_motion = current_motion
                updated_start_time = current_time
                final_motion = "IDLE"
                final_speed = 0.0
            # the gesture is the same as the last frame
            else:
                elapsed_time = current_time - last_start_time

                # update the command if held for > COMMAND_DELAY
                if (elapsed_time >= self.COMMAND_DELAY):
                    final_motion = current_motion
                    final_speed = current_speed
                else:
                    final_motion = "IDLE"
                    final_speed = 0.0
        # if the hand is not inside the frame
        else:
            final_motion = "IDLE"
            final_speed = 0.0

        return final_motion, final_speed, updated_prev_motion, updated_start_time