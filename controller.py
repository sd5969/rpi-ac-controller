"""Services for controlling hardware"""

from threading import Thread
from time import sleep
from datetime import datetime

TEMP_MAX = 80 # Fahrenheit
TEMP_MIN = 60 # Fahrenheit
THRESHOLD = 2 # Fahrenheit
MIN_TIME = 180 # seconds

class Controller(object):
    """Control abstraction"""

    def __init__(self):
        self.thread = None                                  # for running in multithread
        self.running = False                                # continues control loop if true
        self.controls = {}                                  # variables to control the system
        self.measurements = {}                              # variables for system input

        self.measurements['actual_temperature'] = 65        # outside temperature
        self.measurements['button_state'] = False           # push button (not momentary) state

        self.controls['temperature'] = 70                   # target temperature
        self.controls['enabled'] = False                    # controller enabled?
        self.controls['override'] = False                   # controller overridden?
        self.controls['ac_on'] = False                      # AC on?
        self.controls['last_state_change'] = datetime.now() # last time state was changed
        self.controls['led_1'] = False                      # indicates if AC is turned on
        self.controls['led_2'] = False                      # indicates state of controller enabled
        self.controls['led_2_blink'] = False                # indicates state of override
        self.controls['servo_angle'] = -15                  # servo angle, default off

    def run(self):
        """Runs controller in new thread"""
        self.thread = Thread(target=self._run)
        self.thread.start()

    def _run(self):
        """Runs controller"""
        self.running = True
        print "Started hardware controller"
        self.controls['last_state_change'] = datetime.now()
        while self.running:
            if self.controls['override']:
                self.enable_ac(True)
            elif self.controls['enabled'] and \
              (datetime.now() - self.controls['last_state_change']).seconds > MIN_TIME:
                outside_temp = self.read_temperature()
                if outside_temp < (self.controls['temperature'] - THRESHOLD):
                    self.enable_ac(False)
                if outside_temp > (self.controls['temperature'] + THRESHOLD):
                    self.enable_ac(True)
            elif not self.controls['enabled'] and \
              (datetime.now() - self.controls['last_state_change']).seconds > MIN_TIME:
                self.enable_ac(False)

            self.set_button_state()
            self.controls['override'] = (True and self.measurements['button_state'])

            self.set_led_1()
            self.set_led_2()

            # if AC is on solid LED 1
            # if override blink LED 2
            # if enabled solid LED 2

            sleep(0.1)

    def stop(self):
        """Stops controller"""
        self.running = False
        print "Stopping hardware controller"
        self.thread.join()

    def set_temperature(self, temperature):
        """Sets temperature for controller"""
        if temperature <= TEMP_MAX and temperature >= TEMP_MIN:
            self.controls['temperature'] = temperature

    def set_controller_state(self, enabled):
        """Sets controller to enabled/disabled"""
        self.controls['enabled'] = (True and enabled)

    def get_temperature(self):
        """Gets controller set temperature"""
        return self.controls['temperature']

    def get_controller_state(self):
        """Gets controller enabled state"""
        return self.controls['enabled']

    def set_override(self, state):
        """Sets controller to override state"""
        self.controls['override'] = (True and state)

    def get_override(self):
        """Gets override AC always-on state"""
        return self.controls['override']

    def enable_ac(self, enabled):
        """Enables and disables AC"""
        if self.controls['ac_on'] != enabled:
            self.controls['last_state_change'] = datetime.now()
        self.controls['ac_on'] = (True and enabled)
        self.set_servo(self.controls['ac_on'])

    def read_temperature(self):
        """Reads outside temp and returns as Fahrenheit"""
        # read temp here
        return self.measurements['actual_temperature']

    def set_servo(self, servo_on):
        """Sets servo to turn AC either on or off"""
        if servo_on:
            self.controls['servo_angle'] = -15
        else:
            self.controls['servo_angle'] = 15
        # set servo here

    def set_button_state(self):
        """Uses status of button and web server to determine button state"""
        # read button here
        self.measurements['button_state'] = True
        self.set_controller_state(self.measurements['button_state'])

    def set_led_1(self):
        """Sets LED 1 based on instance vars (ac_on)"""
        self.controls['led_1'] = self.controls['ac_on']
        if self.controls['led_1']:
            # set LED 1 on
            pass
        else:
            # set LED 1 off
            pass

    def set_led_2(self):
        """Sets LED 2 based on instance vars (enabled, override)"""
        self.controls['led_2'] = self.controls['enabled']
        self.controls['led_2_blink'] = self.controls['override']
        if self.controls['led_2_blink']:
            # set LED 2 to blink
            pass
        elif self.controls['led_2']:
            # set LED 2 on
            pass
        else:
            # set LED 2 off
            pass
