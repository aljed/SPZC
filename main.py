import socketserver
import http.server
import urllib
import urllib.request
import tagger
import randomizer as r
import random

PORT = 9097

master_key = random.random()

class MyProxy(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        url = self.path[1:]
        self.send_response(200)
        self.end_headers()
        client_key = hash(str(master_key) + str(self.client_address))

        opened = urllib.request.urlopen('http://localhost/phpbb3/' + url)
        tagged = tagger.tag_file(opened.read())
        randomized = r.randomize(tagged, client_key)
        tagged.write("output.html", short_empty_elements=False)

        self.copyfile(opened, self.wfile)

    def do_POST(self):
        url = self.path

        content_length = int(self.headers.get('Content-Length', 0))
        content = self.rfile.read(content_length)

        req = urllib.request.Request('http://localhost/phpbb3/' + url, method="POST", data=r.derandomize(content))
        output = urllib.request.urlopen(req)

        self.send_response(200)
        self.end_headers()
        self.copyfile(output, self.wfile)


httpd = socketserver.TCPServer(('', PORT), MyProxy)
httpd.serve_forever()
