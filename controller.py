"""Services for controlling hardware"""

from threading import Thread
from time import sleep

TEMP_MAX = 80
TEMP_MIN = 60

class Controller(object):
    """Control abstraction"""

    def __init__(self):
        self.thread = None
        self.running = False
        self.temperature = 70
        self.enabled = False

    def run(self):
        """Runs controller in new thread"""
        self.thread = Thread(target=self._run)
        self.thread.start()

    def _run(self):
        """Runs controller"""
        self.running = True
        print "Started hardware controller"
        while self.running:
            sleep(1)

    def stop(self):
        """Stops controller"""
        self.running = False
        print "Stopping hardware controller"
        self.thread.join()

    def set_temperature(self, temperature):
        """Sets temperature for controller"""
        if temperature <= TEMP_MAX and temperature >= TEMP_MIN:
            self.temperature = temperature

    def set_controller_state(self, enabled):
        """Sets controller to enabled/disabled"""
        self.enabled = (True and enabled)

    def get_temperature(self):
        """Gets controller set temperature"""
        return self.temperature

    def get_controller_state(self):
        """Gets controller enabled state"""
        return self.enabled
