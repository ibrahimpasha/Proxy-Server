import urllib.request
import time
import sys
import base64
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
MEASURE_IP = sys.argv[3]
MEASURE_PORT = int(sys.argv[4])
PROXY_PORT = int(sys.argv[5])
MEASURE_FILE = sys.argv[6]


class myMainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/'):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                url_measure = 'http://' + MEASURE_IP + ':' + str(MEASURE_PORT)
                # print(url_measure)
                req = urllib.request.Request(url_measure)
                with urllib.request.urlopen(req) as response:
                    html = response.read()
                self.wfile.write(html)


            elif self.path.endswith(".html"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                url_server = 'http://' + SERVER_IP + ':' + str(SERVER_PORT) + '/.html'
                req = urllib.request.Request(url_server)
                with urllib.request.urlopen(req) as response:
                    html = response.read()
                self.wfile.write(html)

            elif self.path.endswith('.jpg'):
                # Request to Measure
                list = str(self.path).split('/')
                RESOURCE = list[len(list)-1]
                url_measure = 'http://' + MEASURE_IP + ':' + str(MEASURE_PORT) + '/' + MEASURE_FILE
                before = time.monotonic()
                response, headers = urllib.request.urlretrieve(url_measure)
                after = time.monotonic()
                duration = after - before
                size = int(headers['Content-length']) / 1024
                dt = int(size / duration)

                # Rquest to Server
                url_server = 'http://' + SERVER_IP + ':' + str(SERVER_PORT) + '/' + RESOURCE
                try:
                    req = urllib.request.Request(url_server)
                    req.add_header('datarate', dt)
                    res = urllib.request.urlopen(req)
                    if res.getcode() == 200:
                        print(res.info())
                        self.send_response(200)
                        self.send_header('Content-type', res.info()['Content-type'])
                        self.send_header('Datarate', res.info()['Datarate'])
                        self.send_header('Content-length', res.info()['Content-length'])
                        self.end_headers()
                        with res as f:
                            self.wfile.write(f.read())
                    else:
                        self.send_response(404)
                        self.end_headers()
                        print("Page not found")
                except http.client.HTTPException as e:
                    self.send_response(404)
                    self.end_headers()
                    print("Page not found")

            else:
                self.send_response(404)
                print("Page not found")
        except http.client.HTTPException as e:
            self.send_response(404)
            print("Page not found")

try:
    server = HTTPServer(('', PROXY_PORT), myMainHandler)
    print("Server Started on port: %s" % PROXY_PORT)
    server.serve_forever()
except KeyboardInterrupt:
    print("Interrupted")
    server.socket.close()
