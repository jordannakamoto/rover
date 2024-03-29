# Video Streamer
# Raspi Camera
# Captures and produces frame as a jpeg file
# params: resolution, jpeg_quality, frame_rate

from picamera2 import Picamera2
import io, time

class VideoStreamer:
    def __init__(self):
        self.picamera2 = Picamera2()
        # resolution
        self.config = self.picamera2.create_still_configuration(main={"size": (160, 120)}) # set config for capturing still frames (jpeg)
        self.picamera2.configure(self.config)
        # jpeg_quality
        self.jpeg_quality = 5
        self.picamera2.options['quality'] = self.jpeg_quality                              # picamera2 jpeg quality param
        # frame_rate
        self.frame_rate = 10
        self.stream = io.BytesIO()
 
    def capture_frames(self):
        self.picamera2.start()
        while True:
            start_time = time.time()
            # Capture the frame
            self.stream.seek(0)
            self.picamera2.capture_file(self.stream, format='jpeg')
            frame = self.stream.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # FPS control
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1.0 / self.frame_rate - elapsed_time)
            time.sleep(sleep_time)                                                         # waits for t amount of time before capturing next frame
        self.picamera2.stop()
 
	# stop camera > change configuration > restart camera
    def update_settings(self, resolution, jpeg_quality, frame_rate):
        self.picamera2.stop()
        self.config = self.picamera2.create_still_configuration(main={"size": resolution})
        self.picamera2.configure(self.config)
        self.jpeg_quality = jpeg_quality
        self.frame_rate = frame_rate
        self.picamera2.options['quality'] = self.jpeg_quality
        self.picamera2.start()