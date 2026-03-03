# === LIBRARIES ===
import asyncio
import threading
import time
from bleak import BleakScanner, BleakClient
# =================

class BLE:
    def __init__(self):
        self.ESP32_name = "ESP32-S3"
        self.RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

        self.current_command = b'Z'
        
        self.bleak_client = None

        # run a background thread for the bluetooth connection
        # if we put the BLE code inside the while(camera.isOpened()) loop, the camera will freeze everytime it tries to send a bluetooth message
        self.async_loop = asyncio.new_event_loop()
        threading.Thread(target=self._start_async_loop, daemon=True).start()
        return
    
    # used to run an infinite bluetooth connection loop in the background thread
    def _start_async_loop(self):
        asyncio.set_event_loop(self.async_loop)
        self.async_loop.run_until_complete(self._connect_and_run())
        return
    
    # establishes bluetooth connection and runs infinite command sending loop
    async def _connect_and_run(self):
        print(f"[BLE] -- Scanning for the {self.ESP32_name} device nearby...\n")

        # find the ESP32 from the bluetooth scan
        devices = await BleakScanner.discover()
        esp_device = None
        for device in devices:
            if (device.name == self.ESP32_name):
                esp_device = device
                break
        
        # break out of the loop if the ESP32 wasn't found
        if (esp_device == None):
            print(f"[BLE Error] -- Did not find the {self.ESP32_name} device to be nearby. Turn on the device and try again...\n")
            return
        
        print(f"[BLE] -- Found the {self.ESP32_name} device. Establishing connection...\n")

        try:
            # establishes the bluetooth connection
            async with BleakClient(esp_device) as client:
                self.bleak_client = client
                print(f"[BLE] -- Successfully connected to the {self.ESP32_name} device...\n")

                last_command_sent = None
                last_command_sent_time = time.time()
                time_interval = 0.3

                # keeps the connection alive while watching for new commands
                while (self.bleak_client.is_connected):
                    elapsed_time = time.time() - last_command_sent_time

                    # if the command is new or if the interval was reached then send the command
                    if ((self.current_command != last_command_sent) or (elapsed_time > time_interval)):
                        try:
                            # send the command to the ESP32
                            await self.bleak_client.write_gatt_char(self.RX_UUID, self.current_command)

                            last_command_sent = self.current_command
                            last_command_sent_time = time.time()

                        except Exception as e:
                            print(f"[BLE Error] -- Connection to the {self.ESP32_name} device was lost or failed...\n")

                    # prevents maxing out the CPU thread
                    await asyncio.sleep(0.05)

        except Exception as e:
            print(f"[BLE Error] -- Connection to the {self.ESP32_name} device was lost or failed: {e}...\n")

        return
    
    # update the car's direction
    def send_command(self, command):
        self.current_command = command
        return