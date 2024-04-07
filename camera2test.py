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

@app.route('/video_feed')
def video_feed():
    # Here we define the camera source, which is index 0 by default.
    # If you have multiple cameras, you can select them by changing the index number
    try:
        camera = imageio.get_reader('<video0>',  'ffmpeg', size=(320,240))
        return Response(gen(camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error: {e}")

@app.route('/video_feed_conveyor')
def video_feed_conveyor():
    # Here we define the camera source, which is index 0 by default.
    # If you have multiple cameras, you can select them by changing the index number
    try:
        camera = imageio.get_reader('<video2>',  'ffmpeg', size=(320,240))
        return Response(gen(camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
