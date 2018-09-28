#!/usr/bin/python

# This code is based on the sample code provided here: https://www.acmesystems.it/python_http
# You can create a random file with size of 5 MB in Linux or OS X using the following command:
# dd if=/dev/urandom of=file.bin bs=1024 count=5120

from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import time
import sys
import os

HTTP_PORT_DEFAULT = 8080
MIN_DELAY = 1
MAX_DELAY = 5


# This class handles any incoming request from the browser
class MeasurementServerRequestHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        global MIN_DELAY, MAX_DELAY

        if self.path == "/":

            # Send response code and headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Send the html message
            contents = ''
            for item in os.listdir("."):
                contents += '<li>' + item + '</li>'
            body = '<html><head><title>Index of /</title></head><body><h1>Index of /</h1><ul>%s</ul></body></html>' % contents
            self.wfile.write(body.encode('utf-8'))
        elif os.path.isfile('./' + self.path):
            # Wait for random time
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            time.sleep(delay)

            # Send response code and headers
            self.send_response(200)
            self.send_header('Content-type', 'application/x-binary')
            self.send_header('Content-length', str(os.stat('./' + self.path).st_size))
            self.end_headers()

            # Send the binary file
            with open('./' + self.path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Send 404 (Not Found) status code for any other requests
            self.send_response(404)
        return


try:
    if len(sys.argv) == 2:
        http_port = int(sys.argv[1])
    else:
        http_port = HTTP_PORT_DEFAULT
    # Create HTTP server with customized class
    server = HTTPServer(('', http_port), MeasurementServerRequestHandler)
    print('Started httpserver on port', http_port)

    # Wait forever for incoming HTTP requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()