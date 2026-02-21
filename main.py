# === LIBRARIES ===
import cv2
import time
import mediapipe as mp
import serial

import hand_configurations
from hand_tracker import hand_detector
from render_frame import display_objects
from process_command import assign_command
# =================

def main():
    # === INITIALIZATION ===
    left_box = hand_configurations.LEFT_BOX
    right_box = hand_configurations.RIGHT_BOX
    detector = hand_detector()
    COM_PORT = 'COM11'
    BAUD_RATE = 9600
    # ======================

    # === ARDUINO SERIAL SETUP ===
    try:
        arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)   # give the arduino a moment to reset after connecting
        print("Connected to Arduino...")
    except Exception as e:
        print(f"Error: Could not connect to Arduino: {e}")
        return
    # ============================

    # set up last Arduino command
    last_arduino_command = b'Q'

    # === OPEN CAMERA ===
    camera = cv2.VideoCapture(0)
    if (not camera.isOpened()):
        print("Error: Could not open camera.")
        return
    # ===================

    # === PROCESS INITIAL FRAME ===
    ret, initial_frame = camera.read()
    if (ret):
        left_processor = assign_command(initial_frame)
        right_processor = assign_command(initial_frame)
    else:
        print("Error: Could not read in the initial frame.")
        return
    # =============================

    # === MAIN INFINITY LOOP ===
    try:
        while (camera.isOpened()):
            # determine if frame was read
            # skip current loop's iteration if frame wasn't read
            ret, frame = camera.read()
            if (not ret):
                continue

            # prepare the frame
            frame = cv2.flip(frame, 1)      # mirror effect
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # process the frame using mediapipe
            mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = int(time.time() * 1000)
            detector.process_frame(mp_frame, timestamp_ms)

            # get the results
            current_hands = detector.get_recent_hands()

            # initialize the hands into the frame
            visualizer = display_objects(frame)

            # initialize the hands' information

            # === LEFT HAND ===
            left_hand_active = False
            left_motion = "IDLE"
            left_speed = 0.0
            # =================

            # === RIGHT HAND ===
            right_hand_active = False
            right_motion = "IDLE"
            right_speed = 0.0
            # ==================

            # visualize the hands in the frame
            for (i, hand) in enumerate(current_hands):
                hand_name = hand["hand_name"]
                hand_landmarks = hand["hand_landmarks"]

                # === NOTE: comment out the hand that you don't need to track ===
                # === NOTE: flipped target hand due to frame being mirrored ===
                
                # === LEFT HAND ===
                #if (hand_name == "Right"):
                #    left_hand_active = left_processor.determine_hand_state(True, hand_landmarks, left_box)
                #    left_motion, left_speed = left_processor.get_command(left_hand_active, "Left", hand_landmarks)
                #    visualizer.draw_hand(frame, hand_landmarks)
                # =================

                # === RIGHT HAND ===
                if (hand_name == "Left"):
                    right_hand_active = right_processor.determine_hand_state(True, hand_landmarks, right_box)
                    right_motion, right_speed = right_processor.get_command(right_hand_active, "Right", hand_landmarks)
                    visualizer.draw_hand(frame, hand_landmarks)
                # ==================

            # command to send to Arduino and initialize the IDLE command
            arduino_command = b'Z'

            # configure which command to send

            """
            if (left_hand_active == True):
                print(f"Sending left hand command to Arduino: {left_motion}")

                if (left_motion == "FORWARD"):
                    arduino_command = b'Q'
                elif (left_motion == "SLIGHT LEFT"):
                    arduino_command = b'W'
                elif (left_motion == "LEFT"):
                    arduino_command = b'E'
                elif (left_motion == "HARD LEFT"):
                    arduino_command = b'R'
                elif (left_motion == "SLIGHT RIGHT"):
                    arduino_command = b'T'
                elif (left_motion == "RIGHT"):
                    arduino_command = b'Y'
                elif (left_motion == "HARD RIGHT"):
                    arduino_command = b'U'
                elif (left_motion == "REVERSE"):
                    arduino_command = b'A'
                elif (left_motion == "REVERSE SLIGHT LEFT"):
                    arduino_command = b'S'
                elif (left_motion == "REVERSE LEFT"):
                    arduino_command = b'D'
                elif (left_motion == "REVERSE HARD LEFT"):
                    arduino_command = b'F'
                elif (left_motion == "REVERSE SLIGHT RIGHT"):
                    arduino_command = b'G'
                elif (left_motion == "REVERSE RIGHT"):
                    arduino_command = b'H'
                elif (left_motion == "REVERSE HARD RIGHT"):
                    arduino_command = b'J'
                elif (left_motion == "IDLE"):
                    arduino_command = b'Z'
            """

            if (right_hand_active == True):
                print(f"Sending right hand command to Arduino: {right_motion}")

                if (right_motion == "FORWARD"):
                    arduino_command = b'Q'
                elif (right_motion == "SLIGHT LEFT"):
                    arduino_command = b'W'
                elif (right_motion == "LEFT"):
                    arduino_command = b'E'
                elif (right_motion == "HARD LEFT"):
                    arduino_command = b'R'
                elif (right_motion == "SLIGHT RIGHT"):
                    arduino_command = b'T'
                elif (right_motion == "RIGHT"):
                    arduino_command = b'Y'
                elif (right_motion == "HARD RIGHT"):
                    arduino_command = b'U'
                elif (right_motion == "REVERSE"):
                    arduino_command = b'A'
                elif (right_motion == "REVERSE SLIGHT LEFT"):
                    arduino_command = b'S'
                elif (right_motion == "REVERSE LEFT"):
                    arduino_command = b'D'
                elif (right_motion == "REVERSE HARD LEFT"):
                    arduino_command = b'F'
                elif (right_motion == "REVERSE SLIGHT RIGHT"):
                    arduino_command = b'G'
                elif (right_motion == "REVERSE RIGHT"):
                    arduino_command = b'H'
                elif (right_motion == "REVERSE HARD RIGHT"):
                    arduino_command = b'J'
                elif (right_motion == "IDLE"):
                    arduino_command = b'Z'
            #"""
                
            # send the command to the Arduino if it is a different command
            if (arduino_command != last_arduino_command):
                arduino.write(arduino_command)
                last_arduino_command = arduino_command
                print(f"Sent to Arduino: {arduino_command.decode()}")

            # === NOTE: comment out the hand that you don't need to track ===
            # === NOTE: flipped target hand due to frame being mirrored ===
            # hand in box = green, hand not in box = red

            # === LEFT HAND ===
            #visualizer.draw_hand_box(frame, current_hands, left_box, "Right", left_hand_active)
            #visualizer.draw_text_box(frame, current_hands, left_box, "Right", left_hand_active, left_motion,  left_speed)
            # =================

            # === RIGHT HAND ===
            visualizer.draw_hand_box(frame, current_hands, right_box, "Left", right_hand_active)
            visualizer.draw_text_box(frame, current_hands, right_box, "Left", right_hand_active, right_motion, right_speed)
            # ==================

            # display the visualized hands in the frame
            cv2.imshow('Hand Controller', frame)

            # if user presses q to quit the program
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
    finally:
        # exit the livestream and destroy all cv2 objects
        camera.release()
        cv2.destroyAllWindows()
    # ==========================

if __name__ == '__main__':
    main()