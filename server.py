"""Services for controlling web API"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

class _apiHandler(BaseHTTPRequestHandler):
    """Class for handling API requests"""

    def do_GET(self):
        """Handles GET requests"""

        def get_file(self):
            """Serves root file"""
            if self.path == '/':
                self.path = '/index.html'
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return_file = None
            with file('web/public/' + self.path[1:]) as out_file:
                return_file = out_file.read()
            self.wfile.write(return_file)

        def get_temp(self):
            """API endpoint to get temp sensor value"""
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write('{ "temperature": 70 }')

        def get_controller(self):
            """API endpoint to get temp sensor value"""
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write('{ "enabled": false }')

        def get_default(self):
            """Default return"""
            self.send_response(404)
            self.send_header("Content-length", "0")
            self.end_headers()

        options = {
            '/': get_file,
            '/lib/angular/angular.min.js': get_file,
            '/api/temperature': get_temp,
            '/api/controller': get_controller
        }
        options.get(self.path, get_default)(self)

    def do_HEAD(self):
        """Handles HEAD requests"""
        self.send_response(200)
        self.send_header("Content-length", "0")
        self.end_headers()

    def do_POST(self):
        """Handles POST requests"""

        def post_temp(self):
            """Save new temperature setting"""
            self.send_response(201)
            self.send_header("Content-length", "0")
            self.end_headers()

        def post_controller(self):
            """Enable or disable controller"""
            self.send_response(201)
            self.send_header("Content-length", "0")
            self.end_headers()

        def post_default(self):
            """Default return"""
            self.send_response(404)
            self.send_header("Content-length", "0")
            self.end_headers()

        options = {
            '/api/temperature': post_temp,
            '/api/controller': post_controller
        }
        options.get(self.path, post_default)(self)

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write("{ \"message\": \"Hello POST World!\"")

class WebServer(object):
    """Web server abstraction"""

    def __init__(self, port=80):
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
