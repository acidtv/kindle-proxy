#!/usr/bin/python

import argparse
import requests
import BaseHTTPServer
from readability.readability import Document

class ProxyRetrieve():

    def handle(self, path):
        r = requests.get(path)
        doc = Document(r.text)

        content = doc.summary(html_partial=True)
        content = self.prettify(doc, content)

        if len(content) < 1000:
            content = r.text

        content = content.encode('utf8')

        return content

    def prettify(self, doc, content):
        content = u'<html><head><title>%s</title></head><body><h1>%s</h1>%s</body></html>' \
            % (doc.title(), doc.short_title(), content)

        return content

class ProxyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    retriever = None

    def do_GET(self):
        content = self.retriever.handle(self.path)

        if type(content) is not str:
            raise Exception('Returned content should be of type str, otherwise it cannot be written to a socket.')

        headers = {
            'Content-Length': len(content),
            'Content-Type': 'text/html; charset=utf-8'
        }

        self.send_response(200)
        self._write_headers(headers)

        self.wfile.write(content)

    def _write_headers(self, headers):
        for header in headers.items():
            self.send_header(header[0], header[1])

        self.end_headers()


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', dest='port', type=int, default=8080, help='The port number to listen on')
    args = parser.parse_args()

    address = ''
    port = args.port
    server_address = ('', port)
    ProxyRequestHandler.retriever = ProxyRetrieve()
    httpd = BaseHTTPServer.HTTPServer(server_address, ProxyRequestHandler)

    print 'Serving on %s:%s...' % (address, port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Interrupted, quitting...'

if __name__ == '__main__':
    main()

