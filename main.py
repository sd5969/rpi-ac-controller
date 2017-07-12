"""Starts the AC controller service"""

from server import WebServer
from controller import Controller

def main():
    """Runs the application as a service"""
    server = WebServer()
    controller = Controller()
    try:
        server.serve()
        controller.run()
        while 1:
            pass
    except KeyboardInterrupt:
        server.shutdown()
        controller.stop()

if __name__ == '__main__':
    main()
