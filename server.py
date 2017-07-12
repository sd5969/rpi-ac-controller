"""Services for controlling web API"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

class _apiHandler(BaseHTTPRequestHandler):
    """Class for handling API requests"""

    def do_GET(self):
        """Handles GET requests"""
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write("Hello GET World!")

    def do_HEAD(self):
        """Handles HEAD requests"""
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

    def do_POST(self):
        """Handles POST requests"""
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write("Hello POST World!")

class WebServer(object):
    """Web server abstraction"""

    def __init__(self, port=80):
        """Constructor to store params"""
        self.port = port
        self.running = False
        self.server = None
        self.thread = None

    def _serve(self):
        """Serves web server"""
        self.server = HTTPServer(('', self.port), _apiHandler)
        print "Started HTTP server on port", self.port
        self.running = True
        while self.running:
            try:
                self.server.handle_request()
            except Exception as ex:
                if type(ex).__name__ != "error" or \
                   ex.args[0] != 9:
                    raise ex

    def serve(self):
        """Serves web server in new thread"""
        self.thread = Thread(target=self._serve)
        self.thread.start()

    def shutdown(self):
        """Shuts down web server"""
        self.running = False
        print "Shutting down web server"
        self.server.server_close()
        self.thread.join()
