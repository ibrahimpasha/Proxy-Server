from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import time
import sys
import os
import base64
HTTP_PORT = int(sys.argv[1])
datarate_low = int(sys.argv[2])
datarate_high = int(sys.argv[3])


# This class handles any incoming request from the browser
class HTTPServerRequestHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        if self.path.endswith('.html'):
            # print(self.headers)
            # Send response code and headers
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            # Send the html message
            body = '<html><head><title>Title/</title></head><body><h1>Hi buddy</h1></body></html>'
            self.wfile.write(body.encode('utf-8'))
        elif os.path.isfile('./' + self.path):
            s = str(self.path).split('.')
            RES = s[0]
            # print(self.headers)
            datarate = int(self.headers['datarate'])
            if datarate <= datarate_low:
                self.path = RES + '_small.jpg'
            elif datarate >datarate_low and datarate <datarate_high:
                self.path = RES + '_medium.jpg'
            else:
                self.path = RES + '_large.jpg'

            #Send response code and headers
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.send_header('Datarate', str(datarate)+' KBytes ps')
            self.send_header('Content-length', os.stat('./' + self.path).st_size)
            self.end_headers()

            # Send the binary file
            with open('./' + self.path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Send 404 (Not Found) status code for any other requests
            self.send_response(404)
        return


try:
    # Create HTTP server with customized class
    server = HTTPServer(('', HTTP_PORT), HTTPServerRequestHandler)
    print('Started httpserver on port', HTTP_PORT)

    # Wait forever for incoming HTTP requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()