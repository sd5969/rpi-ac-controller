"""Services for controlling web API"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import json

MAX_TEMP = 80
MIN_TEMP = 60

class _apiHandler(BaseHTTPRequestHandler):
    """Class for handling API requests"""

    def __init__(self, *args, **kwargs):
        self.temperature = 70
        self.controller_enabled = False
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

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
            response = {
                'temperature': self.temperature
            }
            self.wfile.write(json.dumps(response))

        def get_controller(self):
            """API endpoint to get temp sensor value"""
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                'enabled': self.controller_enabled
            }
            self.wfile.write(json.dumps(response))

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

        def post_temp(self, body):
            """Save new temperature setting"""
            self.send_response(201)
            self.send_header("Content-length", "0")
            self.end_headers()
            if 'temperature' in body:
                try:
                    new_temp = int(body.temperature)
                except ValueError:
                    pass
            if new_temp <= MAX_TEMP and new_temp >= MIN_TEMP:
                self.temperature = new_temp

        def post_controller(self, body):
            """Enable or disable controller"""
            self.send_response(201)
            self.send_header("Content-length", "0")
            self.end_headers()
            if 'enabled' in body:
                try:
                    self.controller_enabled = (body.enabled == "True")
                except ValueError:
                    pass

        def post_default(self, _):
            """Default return"""
            self.send_response(404)
            self.send_header("Content-length", "0")
            self.end_headers()

        content_length = int(self.headers.getheader('content-length'))
        if content_length > 0:
            post_body = self.rfile.read(content_length)
            parsed_body = json.loads(post_body)
            print parsed_body
        else:
            parsed_body = {}

        options = {
            '/api/temperature': post_temp,
            '/api/controller': post_controller
        }
        options.get(self.path, post_default)(self, parsed_body)

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
