import os
from flask import Flask, render_template, request, jsonify
from google.cloud import vision

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'kuickhackhackatonimagelabels-57374b99c466.json'

FORBIDDEN_LABELS = [
    "meat", "cigarette", "fast food", "casino", "alcohol", "drugs",
    "gambling", "junk food", "sugar", "soda", "smoking", "overeating",
    "sedentary", "lack of exercise", "sleep deprivation", "red meat",
    "tobacco", "casino", "advertisement", "poster"
]


def detect_labels(image_content):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    detected_labels = [label.description.lower() for label in labels]
    has_forbidden_label = any(label in detected_labels for label in FORBIDDEN_LABELS)

    return detected_labels, has_forbidden_label


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        content = file.read()
        labels, has_forbidden_label = detect_labels(content)
        return jsonify({'labels': labels, 'forbidden': has_forbidden_label})

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
