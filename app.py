from flask import Flask, render_template, request, redirect, url_for
import os
from pathlib import Path
import torch
from PIL import Image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Pastikan folder upload ada
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load model YOLO sekali di awal
MODEL_PATH = Path("models/best.pt")
model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path=str(MODEL_PATH),
    source="github"  # diunduh dari GitHub, tidak perlu commit folder yolov5
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)

        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            # Simpan file upload
            save_path = Path(app.config["UPLOAD_FOLDER"]) / file.filename
            file.save(save_path)

            # Inference YOLO
            results = model(str(save_path))

            # Simpan hasil (annotated image) ke file baru
            result_img_path = Path(app.config["UPLOAD_FOLDER"]) / f"result_{file.filename}"
            results.render()  # hasil anotasi disimpan di results.ims[0]
            img = Image.fromarray(results.ims[0])
            img.save(result_img_path)

            return render_template(
                "result.html",
                original_image=url_for("static", filename=f"uploads/{file.filename}"),
                result_image=url_for("static", filename=f"uploads/result_{file.filename}")
            )

    return render_template("index.html")


if __name__ == "__main__":
    # Untuk run lokal
    app.run(host="0.0.0.0", port=5000, debug=True)
