from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        combo_file = request.files["combo"]
        save_as = request.form["output_name"].strip()

        if not combo_file or not save_as:
            return "❌ تأكد من رفع الملف وكتابة اسم الحفظ"

        input_path = os.path.join(UPLOAD_FOLDER, combo_file.filename)
        output_path = os.path.join(UPLOAD_FOLDER, save_as + ".txt")
        combo_file.save(input_path)

        with open(input_path, "r") as infile, open(output_path, "w") as outfile:
            for line in infile:
                line = line.strip()
                if ":" in line:
                    email, password = line.split(":", 1)
                    username = email.split("@")[0]
                    outfile.write(f"{username}:{password}\n")

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")
