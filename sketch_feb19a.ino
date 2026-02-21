// === INITIALIZE VARIABLES ===

// === MOTOR PINS ===
int in1 = 6;
int in2 = 8;
int in3 = 10;
int in4 = 12;
// ==================

// === MOTOR SPEEDS ===
float speed = 150.0;
float left_speed = 30.0;
float right_speed = 50.0;
float MINIMUM_SPEED = 100.0;
float MAXIMUM_SPEED = 255.0;
// ====================

// === USER INPUT ===
int state;
String last_command = "IDLE/STOP";
// ==================

// ============================

void setup() {
  // put your setup code here, to run once:

  // create serial monitor
  Serial.begin(9600);

  // motor controller pins
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  Serial.println("System Ready.");
}

// function that adjusts the motors' speed based on user's input
float adjust_speed(int state, float speed) {
  // 1: increase speed by 1
  // 2: increase speed by 5
  // 3: increase speed by 10
  // 4: decrease speed by 1
  // 5: decrease speed by 5
  // 6: decrease speed by 10

  // adjust the speed based on the user's input
  switch (state) {
    case '1':
      speed = speed + 1;
      break;
    case '2':
      speed = speed + 5;
      break;
    case '3':
      speed = speed + 10;
      break;
    case '4':
      speed = speed - 1;
      break;
    case '5':
      speed = speed - 5;
      break;
    case '6':
      speed = speed - 10;
      break;
    default:
      speed = speed + 0;
      break;
  }

  // if the speed is less than the MINIMUM_SPEED or goes past the MAXIMUM_SPEED then set it to either MINIMUM_SPEED or MAXIMUM_SPEED (min/max allowed speeds)
  speed = constrain(speed, MINIMUM_SPEED, MAXIMUM_SPEED);

  return speed;
}

// function that kickstarts the motors if the speed is too low to output due to friction
void kickstart_motors(String command_name, String last_command, float in1_value, float in2_value, float in3_value, float in4_value) {
  // check if the command is not to stop and is not the same command as the last recorded command
  int pulsed = 0;
  if ((command_name != "IDLE/STOP") && (command_name != last_command)) {
    pulsed = 1;
  }

  if (pulsed == 1) {
    // apply the temporary speeds to the motors
    if (in1_value < MINIMUM_SPEED) {
      analogWrite(in1, MINIMUM_SPEED);
    }
    if (in2_value < MINIMUM_SPEED) {
      analogWrite(in2, MINIMUM_SPEED);
    }
    if (in3_value < MINIMUM_SPEED) {
      analogWrite(in3, MINIMUM_SPEED);
    }
    if (in4_value < MINIMUM_SPEED) {
      analogWrite(in4, MINIMUM_SPEED);
    }

    // set a delay to set the burst's duration
    delay(50);
  }

  return;
}

// function that turns on the motors based on the command from the user's input
void drive(String command_name, float in1_value, float in2_value, float in3_value, float in4_value) {
  // print out the command's information
  Serial.print("Command: ");
  Serial.print(command_name);
  Serial.print(" -- In1: ");
  Serial.print(in1_value);
  Serial.print(" -- In2: ");
  Serial.print(in2_value);
  Serial.print(" -- In3: ");
  Serial.print(in3_value);
  Serial.print(" -- In4: ");
  Serial.print(in4_value);
  Serial.println();

  // start the motors if the speed is too slow for the motors to turn on
  kickstart_motors(command_name, last_command, in1_value, in2_value, in3_value, in4_value);

  // apply the speeds to the motors
  analogWrite(in1, in1_value);
  analogWrite(in2, in2_value);
  analogWrite(in3, in3_value);
  analogWrite(in4, in4_value);

  // set the last command to the current command
  last_command = command_name;

  return;
}

// function that processes the user's input and sends the command to the motors
void process_command(int state, float speed) {
  // Q: FORWARD
  // W: SLIGHT LEFT
  // E: LEFT
  // R: HARD LEFT
  // T: SLIGHT RIGHT
  // Y: RIGHT
  // U: HARD RIGHT
  // A: REVERSE
  // S: REVERSE SLIGHT LEFT
  // D: REVERSE LEFT
  // F: REVERSE HARD LEFT
  // G: REVERSE SLIGHT RIGHT
  // H: REVERSE RIGHT
  // J: REVERSE HARD RIGHT

  // temp variable used to give a slower speed to a motor
  float temp = 0.0;

  // check which input the user gave
  switch (state) {
    case 'q':
    case 'Q':
      drive("FORWARD", 0, speed, 0, speed);
      break;

    case 'w':
    case 'W':
      // change the left motor's speed to account for the turning
      //temp = (speed < 30) ? 15:(speed - 30);
      temp = (speed < left_speed) ? (left_speed / 2):(speed - left_speed);
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Left Motor Speed: ");
      Serial.println(temp);

      drive("SLIGHT LEFT", 0, temp, 0, speed);
      break;

    case 'e':
    case 'E':
      // change the left motor's speed to account for the turning
      //temp = (speed < 60) ? 30:(speed - 60);
      temp = (speed < (left_speed * 2)) ? ((left_speed * 2) / 2):(speed - (left_speed * 2));
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Left Motor Speed: ");
      Serial.println(temp);

      drive("LEFT", 0, temp, 0, speed);
      break;

    case 'r':
    case 'R':
      drive("HARD LEFT", 0, 0, 0, speed);
      break;

    case 't':
    case 'T':
      // change the right motor's speed to account for the turning
      //temp = (speed < 50) ? 25:(speed - 50);
      temp = (speed < right_speed) ? (right_speed / 2):(speed - right_speed);
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Right Motor Speed: ");
      Serial.println(temp);

      drive("SLIGHT RIGHT", 0, speed, 0, temp);
      break;

    case 'y':
    case 'Y':
      // change the right motor's speed to account for the turning
      //temp = (speed < 80) ? 40:(speed - 80);
      temp = (speed < (right_speed * 2)) ? ((right_speed * 2) / 2):(speed - (right_speed * 2));
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Right Motor Speed: ");
      Serial.println(temp);

      drive("RIGHT", 0, speed, 0, temp);
      break;

    case 'u':
    case 'U':
      drive("HARD RIGHT", 0, speed, 0, 0);
      break;

    case 'a':
    case 'A':
      drive("REVERSE", speed, 0, speed, 0);
      break;

    case 's':
    case 'S':
      // change the left motor's speed to account for the turning
      temp = (speed < left_speed) ? (left_speed / 2):(speed - left_speed);
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Left Motor Speed: ");
      Serial.println(temp);

      drive("REVERSE SLIGHT LEFT", temp, 0, speed, 0);
      break;

    case 'd':
    case 'D':
      // change the left motor's speed to account for the turning
      temp = (speed < (left_speed * 2)) ? ((left_speed * 2) / 2):(speed - (left_speed * 2));
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Left Motor Speed: ");
      Serial.println(temp);

      drive("REVERSE LEFT", temp, 0, speed, 0);
      break;

    case 'f':
    case 'F':
      drive("REVERSE HARD LEFT", 0, 0, speed, 0);
      break;

    case 'g':
    case 'G':
      // change the right motor's speed to account for the turning
      temp = (speed < right_speed) ? (right_speed / 2):(speed - right_speed);
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Right Motor Speed: ");
      Serial.println(temp);

      drive("REVERSE SLIGHT RIGHT", speed, 0, temp, 0);
      break;

    case 'h':
    case 'H':
      // change the right motor's speed to account for the turning
      temp = (speed < (right_speed * 2)) ? ((right_speed * 2) / 2):(speed - (right_speed * 2));
      temp = constrain(temp, MINIMUM_SPEED, MAXIMUM_SPEED);
      Serial.print("Right Motor Speed: ");
      Serial.println(temp);

      drive("REVERSE RIGHT", speed, 0, temp, 0);
      break;

    case 'j':
    case 'J':
      drive("REVERSE HARD RIGHT", speed, 0, 0, 0);
      break;

    case 'z':
    case 'Z':
      drive("IDLE/STOP", 0, 0, 0, 0);
      break;

    default:
      break;
  }

  return;
}

void loop() {
  // put your main code here, to run repeatedly:

  // if the speed is less than the MINIMUM_SPEED or goes past the MAXIMUM_SPEED then set it to either MINIMUM_SPEED or MAXIMUM_SPEED (min/max allowed speeds)
  speed = constrain(speed, MINIMUM_SPEED, MAXIMUM_SPEED);

  // don't do anything if there's nothing read from serial input
  if (Serial.available() > 0) {
    // read in the user input
    state = Serial.read();

    // print out the user's input in decimal format
    Serial.print("Received State in Decimal: ");
    Serial.println(state);

    // adjust the speed based on user's input
    if ((state >= '1') && (state <= '6')) {
      speed = adjust_speed(state, speed);
      Serial.print("Adjusted Speed: ");
      Serial.println(speed);
    }
    // send the user's input to the motors
    else if (isAlpha(state)) {
      process_command(state, speed);
    }
    // set the car to idle
    else {
      drive("IDLE/STOP", 0, 0, 0, 0);
    }

    Serial.println();
  }
}