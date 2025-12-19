from flask import Flask, render_template, redirect, url_for, send_from_directory
import subprocess
import os
import glob
from datetime import datetime
import functions  # Import functions for capturing images

app = Flask(__name__)

BASE_DIR = "captured_images"


@app.route("/")
def index():
    # Get today's date in the format used for folders
    today = datetime.now().strftime("%m-%d-%Y")

    # Find all folders matching today's date
    matching_folders = sorted(glob.glob(os.path.join(BASE_DIR, f"{today}_*")), reverse=True)

    # Prepare data structure for templates
    captured_sessions = []
    for folder in matching_folders:
        folder_name = os.path.basename(folder)
        image_files = sorted(glob.glob(os.path.join(folder, "*.jpg")))
        images = [os.path.join(folder, os.path.basename(img)) for img in image_files]

        if images:
            captured_sessions.append({"folder": folder_name, "images": images})

    return render_template("index.html", captured_sessions=captured_sessions)


@app.route("/pallet/")
def pallet_capture():
    return render_template("pallet.html")  # New capture page


@app.route("/browse/")
def browse_images():
    # Get all folders in captured_images directory
    all_folders = sorted(glob.glob(os.path.join(BASE_DIR, "*")), reverse=True)

    # Prepare data structure for templates
    all_sessions = []
    for folder in all_folders:
        if not os.path.isdir(folder):
            continue
        
        folder_name = os.path.basename(folder)
        image_files = sorted(glob.glob(os.path.join(folder, "*.jpg")))
        images = [os.path.join(folder, os.path.basename(img)) for img in image_files]

        if images:
            all_sessions.append({"folder": folder_name, "images": images})

    return render_template("browse.html", captured_sessions=all_sessions)


@app.route("/capture/", methods=["POST"])
def capture():
    functions.capture_images()
    return redirect(url_for("pallet_capture"))  # Redirect back to capture page


@app.route("/captured_images/<path:filename>")
def serve_image(filename):
    return send_from_directory(BASE_DIR, filename)


def launch_kiosk():
    # Prevent launching Chrome twice due to Flask's reloader
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        return

    # Open Chrome in kiosk mode
    subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe",
                      "--kiosk", "http://127.0.0.1:5000/pallet/"])


if __name__ == "__main__":
    launch_kiosk()
    app.run(host="0.0.0.0", port=5000, debug=True)
