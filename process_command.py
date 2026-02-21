# === LIBRARIES ===
import time
import math
# =================

# tie hand gesture to a command to send to the arduino to perform an action
class assign_command:
    def __init__(self, frame):
        # === FRAME VARIABLES ===
        self.f_height, self.f_width, self.f_channel = frame.shape
        # =======================

        # === TIMING VARIABLES ===
        self.previous_motion = None
        self.last_start_time = 0.0
        self.COMMAND_DELAY = 2.0    # seconds to hold before sending the command
        # ========================
        return
    

    # calculate the hand's state before drawing them
    def determine_hand_state(self, hand_in_frame, hand_landmarks, box):
        # check if the hand activates a hand box
        if (hand_in_frame == False):
            return False
        
        return self._is_hand_in_box(hand_landmarks, box)
    

    # helper function that checks if all hand landmarks are inside the given hand box
    def _is_hand_in_box(self, landmarks, box):
        if (not box):
            return False
        
        # calculate the amount of landmarks inside the hand box
        landmarks_in_box = 0
        for (lx, ly) in landmarks:
            # translate the landmark into the frame's 2D coordinates
            px, py = int(lx * self.f_width), int (ly * self.f_height)

            if ((box['x1'] <= px <= box['x2']) and (box['y1'] <= py <= box['y2'])):
                landmarks_in_box = landmarks_in_box + 1

        total_landmarks = len(landmarks)

        return landmarks_in_box == total_landmarks
    

    # determine the command based on which hand is active inside the hand box
    def get_command(self, is_active, hand_name, landmarks):
        current_motion = "IDLE"
        current_speed = 0.0
        angle_degrees = 0

        # get specific landmarks for geometry calculation
        wrist = landmarks[0]
        index_knuckle = landmarks[5]
        index_tip = landmarks[8]
        pinky_knuckle = landmarks[17]
        pinky_tip = landmarks[20]

        # calculate steering angle
        angle_degrees = self._calculate_steering_angle(wrist, index_tip)

        # calculate pointer finger extension
        pf_extension = self._calculate_finger_extension(index_tip, index_knuckle, wrist)
        current_speed = pf_extension

        # calculate pinky finger extension
        pinky_extension = self._calculate_finger_extension(pinky_tip, pinky_knuckle, wrist)

        # calculate direction based on angle
        direction = self._calculate_wheel_direction(angle_degrees)

        # calculate reverse motion
        reverse_motion = False
        if (pinky_extension >= 1.5):
            reverse_motion = True

        # apply reverse logic
        current_motion = self._apply_reverse(direction, reverse_motion)

        # # return nothing if hand is not in the frame
        if (is_active == True):
            current_motion, current_speed = self._process_hand_gesture(current_motion, current_speed)
        
        # debug statement
        #print(f"{hand_name} Hand: Angle={angle_degrees:.0f} | PF={pf_extension} | Pinky={pinky_extension} | Cmd={current_motion}")

        return current_motion, current_speed
    

    # helper function that calculates the steering angle
    # === NOTE: invert Y because the frame's Y-plane is mirrored
    def _calculate_steering_angle(self, wrist, index_tip):
        angle_radians = math.atan2(wrist[1] - index_tip[1], index_tip[0] - wrist[0])
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees
    

    # helper function that calculates the extension of a finger
    def _calculate_finger_extension(self, finger_tip, finger_knuckle, wrist):
        ft_distance = math.sqrt((finger_tip[0] - wrist[0])**2 + (finger_tip[1] - wrist[1])**2)
        fk_distance = math.sqrt((finger_knuckle[0] - wrist[0])**2 + (finger_knuckle[1] - wrist[1])**2)

        f_extension = 0
        if (fk_distance != 0):
            f_extension = ft_distance / fk_distance

        return float(format(f_extension, ".2f"))

    
    # helper function that calculates the direction of the steering wheel based on the wrist's angle
    def _calculate_wheel_direction(self, angle):
        # base command settings
        command_map = {
            "STRAIGHT": "FORWARD",
            "S_R": "SLIGHT RIGHT",
            "R": "RIGHT",
            "H_R": "HARD RIGHT",
            "S_L": "SLIGHT LEFT",
            "L": "LEFT",
            "H_L": "HARD LEFT",
            "I": "IDLE"
        }

        # return the direction based on the angle
        if (0 <= angle <= 25):
            return command_map["H_R"]
        elif (25 < angle <= 50):
            return command_map["R"]
        elif (50 < angle <= 75):
            return command_map["S_R"]
        elif (75 < angle <= 105):
            return command_map["STRAIGHT"]
        elif (105 < angle <= 130):
            return command_map["S_L"]
        elif (130 < angle <= 155):
            return command_map["L"]
        elif (155 < angle <= 180):
            return command_map["H_L"]
        
        return command_map["I"]
    

    # helper function that applies the reverse logic if the pinky finger is fully extended
    def _apply_reverse(self, direction, reverse_command):
        if (reverse_command == False):
            return direction
        
        if (direction == "FORWARD"):
            return "REVERSE"
        
        if (direction != "IDLE"):
            return f"REVERSE {direction}"
        
        return direction
    

    # helper function that validates the hand gesture command before sending it to the car
    def _process_hand_gesture(self, current_motion, current_speed):
        current_time = time.time()
        final_motion = "IDLE"
        final_speed = 0.0

        # return the state variables so they can be saved back to self
        updated_prev_motion = self.previous_motion
        updated_start_time = self.last_start_time

        # update the previous frame's motion and time if it doesn't match the current frame's motion
        if (current_motion != self.previous_motion):
            updated_prev_motion = current_motion
            updated_start_time = current_time

        else:
            elapsed_time = current_time - self.last_start_time

            # update the command if held for > COMMAND_DELAY
            if (elapsed_time >= self.COMMAND_DELAY):
                final_motion = current_motion
                final_speed = current_speed

        # update the previous frame's variables
        self.previous_motion = updated_prev_motion
        self.last_start_time = updated_start_time

        return final_motion, final_speed