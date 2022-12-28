import http.server
import os


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = "/netw/p2p/p2pNode.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


def run(port=8000):
    httpd = http.server.HTTPServer(("", port), MyHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
