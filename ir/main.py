"""Starts the AC controller service"""

from time import sleep
from server import WebServer

def main():
    """Runs the application as a service"""
    server = WebServer(port=8181)
    try:
        server.serve()
        while 1:
            sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        quit()

if __name__ == '__main__':
    main()
