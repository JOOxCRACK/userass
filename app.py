from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# مجلد لحفظ الملفات المرفوعة والمخرجة
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        combo_file = request.files.get("combo")
        save_as = request.form.get("output_name", "").strip()

        if not combo_file or not save_as:
            return "❌ تأكد من رفع الملف وكتابة اسم الحفظ"

        # حفظ الملف الأصلي
        input_path = os.path.join(UPLOAD_FOLDER, combo_file.filename)
        output_path = os.path.join(UPLOAD_FOLDER, save_as + ".txt")
        combo_file.save(input_path)

        try:
            with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
                for line in infile:
                    line = line.strip()
                    if ":" in line:
                        email, password = line.split(":", 1)
                        username = email.split("@")[0]
                        outfile.write(f"{username}:{password}\n")
        except Exception as e:
            return f"❌ حصل خطأ أثناء التحويل: {e}"

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

# ✅ ضروري لتشغيل التطبيق على Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
