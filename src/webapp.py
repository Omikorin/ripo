import cv2
from flask import Flask, Response
from System import System


sys = System()
sys.load_video_capture(0)
sys.configure( 23.5, 15.6, 10, 0.7, 5, 2.5)

app = Flask(__name__)


def generate_frames(path):
    yolo_output = sys.analyse_video()
    for detection in yolo_output:
        ret, buffer = cv2.imencode('.jpg', detection)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

@app.route('/webcam')
def webcam():
    return Response(sys.analyse_video(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
