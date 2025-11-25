import cv2
import io
from PIL import Image
import datetime
import re
import time
import RPi.GPIO as GPIO
import google.generativeai as genai

# ---- CONFIG ----
API_KEY = "AIzaSyC5Q8wJKKSF5gtDLQiThFwbDY3XFKSQtkc"
#CAMERA_URL = "http://192.168.1.9:6464/video"  # Replace with your IP cam / USB cam index (0)
CAMERA_URL = "http://172.16.203.12:8080/video"  # Replace with your IP cam / USB cam index (0)
MODEL_NAME = "gemini-2.0-flash"

# GPIO setup
RED_PIN = 27
YELLOW_PIN = 17
GREEN_PIN = 22

#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
#GPIO.setwarnings(False)
#GPIO.setup(RED_PIN, GPIO.OUT)
#GPIO.setup(YELLOW_PIN, GPIO.OUT)
#GPIO.setup(GREEN_PIN, GPIO.OUT)
#GPIO.output(RED_PIN, GPIO.LOW)
#GPIO.output(YELLOW_PIN, GPIO.LOW)
#GPIO.output(GREEN_PIN, GPIO.LOW)

#def set_led(red=False, yellow=False, green=False):
#    GPIO.output(RED_PIN, red)
#    GPIO.output(YELLOW_PIN, yellow)
#    GPIO.output(GREEN_PIN, green)

def cleanup():
    print("IN cleanup")
    GPIO.cleanup()

# ---- GEMINI SETUP ----
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def capture_frame():
    cap = cv2.VideoCapture(CAMERA_URL)
    if not cap.isOpened():
        raise Exception("Cannot open camera stream.")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise Exception("Failed to capture frame.")
    return frame

def image_to_bytes(frame):
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG")
    return buf.getvalue()

def extract_expiry(img_bytes):
    prompt = (
        "Extract only the expiry date from this medicine packaging image. "
        "Return strictly in 'MM/YYYY' or 'DD/MM/YYYY' format. "
        "If not found, say 'NOT FOUND'."
    )
    response = model.generate_content(
        [prompt, {"mime_type": "image/jpeg", "data": img_bytes}],
        generation_config={"temperature": 0.0}
    )
    return response.text.strip()

def parse_expiry(expiry_text):
    # Try multiple regex formats
    match = re.search(r"(\d{1,2})/(\d{4})", expiry_text)
    if not match:
        return None
    month, year = map(int, match.groups())
    day = 28
    return datetime.date(year, month, day)

def main():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        GPIO.setwarnings(False)
        GPIO.setup(27, GPIO.OUT)
        #GPIO.setup(YELLOW_PIN, GPIO.OUT)
        #GPIO.setup(GREEN_PIN, GPIO.OUT)
        GPIO.output(27, GPIO.LOW)
        #GPIO.output(YELLOW_PIN, GPIO.LOW)
        #GPIO.output(GREEN_PIN, GPIO.LOW)
        print("Capturing image from camera...")
        frame = capture_frame()
        img_bytes = image_to_bytes(frame)

        print("Analyzing image with Gemini...")
        expiry_text = extract_expiry(img_bytes)
        print("Gemini Output:", expiry_text)

        expiry_date = parse_expiry(expiry_text)
        if not expiry_date:
            print("❌ Could not parse expiry date.")
            #set_led(red=True)
            GPIO.setup(22, GPIO.OUT)
            GPIO.output(22, GPIO.HIGH)
            time.sleep(10)  # Keep LED on for 10 seconds
            GPIO.output(22, GPIO.LOW)
            return

        today = datetime.date.today()
        days_left = (expiry_date - today).days
        print(f"Today: {today}")
        print(f"Expiry: {expiry_date}")
        print(f"Days until expiry: {days_left}")

        if days_left < 0:
            print("⚠️ Medicine is EXPIRED!")
            #set_led(red=True)
            #GPIO.output(RED_PIN, GPIO.HIGH)
            GPIO.setup(22, GPIO.OUT)
            GPIO.output(22, GPIO.HIGH)
            time.sleep(10)  # Keep LED on for 10 seconds
            GPIO.output(22, GPIO.LOW)
        elif days_left <= 14:
            print("⚠️ Expiring soon (within 2 weeks).")
            #set_led(yellow=True)
            #GPIO.output(YELLOW_PIN, GPIO.HIGH)
            GPIO.setup(27, GPIO.OUT)
            GPIO.output(27, GPIO.HIGH)
            time.sleep(10)  # Keep LED on for 10 seconds
            GPIO.output(27, GPIO.LOW)
        else:
            print("✅ Medicine is valid.")
            #set_led(green=True)
            #GPIO.output(GREEN_PIN, GPIO.HIGH)
            GPIO.setup(17, GPIO.OUT)
            GPIO.output(17, GPIO.HIGH)
            time.sleep(10)  # Keep LED on for 10 seconds
            GPIO.output(17, GPIO.LOW)

        #time.sleep(10)  # Keep LED on for 10 seconds

    finally:
        cleanup()

if __name__ == "__main__":
    main()
