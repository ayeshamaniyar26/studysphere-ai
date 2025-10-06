from PIL import Image
import pytesseract

# Path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Load and OCR an image (replace with your actual image)
img = Image.open("test.png")
print(pytesseract.image_to_string(img))
