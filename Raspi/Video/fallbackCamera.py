# Open a network camera stream over UDP that is then read from client PC
# ! Not working

import subprocess
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

# Initialize Picamera2
picamera2 = Picamera2()

# Prepare the video configuration and start the preview
video_config = picamera2.create_video_configuration(main={"size": (1920, 1080)})
picamera2.configure(video_config)
picamera2.start()

# Use ffmpeg to encode and stream the video
# Note: Adjust the ffmpeg command to suit your streaming setup and destination
ffmpeg_command = [
    'ffmpeg',
    '-f', 'v4l2',  # Input format
    '-i', '/dev/video0',  # Input device file
    '-f', 'mpegts',  # Output format
    '-codec:v', 'mpeg1video',  # Output codec
    '-s', '1920x1080',  # Output size
    'udp://<destination_ip>:<port>'  # Streaming destination
]

# Start ffmpeg process
subprocess.run(ffmpeg_command)
