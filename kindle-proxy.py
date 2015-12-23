#!/usr/bin/python

import requests
import BaseHTTPServer
from readability.readability import Document

class ProxyRetrieve():

    def handle(self):
        r = requests.get('http://azarius.vagrant/news/580/Farewell_Wubbo_Ockels/')
        doc = Document(r.text)

        content = doc.summary(html_partial=False)

        # FIXME pythons socket lib breaks on a unicode object, find out how to properly fix that
        content = content.encode('ascii', 'backslashreplace')

        headers = r.headers

        if 'Content-Encoding' in headers:
            del headers['Content-Encoding']

        headers['Content-Length'] = len(content)

        return (headers, content)

class ProxyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    retriever = None

    def do_GET(self):
        (headers, content) = self.retriever.handle()

        self.send_response(200)
        self._write_headers(headers)

        self.wfile.write(content)

    def _write_headers(self, headers):
        for header in headers.items():
            self.send_header(header[0], header[1])

        self.end_headers()


def main():
    address = ''
    port = 8080
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

