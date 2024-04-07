from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from picamera2 import Picamera2, Preview
import imageio
import io, time, threading, subprocess, os, json

# PICAM2 - Video Streamer
# For main Front Camera connected over Pi Camera Bus
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

# Instantiate VideoStreamer
streamer = VideoStreamer()

# SERVER
app = Flask(__name__)
CORS(app)   # CORS to allow access to files from another IP

# Main Stream Access Point
# - Access the video feed (streamed jpeg file) over 192.168.1.2/video_feed
@app.route('/video_feed_main')
def video_feed_main():
    """Video streaming route."""
    return Response(streamer.capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# SERVER API

# API Route to update stream quality settings
# - Gets params from client-side app and calls streamer.update_settings
@app.route('/update_settings', methods=['POST'])
def update_settings():
    data = request.json
    resolution = tuple(data.get('resolution'))
    jpeg_quality = int(data.get('jpeg_quality'))
    frame_rate = int(data.get('frame_rate'))
    if resolution and jpeg_quality is not None and frame_rate is not None:
        streamer.update_settings(resolution, jpeg_quality, frame_rate)
        return 'Settings updated successfully', 200
    else:
        return 'Invalid request data', 400

# API Route to send bitrate information
# - Captures packets on Raspi with dumpcap
# - Analyzes packets with tshark
# - Computes average bitrate and provides result back to client
@app.route('/get_bitrate', methods=['GET'])
def get_bitrate():
    capture_duration = 10  # seconds
    capture_file = "/tmp/capture.pcap"
    interface = "wlan0"  # or wlan0, or your relevant network interface
    
    # Start dumpcap to capture packets
    dumpcap_cmd = f"sudo dumpcap -a duration:{capture_duration} -w {capture_file} -i {interface}"
    subprocess.run(dumpcap_cmd.split())
    
    # Analyze the capture with tshark to compute the bitrate
    tshark_cmd = f"tshark -r {capture_file} -q -z io,stat,1"
    tshark_output = subprocess.run(tshark_cmd.split(), capture_output=True)
    
    # Extract the average bitrate
    try:
        output = tshark_output.stdout.decode('utf-8')
        lines = output.split('\n')
        bitrate_line = next(line for line in lines if "Duration" in line)
        bitrate_info = bitrate_line.split()
        avg_bitrate = bitrate_info[-2]  # Assuming the second last entry is the average bitrate
    except Exception as e:
        return jsonify({"error": "Failed to compute bitrate", "details": str(e)}), 500

    # Remove the capture file to save space
    os.remove(capture_file)

    # Send the bitrate information back to the client
    return jsonify({"avg_bitrate": avg_bitrate}), 200


# Use 'imageio_ffmpeg' as reader to read the video feed
def gen(camera):
    while True:
        frame = camera.get_next_data()
        img = imageio.imwrite('<bytes>', frame, format='.jpg')  # Write frame to bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

# IMAGEIO DUMP BUCKET CAM ON VIDEO0
@app.route('/video_feed_dump_bucket')
def video_feed_dump_bucket():
    try:
        camera = imageio.get_reader('<video0>',  'ffmpeg', size=(320,240))
        return Response(gen(camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error: {e}")

# IMAGEIO CONVEYOR CAM ON VIDEO2
@app.route('/video_feed_conveyor')
def video_feed_conveyor():
    try:
        camera = imageio.get_reader('<video2>',  'ffmpeg', size=(320,240))
        return Response(gen(camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)
