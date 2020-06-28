import pytesseract
import nltk
import difflib
import json

import sys
import re
import os

# from external file
from tesseract_ocr import image_to_text

# filePath = [ "../sample/bad_image/UNCLEAR-1.jpeg", "../sample/bad_image/UNCLEAR-3.jpeg", "../sample/bad_image/VERTICAL-2.jpg", "../sample/bad_image/WRONG RESULT- SAME NAME AS DOSEN- 1.jpeg"]
# filePath = [ "../sample/bad_image/UNCLEAR-1.jpeg", "../sample/bad_image/UNCLEAR-3.jpeg"]
# filePath = [ "../sample/sertifikat/sertifikat1.jpeg"]
# filePath = [ "../sample/tugas/tugas_kolektif1.jpeg"]
filePath = ["../sample/bad_image/VERTICAL-2.jpg"]
# filePath = ["../sample/bad_image/VERTICAL2.jpeg"]


def preprocess_text(sentences):
    # split sentence into individual word
    full_words = []
    for i, sentence in enumerate(sentences):
        # change all text to lowercase
        resultLowerCase = sentence.lower()
        # replace enter (\n) with space
        resultNoEnter = re.sub('\n', ' ', resultLowerCase)
        # replace tabs and multiple spaces with single space
        resultNoTab = re.sub(' +', ' ', resultNoEnter)
        # change text encoding to utf8
        encodedText = resultNoTab
        # encodedText = resultNoTab.encode("utf-8")
        # # apply Sastrawi stopper removal
        # endText = stopword.remove(encodedText)

        word = encodedText.split()
        full_words = full_words + word
    return full_words

for item in filePath:
    # raw_text = textTransform("../sample/s_tugas1.jpeg")
    raw_text = image_to_text(item)
    sentences = nltk.sent_tokenize(raw_text)
    full_words = preprocess_text(sentences)

sentence = ""
for word in full_words:
    sentence = sentence + " " + word

print sentence
