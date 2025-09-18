import google.generativeai as genai
import cv2
import numpy as np
from PIL import Image
import os

def extract_text_image(uploaded_file):
    # Convert uploaded file into numpy array
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Preprocess
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, image_bw = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY)

    final_image = Image.fromarray(image_bw)
    
    # Configure genai model
    key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")  # ← no need for from_pretrained

    # OCR prompt
    prompt = '''You act as an OCR application on the given image and extract the text from it.
                Give only the text as output, do not give any other explanation or description.'''

    response = model.generate_content([prompt, final_image])
    return response.text
