# 🏎️ Hand-Controlled-RC-Car

AI-controlled RC car using MediaPipe Hand Tracking and Arduino. Python + Computer Vision. I built this project to learn how to design and program a robot from the ground up, specifically exploring Human-Robot Interaction by replacing traditional controllers with vision-based gesture recognition.

## 📦 Technologies
- `Python`

### 📚 Libraries:
- `pathlib`
- `MediaPipe`
- `OpenCV`
- `time`

## 🛠️ Features
Here are the project's key functionalities:
- **Region of Interest (ROI) Detection:** The system uses a defined "activation box" inside the frame. This is to make sure that the gesture tracking is only active when the user's hand is correctly positioned inside the box to prevent erratic movement from the background noise.
- **Intuitive Gesture Mapping:** A real-time hand pose estimation is translated into vehicle kinematics. For example, a vertical finger orientation triggers a forward propulsion, while curling the finger acts as a brake.

## 👨🏼‍🍳 The Process
The project's development started by establishing a real-time vision pipeline using `OpenCV` to capture video frames for Google's `MediaPipe` pose estimation ([link to documentation](https://ai.google.dev/edge/mediapipe/solutions/guide)). I implemented spatial constraints inside the frame to serve as a safety "dead-man's switch" to make sure the user is properly positioned before the system initializes the hardware control.

I developed a custom gesture-mapping algorithm to translate the hand landmarks into precise directional commands. For example, the system calculates the vector orientation from the wrist to the index finger to determine the target input of the steering wheel.

To make sure that the system is stable and there's little-to-no noise, I created a command-validation filter. This filter requires the user to maintain a specific hand gesture for a defined threshold before the command is executed to prevent erratic motor responses and simulate realistic input latency.

## 📖 What I Learned
During this project, I've picked up important skills and a better understanding of complex ideas, which improved my logical thinking.

### Real-Time Computer Vision:
- I optimized the `MediaPipe` and `OpenCV` libraries to minimize latency and provide ample time to process the hand gestures before commanding a vehicle to move.

### Coordinate Mapping & Transformation:
- Implemented a gesture-translation algorithm that maps 3D hand landmarks into actuation commands.

### System Constraints & Robustness:
- Developed fail-safes in the system to prevent unintended movement from noise or background interference by defining control zones and gesture requirements.

### Overall Growth:
Each part of this project helped me understand more about designing robots, managing complex information, and enhancing user experience by allowing me to solve unique problems, learn new concepts, and improve my skills for future work.

## 💭 How can it be improved?
- Add timer logic to give the system time to process the command made by the hand gesture before sending it to the RC car. [✅]
- Add velocity by calculating the finger's extension ratio. [✅]
- Clean the code by organizing it based on its functionality. [✅]
- Incorporate the RC car code. []

## 🚦 Running the Project
To run the project in your local environment, follow these steps:
1. Clone the repository to your local machine.
2. Run `pip install -r requirements.txt` to install the required Python libraries.
3. Have a webcam hooked up to your computer and change the `camera = cv2.VideoCapture()` line in `main.py` to the port the webcam is connected to.
4. Run `python main.py` to start the project.