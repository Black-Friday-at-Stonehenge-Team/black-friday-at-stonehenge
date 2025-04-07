import pygame
import serial
import numpy as np

import struct
import threading
import time
from collections import deque

from core.logs import get_logger

logger = get_logger("SoundController")


class SoundController:
    # Singleton tracked instance
    _instance = None

    @classmethod
    def get_instance(cls, config=None, jump_callback=None):
        """Singleton pattern to ensure only one controller exists"""
        if cls._instance is None and config is not None:
            cls._instance = cls(config, jump_callback)
        return cls._instance

    def __init__(self, config, jump_callback):
        # Ensure a singleton instance
        if SoundController._instance is not None:
            logger.warning(
                "A SoundController instance already exists! Stopping existing instance."
            )
            SoundController._instance.stop()
            # Wait for the thread to close properly
            if (
                hasattr(SoundController._instance, "serial_thread")
                and SoundController._instance.serial_thread.is_alive()
            ):
                SoundController._instance.serial_thread.join(timeout=1.0)

        self.window = deque(maxlen=config["window_size"])
        self.base_z_threshold = config["z_threshold"]
        self.holdoff = config["holdoff_time"]
        self.sensitivity = config["sensitivity"]
        self.noise_floor = config.get("noise_floor", 100)
        self.last_trigger = 0
        self.dynamic_threshold = config["z_threshold"]
        self.jump_callback = jump_callback
        self.running = True
        self.port = config["port"]
        self.baudrate = config["baudrate"]

        # Set this as the instance
        SoundController._instance = self

        # Start serial monitoring in a separate thread
        self.serial_thread = threading.Thread(
            target=self._monitor_serial, args=(self.port, self.baudrate)
        )
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def update(self, value):
        self.window.append(value)

        if len(self.window) < self.window.maxlen // 2:
            return False

        current_mean = np.mean(self.window)
        current_std = np.std(self.window)

        # Adaptive sensitivity
        self.dynamic_threshold = self.base_z_threshold * (
            1 + (self.sensitivity - 0.5) * 2
        )

        # Dynamic noise floor adjustment
        if current_std < 1 or value < self.noise_floor:
            return False

        z_score = abs((value - current_mean) / current_std)

        if (
            z_score > self.dynamic_threshold
            and (time.time() - self.last_trigger) > self.holdoff
        ):
            self.last_trigger = time.time()
            return True
        return False

    def stop(self):
        logger.info("Stopping sound controller...")
        self.running = False

        if hasattr(self, "serial_thread") and self.serial_thread.is_alive():
            self.serial_thread.join(timeout=1.0)
            logger.info("Sound controller thread stopped")

        # Reset the Singleton instance
        if SoundController._instance == self:
            SoundController._instance = None

    def _monitor_serial(self, port, baudrate):
        serial_obj = None
        try:
            # Open the serial port
            serial_obj = serial.Serial(port, baudrate)
            logger.info(f"Monitoring sound sensor on {port}...")

            while self.running:
                try:
                    data = serial_obj.read(2)
                    value = struct.unpack("<H", data)[0]

                    if self.update(value):
                        logger.info("Sound trigger detected! Jumping...")
                        # Add new SOUND_TRIGGER event to the pygame event queue
                        pygame.event.post(
                            pygame.event.Event(
                                pygame.USEREVENT, {"action": "SOUND_TRIGGER"}
                            )
                        )
                except Exception as e:
                    if self.running:
                        logger.error(f"Error reading from serial: {str(e)}")
                        time.sleep(1)

        except Exception as e:
            logger.error(f"Serial monitoring error: {str(e)}")

        finally:
            # Close serial port
            if serial_obj and serial_obj.is_open:
                serial_obj.close()
                logger.info(f"Closed serial port {port}")
