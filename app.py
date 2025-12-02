from flask import Flask, request, send_file, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# ① ブラウザでアクセスしたときに表示する簡易ページ
@app.route("/", methods=["GET"])
def index():
    return """
    <html>
      <body>
        <h1>Image Compress API</h1>
        <p>POST /convert に画像を送ると JPEG に変換＆圧縮します。</p>
        <form action="/convert" method="post" enctype="multipart/form-data">
          <p><input type="file" name="image" required></p>
          <p>Quality: <input type="number" name="quality" value="80" min="1" max="95"></p>
          <p><button type="submit">Convert</button></p>
        </form>
      </body>
    </html>
    """

# ② 実際に変換を行うAPI
@app.route("/convert", methods=["POST"])
def convert_image():
    # フォーム名 image のファイルを受け取る
    if "image" not in request.files:
        return jsonify({"error": "No image file provided. Use form field name 'image'."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    # quality パラメータ
    quality = request.form.get("quality", default="80")
    try:
        quality = int(quality)
        if not (1 <= quality <= 95):
            raise ValueError()
    except ValueError:
        return jsonify({"error": "Invalid quality. It must be an integer between 1 and 95."}), 400

    try:
        img = Image.open(file)

        # JPEG用に RGB に変換
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        buf.seek(0)

        return send_file(
            buf,
            mimetype="image/jpeg",
            as_attachment=False,
            download_name="converted.jpg",
        )

    except Exception as e:
        return jsonify({"error": "Failed to process image.", "detail": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
