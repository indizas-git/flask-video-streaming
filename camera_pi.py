import time
import io
import threading
import picamera
from fractions import Fraction

class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread

    def __init__(self):
        if self.thread is None:
            # start background frame thread
            self.thread = threading.Thread(target=self._thread)
            self.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            # camera.hflip = True
            # camera.vflip = True

            # let camera warm up
            # camera.start_preview()
            # time.sleep(2)

            camera.resolution = (1296,730)
            camera.framerate = Fraction(3,1)
            camera.annotate_frame_num = True

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True, resize=(648,365)):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
