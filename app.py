# Updated app.py

from flask import Flask, render_template, request
import os
import cv2
import pytesseract

app = Flask(__name__)

# Path to the Tesseract OCR executable (change as needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Predefined text to be detected in the image
target_text = "Pixelflames"

def preprocess_image(img):
    # Resize the image
    img_resized = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur for denoising
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return thresholded


def detect_text_in_image(img, target_text):
    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(img, config='--psm 11')

    # Print the extracted text for debugging
    print("Extracted Text:", extracted_text)

    # Check if the target text is present in the extracted text (case-insensitive)
    text_detected = target_text.lower() in extracted_text.lower()

    return text_detected


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded image file
        uploaded_file = request.files['image']

        if uploaded_file.filename != '':
            # Save the uploaded file to a temporary location
            temp_image_path = "temp_image.jpg"
            uploaded_file.save(temp_image_path)

            # Read the uploaded image
            img = cv2.imread(temp_image_path)

            # Preprocess the image
            preprocessed_img = preprocess_image(img)

            # Detect text in the image
            result = detect_text_in_image(preprocessed_img, target_text)

            # Delete the temporary image file
            os.remove(temp_image_path)

            return render_template('result.html', result=result, target_text=target_text)

    return render_template('index.html')

    #gygyghuihui

if __name__ == '__main__':
    app.run(debug=True)
