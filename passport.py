from flask import Flask, request, render_template
import os
from passporteye import read_mrz

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_passport_info(image_path):
    """Extracts first name, last name, and passport number from the image."""
    mrz = read_mrz(image_path, extra_cmdline_params='--oem 3 --psm 6')
    if mrz:
        data = mrz.to_dict()
        first_name = data.get("names", "").split()[0]  # Extract first word from names
        last_name = data.get("surname", "")  # Get surname
        passport_number = data.get("number", "")  # Get passport number
        return first_name, last_name, passport_number
    return None, None, None  # Return None if extraction fails


@app.route("/", methods=["GET", "POST"])
def index():
    first_name, last_name, passport_number = None, None, None

    if request.method == "POST":
        file = request.files["passport"]
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)  # Save uploaded image

            # Extract passport details
            first_name, last_name, passport_number = extract_passport_info(file_path)

    return render_template("upload.html", first_name=first_name, last_name=last_name, passport_number=passport_number)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
