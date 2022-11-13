#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import os
import io
import logging
import socketserver
import libcamera

import netifaces
import base64

from http import server
from threading import Condition, Thread

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

from hardware import write_servo,retour_servo,set_motor_modus,display_write

PORT = 8000

ip = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']

iface_usr = os.environ['INTERFACE_USR']
iface_pass = os.environ['INTERFACE_PASS']
iface_auth_base = f'{iface_usr}:{iface_pass}'
iface_bytes = base64.b64encode(iface_auth_base.encode('utf-8'))
iface_auth = iface_bytes.decode('utf-8')


server_dir = '/home/robot/rollout/rollout_server'

def write_to_servo(channel, angle):
    write_servo(int(channel),int(angle))
    return True

def write_to_display(text):
    display_write(f'{ip}:{PORT}\n{text}')
    return True

def shoot():
    retour_servo(0,0,0.5)

def drive(modus):
    set_motor_modus(modus)

def snapshot():
    if os.path.isfile("www/snapshots/snapshot.jpg"):
        index = len(next(os.walk("www/snapshots/album"))[2])
        os.rename("www/snapshots/snapshot.jpg",f"www/snapshots/album/{index:04d}.jpg")
    picam2.capture_file("www/snapshots/snapshot.jpg")

command_router={
    "servo":lambda p : write_to_servo(p["channel"],p["angle"]),
    "shoot":lambda p : shoot(),
    "drive":lambda p: drive(p["modus"]),
    "display": lambda p : write_to_display(p["text"]),
    "snapshot": lambda p :snapshot()
}

mimetypes ={
    ".html":"text/html",
    ".css":"text/css",
    ".js":"text/javascript",
    ".jpeg":"image/jpeg",
    ".jpg":"image/jpg",
    ".png":"image/png"
}


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def creat_paramdict(self,payload):
        rtn = {}
        for param in payload.split("&"):
            _k,_v = param.split("=")
            rtn[_k] = _v
        return rtn


    def serve_file(self,file,code = 200):
        name,extension = os.path.splitext(file)
        with open(file, 'rb') as f:
            content = f.read()
            self.send_response(code)
            self.send_header('Content-Type', mimetypes[extension])
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)


    def do_AUTHHEAD(self):
        with open(server_dir+'/www/codes/401.html', 'rb') as f:
            content = f.read()
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"rollout\"')
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

    def do_GET(self):
        path = self.path.split("?")
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path == '/snapshot.jpg':
            self.serve_file(server_dir+'/www/snapshots/snapshot.jpg')

        elif self.path == '/logout':
            self.serve_file(server_dir+'/www/logout.html',401)

        elif os.path.isfile(server_dir+'/www' + path[0]):
            if self.headers['Authorization'] == None:
                self.do_AUTHHEAD()
                # self.serve_file('/home/robot/rollout_server/www/codes/401.html',401)
                pass
            # amVyb2VuOmplcm9lbg==
            elif self.headers['Authorization']== f'Basic {iface_auth}':
                self.serve_file(server_dir+'/www' + path[0])
                pass
            else:
                self.do_AUTHHEAD()
                logging.warning("got %s",self.headers['Authorization'])
                # self.serve_file('/home/robot/rollout_server/www/codes/401.html',401)
                pass
        
        else:
            self.serve_file(server_dir+'/www/codes/404.html',404)
            # self.send_error(404)
            # self.end_headers()

    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        command = self.path.split('/')[-1]
        payload = self.rfile.read(content_len).decode('utf-8')
        parameters = self.creat_paramdict(payload)
        logging.warning(f'{command}, {content_len} values: {parameters}') 
        if command in command_router:
            command_router[command](parameters)
            content = """POST OK""".encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
config["transform"]  = libcamera.Transform(hflip=1, vflip=1)
picam2.configure(config)

output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    address = ('', PORT)
    server = StreamingServer(address, StreamingHandler)
    write_to_display("server on! 123")
    server.serve_forever()
except:
    display_write("something went wrong!\ncheck SSH")
finally:
    picam2.stop_recording()
