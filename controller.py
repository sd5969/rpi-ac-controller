"""Services for controlling hardware"""

from threading import Thread

class Controller(object):
    """Control abstraction"""

    def __init__(self):
        self.thread = None
        self.running = False

    def run(self):
        """Runs controller in new thread"""
        self.thread = Thread(target=self._run)
        self.thread.start()

    def _run(self):
        """Runs controller"""
        self.running = True
        print "Started hardware controller"
        while self.running:
            pass

    def stop(self):
        """Stops controller"""
        self.running = False
        print "Stopping hardware controller"
        self.thread.join()
