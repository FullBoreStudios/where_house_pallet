import cv2
import os
import time
from datetime import datetime, timedelta

# Base directory for saving images
BASE_DIR = "captured_images"
DAYS_TO_KEEP = 240  # Adjust as needed


def prune_old_folders():
    """Delete image folders older than DAYS_TO_KEEP days."""
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP)

    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)

        # Ensure it's a directory and matches our date naming pattern
        try:
            folder_date = datetime.strptime(folder.split("_")[0], "%m-%d-%Y")
            if folder_date < cutoff_date:
                print(f"Deleting old folder: {folder_path}")
                for file in os.listdir(folder_path):
                    os.remove(os.path.join(folder_path, file))
                os.rmdir(folder_path)  # Remove empty folder
        except ValueError:
            continue  # Skip non-date folders


def detect_cameras(max_cams=10):
    cameras = []
    for i in range(max_cams):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use CAP_DSHOW for Windows
        if cap.isOpened():
            cameras.append(i)
        cap.release()
    return cameras


def capture_images():
    prune_old_folders()  # Run cleanup before capturing new images

    cameras = detect_cameras()
    if not cameras:
        print("No cameras detected.")
        return {"status": "error", "message": "No cameras detected."}

    timestamp = datetime.now().strftime("%m-%d-%Y_%I_%M_%p")
    session_folder = os.path.join(BASE_DIR, timestamp)
    os.makedirs(session_folder, exist_ok=True)

    saved_files = []
    for cam_index in cameras:
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                filename = os.path.join(session_folder, f"camera_{cam_index}.jpg")
                cv2.imwrite(filename, frame)
                saved_files.append(filename)
                print(f"Saved: {filename}")
            cap.release()

    return {"status": "success", "files": saved_files}
