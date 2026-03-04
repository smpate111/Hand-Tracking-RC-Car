// === LIBRARIES ===
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
// =================

// === UNIQUE IDs ===
#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
// ==================

// class that controls the ultrasonic distance sensor
class ultrasonic_sensor {
  private:
    int trig_pin, echo_pin;
    float distance;
    volatile unsigned long start_time = 0;
    volatile unsigned long travel_time = 0;
    static ultrasonic_sensor* instance;

    // interrupt service routine that runs in the background ram
    static void ARDUINO_ISR_ATTR echo_isr() {
      if (digitalRead(instance->echo_pin) == HIGH) {
        instance->start_time = micros();
      }
      else {
        instance->travel_time = micros() - instance->start_time;
      }
      return;
    }

  public:
    ultrasonic_sensor(int trig, int echo) : trig_pin(trig), echo_pin(echo) {
      instance = this;
    }

    void init() {
      pinMode(trig_pin, OUTPUT);
      pinMode(echo_pin, INPUT);
      attachInterrupt(digitalPinToInterrupt(echo_pin), echo_isr, CHANGE);
      return;
    }

    void trigger_sensor() {
      digitalWrite(trig_pin, LOW);
      delayMicroseconds(2);

      digitalWrite(trig_pin, HIGH);
      delayMicroseconds(10);

      digitalWrite(trig_pin, LOW);
      return;
    }

    float calculate_distance() {
      if (travel_time == 0) {
        return 400.0;
      }

      float distance = (travel_time * 0.034) / 2.0;
      
      if ((distance <= 0) || (distance > 400.0)) {
        return 400.0;
      }

      return distance;
    }
};

// class that controls the speed and direction of the motors
class drive_controller {
  // === PRIVATE VARIABLES ===
  private:
    int in1, in2, in3, in4;
    float current_speed;
    const float MINIMUM_SPEED = 100.0;
    const float MAXIMUM_SPEED = 255.0;
    String last_command = "IDLE";
  // =========================

  public:
    drive_controller(int pin1, int pin2, int pin3, int pin4) : in1(pin1), in2(pin2), in3(pin3), in4(pin4) {}

    // initializes the pins and car's speed
    void init() {
      pinMode(in1, OUTPUT);
      pinMode(in2, OUTPUT);
      pinMode(in3, OUTPUT);
      pinMode(in4, OUTPUT);
      current_speed = 255.0;
      return;
    }

    // updates the current speed and ensures it's within the defined range
    void adjust_speed(float speed) {
      current_speed = constrain(speed, MINIMUM_SPEED, MAXIMUM_SPEED);
      return;
    }

    // display the speed to the user
    /*void display_speed(float speed) {
      if (pCharacteristic != NULL) {
        String feedback = "New Speed: " + speed;
        pCharacteristic->setValue(feedback.c_str());
        pCharacteristic->notify();
      }

      return;
    }*/

    // controls the motors by speed and direction
    void drive(String str_command, int speed1, int speed2, int speed3, int speed4) {
      analogWrite(in1, speed1);
      analogWrite(in2, speed2);
      analogWrite(in3, speed3);
      analogWrite(in4, speed4);

      last_command = str_command;
      return;
    }

    // stops the motors
    void stop() {
      //display_command("IDLE", 0, 0, 0, 0);
      drive("IDLE", 0, 0, 0, 0);
      return;
    }

    // displays the command to the user
    /*void display_command(String command, int speed1, int speed2, int speed3, int speed4) {
      if ((pCharacteristic != NULL) && (command != last_command)) {
        String feedback = "Command: " + command + " -- In1: " + speed1 + " -- In2: " + speed2 + " -- In3: " + speed3 + " -- In4: " + speed4;
        pCharacteristic->setValue(feedback.c_str());
        pCharacteristic->notify();
      }

      return;
    }*/

    // specifies what to send to the drive function based on given command
    void execute_command(char command) {
      // speed adjustment
      if ((command >= '0') && (command <= '9')) {
        int index = 9;
        
        if (command != '0') {
          index = command - '1';
        }

        // current speed = minimum speed + (speed index * 31)
        //current_speed = MINIMUM_SPEED + ((command - '1') * 31.0);
        current_speed = MINIMUM_SPEED + (index * 17.22);
        //display_speed(current_speed);
        return;
      }

      // movement adjustment
      switch (command) {
        // === FORWARD MOVEMENTS ===
        // FORWARD
        case 'q':
        case 'Q':
          //display_command("FORWARD", 0, current_speed, 0, current_speed);
          drive("FORWARD", 0, current_speed, 0, current_speed);
          break;

        // SLIGHT LEFT
        case 'w':
        case 'W':
          //display_command("SLIGHT LEFT", 0, current_speed * 0.75, 0, current_speed);
          drive("SLIGHT LEFT", 0, current_speed * 0.75, 0, current_speed);
          break;

        // LEFT
        case 'e':
        case 'E':
          //display_command("LEFT", 0, current_speed * 0.50, 0, current_speed);
          drive("LEFT", 0, current_speed * 0.50, 0, current_speed);
          break;

        // HARD LEFT
        case 'r':
        case 'R':
          //display_command("HARD LEFT", 0, 0, 0, current_speed);
          drive("HARD LEFT", 0, 0, 0, current_speed);
          break;

        // SLIGHT RIGHT
        case 't':
        case 'T':
          //display_command("SLIGHT RIGHT", 0, current_speed, 0, current_speed * 0.75);
          drive("SLIGHT RIGHT", 0, current_speed, 0, current_speed * 0.75);
          break;

        // RIGHT
        case 'y':
        case 'Y':
          //display_command("RIGHT", 0, current_speed, 0, current_speed * 0.50);
          drive("RIGHT", 0, current_speed, 0, current_speed * 0.50);
          break;

        // HARD RIGHT
        case 'u':
        case 'U':
          //display_command("HARD RIGHT", 0, current_speed, 0, 0);
          drive("HARD RIGHT", 0, current_speed, 0, 0);
          break;
        // =========================

        // === REVERSE MOVEMENTS ===
        // REVERSE
        case 'a':
        case 'A':
          //display_command("REVERSE", current_speed, 0, current_speed, 0);
          drive("REVERSE", current_speed, 0, current_speed, 0);
          break;

        // REVERSE SLIGHT LEFT
        case 's':
        case 'S':
          //display_command("REVERSE SLIGHT LEFT", current_speed * 0.75, 0, current_speed, 0);
          drive("REVERSE SLIGHT LEFT", current_speed * 0.75, 0, current_speed, 0);
          break;

        // REVERSE LEFT
        case 'd':
        case 'D':
          //display_command("REVERSE LEFT", current_speed * 0.50, 0, current_speed, 0);
          drive("REVERSE LEFT", current_speed * 0.50, 0, current_speed, 0);
          break;

        // REVERSE HARD LEFT
        case 'f':
        case 'F':
          //display_command("REVERSE HARD LEFT", 0, 0, current_speed, 0);
          drive("REVERSE HARD LEFT", 0, 0, current_speed, 0);
          break;

        // REVERSE SLIGHT RIGHT
        case 'g':
        case 'G':
          //display_command("REVERSE SLIGHT RIGHT", current_speed, 0, current_speed * 0.75, 0);
          drive("REVERSE SLIGHT RIGHT", current_speed, 0, current_speed * 0.75, 0);
          break;

        // REVERSE RIGHT
        case 'h':
        case 'H':
          //display_command("REVERSE RIGHT", current_speed, 0, current_speed * 0.50, 0);
          drive("REVERSE RIGHT", current_speed, 0, current_speed * 0.50, 0);
          break;

        // REVERSE HARD RIGHT
        case 'j':
        case 'J':
          //display_command("REVERSE HARD RIGHT", current_speed, 0, 0, 0);
          drive("REVERSE HARD RIGHT", current_speed, 0, 0, 0);
          break;
        // =========================

        // === IDLE ===
        case 'z':
        case 'Z':
          //stop();
          drive("IDLE", 0, 0, 0, 0);
          break;
        // ============
      }
    }
};

// class that handles the bluetooth controller
class ble_controller : public BLECharacteristicCallbacks, public BLEServerCallbacks{
  public:
    char current_command = 'Z';
    unsigned long last_command_time = 0;
    bool device_connected = false;
    String incoming_buffer = "";

    void setup() {
      BLEDevice::init("ESP32-S3");

      BLEServer *bluetooth_server = BLEDevice::createServer();
      bluetooth_server->setCallbacks(this);   // handles connecting/disconnecting

      BLEService *bluetooth_service = bluetooth_server->createService(SERVICE_UUID);

      BLECharacteristic *bluetooth_characteristic_rx = bluetooth_service->createCharacteristic(CHARACTERISTIC_UUID_RX, BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_WRITE_NR);
      bluetooth_characteristic_rx->setCallbacks(this);

      BLECharacteristic *bluetooth_characteristic_tx = bluetooth_service->createCharacteristic(CHARACTERISTIC_UUID_TX, BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_READ);
      bluetooth_characteristic_tx->addDescriptor(new BLE2902());

      bluetooth_service->start();
      bluetooth_server->getAdvertising()->start();
      return;
    }

    void onWrite(BLECharacteristic *ble_character) override {
      String value = ble_character->getValue();

      if (value.length() > 0) {
        //current_command = value[0];
        incoming_buffer = incoming_buffer + value;
        last_command_time = millis();
      }

      return;
    }

    void onConnect(BLEServer *ble_server) override {
      device_connected = true;

      ble_server->updateConnParams(ble_server->getConnId(), 0x06, 0x12, 0, 100);
      return;
    }

    void onDisconnect(BLEServer *ble_server) override {
      device_connected = false;
      ble_server->getAdvertising()->start();
      return;
    }
};

// === GLOBAL INSTANCES ===
ultrasonic_sensor* ultrasonic_sensor::instance = nullptr;
drive_controller car(4, 5, 16, 17);
ble_controller ble;
ultrasonic_sensor front_sensor(9, 10);
char last_processed_command = 'Z';
unsigned long last_ping_time = 0;
const unsigned long PING_INTERVAL = 60;
// ========================

bool is_car_moving_forward(char command) {
  bool forward_flag = false;
  switch (command) {
    // === FORWARD MOVEMENTS ===
    // FORWARD
    case 'q':
    case 'Q':
    // SLIGHT LEFT
    case 'w':
    case 'W':
    // LEFT
    case 'e':
    case 'E':
    // HARD LEFT
    case 'r':
    case 'R':
    // SLIGHT RIGHT
    case 't':
    case 'T':
    // RIGHT
    case 'y':
    case 'Y':
    // HARD RIGHT
    case 'u':
    case 'U':
      forward_flag = true;
      break;
    // =========================
  }
  return forward_flag;
}

bool is_car_moving_backward(char command) {
  bool backward_flag = false;
  
  switch (command) {
    // === REVERSE MOVEMENTS ===
    // REVERSE
    case 'a':
    case 'A':
    // REVERSE SLIGHT LEFT
    case 's':
    case 'S':
    // REVERSE LEFT
    case 'd':
    case 'D':
    // REVERSE HARD LEFT
    case 'f':
    case 'F':
    // REVERSE SLIGHT RIGHT
    case 'g':
    case 'G':
    // REVERSE RIGHT
    case 'h':
    case 'H':
    // REVERSE HARD RIGHT
    case 'j':
    case 'J':
      backward_flag = true;
      break;
    // =========================
  }

  return backward_flag;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
  // whenever the usb cable is disconnected from the ESP32
  #if ARDUINO_USB_CDC_ON_BOOT
  Serial.setTxTimeoutMs(0); 
  #endif

  car.init();
  ble.setup();
  front_sensor.init();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (ble.incoming_buffer.length() > 0) {
    ble.current_command = ble.incoming_buffer[0];
    ble.incoming_buffer.remove(0, 1);
    ble.last_command_time = millis();
  }

  char current_cmd = ble.current_command;
  bool forward_flag = is_car_moving_forward(current_cmd);
  bool backward_flag = is_car_moving_backward(current_cmd);

  if (forward_flag == true) {
    if (millis() - last_ping_time >= PING_INTERVAL) {
      front_sensor.trigger_sensor();
      last_ping_time = millis();
    }

    float front_distance = front_sensor.calculate_distance();

    if (front_distance < 20.0) {
      current_cmd = 'Z';
      ble.current_command = 'Z';

      if (ble.incoming_buffer.length() > 0) {
        ble.incoming_buffer = "";
      }
    }
  }

  bool currently_moving_forward = is_car_moving_forward(last_processed_command);
  bool currently_moving_backward = is_car_moving_backward(last_processed_command);

  if ((currently_moving_forward == true) && (backward_flag == true)) {
    car.execute_command('Z');
    delay(50);
  }
  else if ((currently_moving_backward == true) && (forward_flag == true)) {
    car.execute_command('Z');
    delay(50);
  }
  
  // if no new command has been sent within a defined timeframe, then stop the car
  if ((millis() - ble.last_command_time > 500) && (ble.incoming_buffer.length() == 0)) {
    ble.current_command = 'Z';
    current_cmd = 'Z';
  }

  // execute the command if it is not the same as the previous command
  if (current_cmd != last_processed_command) {
    car.execute_command(current_cmd);
    last_processed_command = ble.current_command;
  }
}