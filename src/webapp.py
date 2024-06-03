import os
import cv2
from flask import Flask, Response, render_template, session
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from System import System


sys = System()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'


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
    session.clear()
    return render_template('index.html')


@app.route('/webcam', methods=['GET','POST'])
def webcam():
    session.clear()
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
    
    sys.load_video_capture(path)
    sys.configure( 23.5, 15.6, 10, 0.7, 5, 2.5)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webapp')
def webapp():
    sys.load_video_capture(0)
    sys.configure( 23.5, 15.6, 10, 0.7, 5, 2.5)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
