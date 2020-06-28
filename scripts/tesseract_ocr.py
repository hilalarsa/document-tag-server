import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re
import os

from PIL import Image
from itertools import izip

import ghostscript
import locale

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from pdf2image import convert_from_path, convert_from_bytes


def change_format_and_ocr(pdf_input_path, filename):
    jpeg_output_path = filename+".jpeg"
    args = ["pdf2jpeg", # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r144",
            "-sOutputFile=" + jpeg_output_path,
            pdf_input_path]

    encoding = locale.getpreferredencoding()
    args = [a.encode(encoding) for a in args]

    ghostscript.Ghostscript(*args)
    return image_to_text(jpeg_output_path)


# img = cv2.imread('image.jpg')
def write_image_to_disk(image, filename):
    # Filename must include extension
    destination = './image_output'
    os.chdir(destination) 

    # Saving the image 
    cv2.imwrite(filename, image)

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    
    thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = thresh.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 


def image_to_data(filePath):
    # tesseract run on subject
    data = pytesseract.image_to_data(filePath, lang='ind', output_type=Output.DICT)
    return data

def slice_per(source, step):
    return [source[i::step] for i in range(step)]

def rotate_image(image, center = None, scale = 1.0):
    angle=360-int(re.search('(?<=Rotate: )\d+', pytesseract.image_to_osd(image)).group(0))
    (h, w) = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

def check_rotation(filepath):
    im = cv2.imread(str(filepath), cv2.IMREAD_COLOR)
    newdata=pytesseract.image_to_osd(im)
    # re.search('(?<=Rotate: )\d+', newdata).group(0)
    return rotate_image(im)

# TESSERACT
def image_to_text(filePath):
    image = cv2.imread(filePath)
    # image = deskew(image)
    image = check_rotation(filePath) # if image sideways, it will be rotated based on tesseract confidence level

    image = get_grayscale(image) # jadi abu2
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] # jadi hitam putih
    # image = cv2.medianBlur(image, 3) # diperjelas

    # image = thresholding(image)
    # image = opening(image)

    # tesseract run on subject
    text = pytesseract.image_to_string(image, lang='ind')
    # write_image_to_disk(image, "opening-test2.jpg")
    return text