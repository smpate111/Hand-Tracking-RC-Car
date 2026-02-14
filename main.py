# === LIBRARIES ===
import cv2
import time
import mediapipe as mp
import hand_configurations
from hand_tracker import hand_detector
from render_frame import display_objects
from process_command import hand_to_command
# =================

def main():
    # === INITIALIZATION ===
    left_box = hand_configurations.LEFT_BOX
    right_box = hand_configurations.RIGHT_BOX
    detector = hand_detector()
    # ======================

    # === OPEN CAMERA ===
    camera = cv2.VideoCapture(0)
    if (not camera.isOpened()):
        print("Error: Could not open camera.")
        return
    # ===================

    # === PROCESS INITIAL FRAME ===
    ret, initial_frame = camera.read()
    if (ret):
        left_processor = hand_to_command(initial_frame)
        right_processor = hand_to_command(initial_frame)
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

            # initialize the hand's active state
            left_hand_active = False
            left_motion = "IDLE"
            left_speed = 0.0

            right_hand_active = False
            right_motion = "IDLE"
            right_speed = 0.0

            # visualize the hands in the frame
            for (i, hand) in enumerate(current_hands):
                hand_name = hand["hand_name"]
                hand_landmarks = hand["hand_landmarks"]

                # === NOTE: comment out the hand that you don't need to track ===
                # === NOTE: flipped target hand due to frame being mirrored ===
                
                # === LEFT HAND ===
                if (hand_name == "Right"):
                    left_hand_active = left_processor.determine_hand_state(hand_name, hand_landmarks, left_box)
                    left_motion, left_speed = left_processor.get_command(left_hand_active, "Left", hand_landmarks)
                    visualizer.draw_hand(frame, hand_landmarks)
                # =================

                # === RIGHT HAND ===
                if (hand_name == "Left"):
                    right_hand_active = right_processor.determine_hand_state(hand_name, hand_landmarks, right_box)
                    right_motion, right_speed = right_processor.get_command(right_hand_active, "Right", hand_landmarks)
                    visualizer.draw_hand(frame, hand_landmarks)
                # ==================

            # get commands to send to arduino rc car based on hand gesture and position
            #left_motion, left_speed, right_motion, right_speed, angle = processor.get_command(current_hands, left_hand_active, right_hand_active)

            # print the command (later I will send this via Serial)
            if (left_motion != "IDLE"):
                #print(f"Sending left hand command to Arduino: {left_motion}")
                pass
            if (right_motion != "IDLE"):
                #print(f"Sending right hand command to Arduino: {right_motion}")
                pass

            # === NOTE: comment out the hand that you don't need to track ===
            # === NOTE: flipped target hand due to frame being mirrored ===
            # hand in box = green, hand not in box = red

            # === LEFT HAND ===
            visualizer.draw_hand_box(frame, current_hands, left_box, "Right", left_hand_active)
            visualizer.draw_text_box(frame, current_hands, left_box, "Right", left_hand_active, left_motion,  left_speed)
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