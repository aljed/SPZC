import socketserver
import http.server
import urllib
import urllib.request
import tagger
import randomizer as r
import random

PORT = 9097
TARGET = 'http://localhost/phpbb3'

master_key = random.random()


class MyProxy(http.server.SimpleHTTPRequestHandler):
    client_keys = {}

    def add_client_key(self):
        if self.client_address[0] not in self.client_keys:
            self.client_keys[self.client_address[0]] = str(hash(str(master_key) + str(self.client_address[0])))[0:16].encode()

    @property
    def ck(self):
        return self.client_keys[self.client_address[0]]

    def do_GET(self):
        url = self.path[1:]
        self.send_response(200)
        self.end_headers()
        self.add_client_key()

        opened = urllib.request.urlopen(f'{TARGET}/{url}')
        if "html" in opened.headers._headers[-1][1]:
            tagged = tagger.tag_file(opened.read().decode())
            randomized = r.randomize(tagged, self.ck)
            self.wfile.write(randomized.encode())
        else:
            self.copyfile(opened, self.wfile)

    def do_POST(self):
        url = self.path

        content_length = int(self.headers.get('Content-Length', 0))
        content = self.rfile.read(content_length)

        req = urllib.request.Request(f'{TARGET}/{url}', method="POST", data=r.derandomize(content, self.ck))
        output = urllib.request.urlopen(req)

        self.send_response(200)
        self.end_headers()

        tagged = tagger.tag_file(output.read().decode())
        randomized = r.randomize(tagged, self.ck)
        self.wfile.write(randomized.encode())


def main():
    httpd = socketserver.TCPServer(('', PORT), MyProxy)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
