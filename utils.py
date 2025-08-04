
import os
import cv2
from ultralytics import YOLO
from bs4 import BeautifulSoup
import requests
from PIL import Image

def extract_text(soup, label):
    row = soup.find("th", string=lambda s: s and label.lower() in s.lower())
    if row and row.find_next_sibling("td"):
        return row.find_next_sibling("td").text.strip()
    return "N/A"

def fetch_car_data(plate_text):
    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "referer": "https://www.carcheck.co.uk/"
    }
    api_url = f"https://www.carcheck.co.uk/reg?i={plate_text}"
    car_info = requests.get(api_url, headers=HEADERS)
    soup = BeautifulSoup(car_info.text, "html.parser")

    vehicle_info = {
        "Make": extract_text(soup, "Make"),
        "Model": extract_text(soup, "Model"),
        "Year": extract_text(soup, "Year of manufacture"),
        "Fuel Type": extract_text(soup, "Fuel type"),
        "Gearbox": extract_text(soup, "Gearbox"),
        "Colour": extract_text(soup, "Colour"),
        "Top Speed": extract_text(soup, "Top speed"),
        "0-60 mph": extract_text(soup, "0 - 60 mph"),
        "Power": extract_text(soup, "Power"),
        "Engine Capacity": extract_text(soup, "Engine capacity"),
        "CO2 Emission": extract_text(soup, "CO2 emission"),
        "CO2 Label": extract_text(soup, "CO2 label"),
        "City MPG": extract_text(soup, "Consumption city"),
        "Extra Urban MPG": extract_text(soup, "Consumption extra urban"),
        "Combined MPG": extract_text(soup, "Consumption combined"),
        "Tax Band": extract_text(soup, "Band"),
        "12-Month Tax": extract_text(soup, "Single payment (12 months)"),
        "MOT Expiry": extract_text(soup, "MOT expiry")
    }
    return vehicle_info

def plate_recognition(uploaded_photo, app, result_image_dir, crop_image_dir):
    model = YOLO("models/license_plate_detector.pt")
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_photo.filename)
    uploaded_photo.save(image_path)

    img = cv2.imread(image_path)
    results = model(img)[0]

    result_image_path = os.path.join(result_image_dir, uploaded_photo.filename)
    cv2.imwrite(result_image_path, img)

    cropped_images = []

    for i, box in enumerate(results.boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        cropped = img[y1:y2, x1:x2]
        cropped_path = os.path.join(crop_image_dir, f"crop_{i}.jpg")
        cv2.imwrite(cropped_path, cropped)
        cropped_images.append(cropped_path)

    return result_image_path, cropped_images


# Recognize characters using YOLOv8
def recognize_characters(CROP_IMAGE):
    char_model = YOLO('models/character_recognizer.pt')
    char_detection = char_model.predict(CROP_IMAGE, save=False)[0]
    char_boxes = []
    CONFIDENCE_THRESHOLD = 0.4

    for box in char_detection.boxes:
        if float(box.conf[0]) < CONFIDENCE_THRESHOLD:
            continue  # skip low-confidence

        cls_id = int(box.cls[0])
        x1 = float(box.xyxy[0][0])  # left x for sorting
        char_label = char_model.names[cls_id]
        char_boxes.append((x1, char_label))

    # Sort characters left to right
    char_boxes.sort(key=lambda x: x[0])
    plate_text = ''.join(label for _, label in char_boxes)
    return plate_text
