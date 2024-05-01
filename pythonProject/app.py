import os
from flask import Flask, render_template, request, jsonify
from google.cloud import vision

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'kuickhackhackatonimagelabels-57374b99c466.json'


def detect_labels(image_content):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    detected_labels = [label.description.lower() for label in labels]

    return detected_labels


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        content = file.read()
        labels = detect_labels(content)
        return jsonify({'labels': labels})

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
