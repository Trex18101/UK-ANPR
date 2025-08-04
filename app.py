
import os
from flask import Flask, render_template, request, redirect, url_for
from utils import plate_recognition, recognize_characters, fetch_car_data

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_IMAGE_DIR = 'static/results'
CROP_IMAGE_DIR = 'static/crops'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_IMAGE_DIR, exist_ok=True)
os.makedirs(CROP_IMAGE_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_photo = request.files['image']
        if uploaded_photo:
            result_image_path, cropped_paths = plate_recognition(uploaded_photo, app, RESULT_IMAGE_DIR, CROP_IMAGE_DIR)

            results = []
            for crop in cropped_paths:
                plate_text = recognize_characters(crop)
                vehicle_info = fetch_car_data(plate_text)
                results.append({
                    'plate': plate_text,
                    'cropped_image': crop,
                    'vehicle_info': vehicle_info
                })

            return render_template('result.html', result_image=result_image_path, results=results)

    return render_template('index.html')

@app.route('/result')
def result():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
