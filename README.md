## Proxy and Web Servers
A proxy server that works with a web server to deliver the content customized based on the data rate to the HTTP client.

### Description:
The proxy server "proxy.py" works as a HTTP client and gets request form browser. It then sends a request to download a file from measure server "measure.py" to calculate datarate. One proxy server calculates the data rate, it sends a request with datarate to HTTP server "server.py". HTTP server then sends the required version of the data(image) back to proxy server which is then redirected to browser.

### Implementation:
Proxy server and web serever are implemented in such a way that they work on any host.
1. First browser sends GET request to Proxy.py. 
2. Proxy.py analyses the request and sends a GET request using "urllib' library to measure.py to download a binary file.
3. measure.py receives the request and sends a binary file required adding file size('Content-length') in HTTP Header. 
4. proxy.py then calculates the time it took to download the file and divides the file size with time it took to download the file to get datarate.
5. proxy.py sends the browser url request and datarate in HTTP header to server.py.
6. server.py then decides if the request is .html or .jpg.
7. If the request is a html file it sends "Hi Buddy" in body to proxy server
8. If the request is .jpg file, it looks for the file in file system and if it finds it then it sends the appropriate version of image based on the datarate range provide in server.py
9. If the datarate from the header is below datarate_low it sends smaller version of image, if it is between datarate_low and datarate_high it sends medium version of the image, if it is greater than datarate_high, it sends larger image.
10. proxy.py then sends the response to browser.

### Libraries used:
1. urllib.request
2. http.server

### Limitations:
1. if measure.py cannot find the sample binary file to send, proxy.py doesn't have any default datarate to set.
2. server.py cannot send the content without receiving datarate from the proxy.

### Interesting Observations:
1. Two servers cannot run on single port.
2. If Mimetype is not mentioned in response, image will not be displayed on browser.
3. if you do not end the header, it will not send to browser.
4. Divide datarate by 1024 to get in KBytes ps.

## Author:
### Ibrahim Mohammad
### imohammad@uh.edu
### +1(713)-366-2544