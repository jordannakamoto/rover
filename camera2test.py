from flask import Flask, Response
import imageio

app = Flask(__name__)

def gen(camera):
    while True:
        # Use 'imageio_ffmpeg' as reader to read the video feed
        frame = camera.get_next_data()
        img = imageio.imwrite('<bytes>', frame, format='.jpg')  # Write frame to bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

# IMAGEIO DUMP BUCKET CAM ON VIDEO0
@app.route('/video_feed_dump_bucket')
def video_feed():
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
    app.run(host='0.0.0.0', port=5001, debug=True)
