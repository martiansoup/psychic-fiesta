#!/usr/bin/env python3
import http.server
import socketserver
import shutil
import urllib.parse
import os
import subprocess

PORT = 80

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server, directory="server")

    def do_GET(self):
        if self.path.replace("/", "") == "code":
            with open("lights.py", "rb") as src:
                fs = os.fstat(src.fileno())
                self.send_response(http.HTTPStatus.OK)
                self.send_header("Content-type", "text/python")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Content-Length", str(fs[6]))
                self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
                self.end_headers()
                shutil.copyfileobj(src, self.wfile)
        elif "status" in self.path:
            p = subprocess.run(["systemctl", "status", "lights"], capture_output=True)
            output = p.stdout
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", "text/plain")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(output)))
            self.end_headers()
            self.wfile.write(output)
        elif "upload" in self.path:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", "text/json")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", "0")
            self.end_headers()
            os.system("/home/pi/upload.sh")
        else:
            super().do_GET()

    def do_POST(self):
        self.send_response(http.HTTPStatus.MOVED_PERMANENTLY)
        self.send_header("Location", "/")
        self.end_headers()
        length = int(self.headers.get('content-length'))
        contents = self.rfile.read(length).decode().replace("+", " ")
        parsed = urllib.parse.unquote(contents).replace("src=", "").replace("\r\n", "\n")
        with open("lights.py", "w") as f:
            f.write(parsed)
        os.system("systemctl restart lights")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started at http://127.0.0.1:{}".format(PORT))
    httpd.serve_forever()
