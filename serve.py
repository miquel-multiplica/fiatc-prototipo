import http.server, socketserver, functools

handler = functools.partial(
    http.server.SimpleHTTPRequestHandler,
    directory='/Users/miquelmir/Fiatc'
)
with socketserver.TCPServer(("", 8080), handler) as httpd:
    httpd.serve_forever()
