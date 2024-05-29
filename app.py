from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np

app = Flask(__name__)

def get_color_name(r, g, b):
    colors = {
        'Red': (255, 0, 0),
        'Green': (0, 255, 0),
        'Blue': (0, 0, 255),
        'Yellow': (255, 255, 0),
        'Cyan': (0, 255, 255),
        'Magenta': (255, 0, 255),
        'White': (255, 255, 255),
        'Black': (0, 0, 0),
        'Gray': (128, 128, 128),
        'Orange': (255, 165, 0),
        'Pink': (255, 192, 203)
    }
    min_distance = float('inf')
    closest_color = None
    for color_name, (cr, cg, cb) in colors.items():
        distance = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    return closest_color

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    resized_image = cv2.resize(image, (100, 500)) 

    strip_height, strip_width, _ = resized_image.shape
    strip_segment_height = strip_height // 10
    colors = []

    for i in range(10):
        segment = resized_image[i * strip_segment_height:(i + 1) * strip_segment_height, :, :]
        average_color = cv2.mean(segment)[:3]
        r, g, b = int(average_color[2]), int(average_color[1]), int(average_color[0])
        color_name = get_color_name(r, g, b)
        colors.append({
            'name': color_name,
            'R': r,
            'G': g,
            'B': b
        })

    return jsonify({'colors': colors})

if __name__ == '__main__':
    app.run(debug=True)
