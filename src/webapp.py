import os
import cv2
from flask import Flask, Response, render_template, request, session
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from System import System


sys = System()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['DEFAULT_CONFIG'] = {'sensor_width': 23.5, 'sensor_height': 15.6, 'focal_length': 10, 'camera_position_height': 0.7, 'box_height': 5, 'box_width': 2.5}

class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Run")


def generate_frames():
    yolo_output = sys.analyse_video()
    for detection in yolo_output:
        ret, buffer = cv2.imencode('.jpg', detection)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    if session.get('config', None) is None:
        session['config'] = app.config['DEFAULT_CONFIG']

    return render_template('index.html', config=session['config'])


@app.route('/configure', methods=['GET','POST'])
def configure():
    if session.get('config', None) is None:
        session['config'] = app.config['DEFAULT_CONFIG']

    if request.method == 'POST':
        result = request.form
        json_result = dict(result)
        mapped_result = {key: float(value) for key, value in json_result.items()}

        # save the configuration to the session
        session['config'] = mapped_result
        print(session['config']['focal_length'])
        
    return render_template('index.html', config=session['config'])


@app.route('/webcam', methods=['GET','POST'])
def webcam():
    return render_template('ui.html')


@app.route('/frontpage', methods=['GET','POST'])
def front():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))

        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('new-video.html', form=form)


@app.route('/video')
def video():
    path = session.get('video_path', None)
    if path is None:
        return render_template('new-video.html')
    
    if session.get('config', None) is None:
        session['config'] = app.config['DEFAULT_CONFIG']

    sys.load_video_capture(path)

    sys.configure(session['config']['sensor_width'], session['config']['sensor_height'], session['config']['focal_length'], session['config']['camera_position_height'], session['config']['box_height'], session['config']['box_width'])
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webapp')
def webapp():
    if session.get('config', None) is None:
        session['config'] = app.config['DEFAULT_CONFIG']

    sys.load_video_capture(0)
    sys.configure(session['config']['sensor_width'], session['config']['sensor_height'], session['config']['focal_length'], session['config']['camera_position_height'], session['config']['box_height'], session['config']['box_width'])
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
