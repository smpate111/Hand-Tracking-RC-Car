# === LIBRARIES ===
import cv2
import time
import mediapipe as mp
from hand_processor import hand_detector
from frame_visualizer import display_objects
from arduino_commands import hand_to_command
# =================

def main():
    # === INITIALIZATION ===
    processor = hand_detector()
    visualizer = display_objects()
    controller = hand_to_command()
    # ======================

    # === OPEN CAMERA ===
    camera = cv2.VideoCapture(0)
    if (not camera.isOpened()):
        print("Error: Could not open camera.")
        return
    # ===================

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
            processor.process_frame(mp_frame, timestamp_ms)

            # get the results
            current_hands = processor.get_recent_hands()

            # check the hands' active states first
            left_hand_active, right_hand_active = visualizer.get_active_hand_states(frame, current_hands)

            # get commands to send to arduino rc car based on hand gesture and position
            left_motion, left_speed, right_motion, right_speed = controller.get_command(current_hands, left_hand_active, right_hand_active)

            # print the command (later I will send this via Serial)
            if (left_motion != "IDLE"):
                #print(f"Sending left hand command to Arduino: {left_motion}")
                pass
            if (right_motion != "IDLE"):
                #print(f"Sending right hand command to Arduino: {right_motion}")
                pass

            # visualize the hands in the frame
            visualizer.draw(left_motion, left_speed, left_hand_active, right_motion, right_speed, right_hand_active)

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