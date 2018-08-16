"""Services for controlling web API"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import json

MAX_TEMP = 80
MIN_TEMP = 60

def _api_handler_factory(controller):
    """Factory for building RequestHandler with Controller"""
    class _apiHandler(BaseHTTPRequestHandler):
        """Class for handling API requests"""

        def __init__(self, *args, **kwargs):
            self.controller = controller
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

            def power_enabled(self):
                """API endpoint to get power cooldown disabling value"""
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {
                    'enabled': True
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
                '/api/power-enabled': power_enabled
            }
            options.get(self.path, get_default)(self)

        def do_HEAD(self):
            """Handles HEAD requests"""
            self.send_response(200)
            self.send_header("Content-length", "0")
            self.end_headers()

        def do_POST(self):
            """Handles POST requests"""

            def power_switch(self, body):
                """Press power button"""
                self.send_response(201)
                self.send_header("Content-length", "0")
                self.end_headers()
                os.system("irsend SEND_ONCE airconditioner BTN_X")

            def increase_temperature(self, body):
                """Increase temperature"""
                self.send_response(201)
                self.send_header("Content-length", "0")
                self.end_headers()
                os.system("irsend SEND_ONCE airconditioner BTN_Y")

            def decrease_temperature(self, body):
                """Decrease temperature"""
                self.send_response(201)
                self.send_header("Content-length", "0")
                self.end_headers()
                os.system("irsend SEND_ONCE airconditioner BTN_Z")

            def post_default(self, _):
                """Default return"""
                self.send_response(404)
                self.send_header("Content-length", "0")
                self.end_headers()

            content_length = int(self.headers.getheader('content-length'))
            if content_length > 0:
                post_body = self.rfile.read(content_length)
                parsed_body = json.loads(post_body)
                # print parsed_body
            else:
                parsed_body = {}

            options = {
                '/api/power-switch': power_switch,
                '/api/increase-temperature': increase_temperature,
                '/api/decrease-temperature': decrease_temperature
            }
            options.get(self.path, post_default)(self, parsed_body)

            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write("{ \"message\": \"Hello POST World!\"")
    return _apiHandler










class WebServer(object):
    """Web server abstraction"""

    def __init__(self, port=80, controller=None):
        self.port = port
        self.running = False
        self.server = None
        self.thread = None
        self.controller = controller

    def _serve(self):
        """Serves web server"""
        self.server = HTTPServer(('', self.port), \
                                 _api_handler_factory(self.controller))
        print("Started HTTP server on port", self.port)
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
        self.thread.daemon = True
        self.thread.start()

    def shutdown(self):
        """Shuts down web server"""
        self.running = False
        print("Shutting down web server")
        self.server.server_close()
        # self.thread.join()
