"""Starts the AC controller service"""

from server import WebServer
from controller import Controller
from time import sleep

def main():
    """Runs the application as a service"""
    controller = Controller()
    server = WebServer(port=8181, controller=controller)
    try:
        controller.run()
        server.serve()
        while 1:
            sleep(1)
    except KeyboardInterrupt:
        controller.stop()
        server.shutdown()
        quit()

if __name__ == '__main__':
    main()
