from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return jsonify({'error': '画像が送られていません'}), 400

    image = request.files['image']
    quality = int(request.form.get('quality', 40))

    input_path = f"/tmp/{image.filename}"
    output_path = input_path.rsplit('.', 1)[0] + '_compressed.jpg'

    image.save(input_path)

    try:
        img = Image.open(input_path)
        img = img.convert('RGB')
        img.save(output_path, 'JPEG', quality=quality)
        return jsonify({'message': '成功', 'compressed_image_path': output_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
