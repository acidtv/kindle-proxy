#!/usr/bin/python

import requests
import BaseHTTPServer
from readability.readability import Document

class ProxyRetrieve():

    def handle(self):
        r = requests.get('http://azarius.vagrant/news/580/Farewell_Wubbo_Ockels/')
        doc = Document(r.text)

        content = doc.summary(html_partial=False)

        r.headers['Content-Length'] = len(content)

        return (r.headers, content)

class ProxyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        r = ProxyRetrieve()
        (headers, content) = r.handle()

        self.send_response(200)
        self._write_headers(headers)

        self.wfile.write(content)

    def _write_headers(self, headers):
        for header in headers.items():
            self.send_header(header[0], header[1])

        self.end_headers()


def main():
    server_address = ('', 8080)
    httpd = BaseHTTPServer.HTTPServer(server_address, ProxyRequestHandler)

    print 'Serving...'
    httpd.serve_forever()

if __name__ == '__main__':
    main()

