import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# アップロードフォルダ設定
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 許可する拡張子
ALLOWED_EXTENSIONS = {"xlsx", "xls"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "ファイルが選択されていません", 400

    file = request.files["file"]
    if file.filename == "":
        return "ファイルが選択されていません", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return f"ファイル {filename} がアップロードされました！"
    
    return "許可されていないファイル形式です", 400

if __name__ == "__main__":
    app.run(debug=True)
