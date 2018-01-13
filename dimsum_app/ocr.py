from PIL import Image
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'


def ocr_menu(image_file):
    '''
    Perform OCR on an image of a menu
    '''
    # TODO: test if converting images to grayscale improves accuracy
    image = Image.open(image).convert('L')
    start = time.time()
    # LSTM Tesseract engine is used because of the config flag
    print pytesseract.image_to_string(image, config='-oem 1').encode('utf-8')
    print time.time() - start
