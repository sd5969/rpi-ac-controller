"""Starts the AC controller service"""

from server import WebServer

def main():
    """Runs the application as a service"""
    print "I literally do nothing?"
    server = WebServer(port=80)
    try:
        server.serve()
        while 1:
            pass
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == '__main__':
    main()
