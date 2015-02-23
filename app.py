#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify
from time import strftime
from gevent.pywsgi import WSGIServer
# from gevent import monkey; monkey.patch_thread()

# emulated camera
# from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

app = Flask(__name__)
app.debug = False
app.threaded = False


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/_resp_test')
def resp_test():

    str_msg1 = 'Last Tested: ' + strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(rsp_msg1 = str_msg1)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    try:
        print('Starting ...')
        http_server.serve_forever()
    except KeyboardInterrupt:
        print('Caught KeyboardInterrupt')
