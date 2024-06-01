import cv2
from flask import Flask, Response
from System import System


sys = System()

app = Flask(__name__)


def generate_frames():
    yolo_output = sys.analyse_video()
    for detection in yolo_output:
        ret, buffer = cv2.imencode('.jpg', detection)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

@app.route('/video')
def video():
    sys.load_video_capture('../bikes.mp4')
    sys.configure( 23.5, 15.6, 10, 0.7, 5, 2.5)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webcam')
def webcam():
    sys.load_video_capture(0)
    sys.configure( 23.5, 15.6, 10, 0.7, 5, 2.5)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
