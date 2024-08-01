from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
import cv2
from moviepy.editor import VideoFileClip
from roadlane import detect_lanes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], 'output_' + filename)
        process_video(filepath, output_filepath)
        
        return send_file(output_filepath, as_attachment=True)

def process_video(input_path, output_path):
    clip = VideoFileClip(input_path)
    processed_clip = clip.fl_image(detect_lanes)
    processed_clip.write_videofile(output_path, audio=False)

if __name__ == '__main__':
    app.run(debug=True)
