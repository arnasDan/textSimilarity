from http.server import HTTPServer, BaseHTTPRequestHandler

from os import curdir

PORT = 3000

class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_OPTIONS(self):
        response = b'GET'         
        self.send_response(200)       
        self.send_header('Allow', 'GET')
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With') 
        self.send_header('Content-Length', len(response))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        print(self.path.lower())
        if self.path == '/' or self.path.lower() == '/index.html':
            self.path = '/Home.html'
        try:
            self.send_response(200)
            self.send_header('Connection', 'close')
            self.end_headers()

            if self.path.endswith(".html"):
                mimetype = 'text/html'
            elif self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
            elif self.path.endswith(".js"):
                mimetype = 'application/javascript'
            elif self.path.endswith(".css"):
                mimetype = 'text/css'
            else:
                return

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', mimetype + '; charset=utf-8')
            with open(curdir + '/pages' + self.path, encoding='utf-8') as file:
                file_bytes = bytes(file.read(), 'utf-8')
            
            self.send_header('Content-Length', len(file_bytes))
            self.end_headers()
            self.wfile.write(file_bytes)
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

server_address = ('', PORT)
httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
print ("Starting server on port %d" % PORT)
#TODO: handle interrupts, etc
httpd.serve_forever()
