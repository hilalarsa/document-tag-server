import pytesseract
import nltk
import difflib
import json

import sys
import re
import os

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# from external file
from tesseract_ocr import image_to_text, change_format_and_ocr
from pypdf_test import pdf_to_text
from difflib_checker import text_matcher, text_matcher_dosen, get_document_type, regex_checker
from api import get_data

# receive filepath, filter to either pdf or image
def textTransform(filePath):
    filename, file_extension = os.path.splitext(filePath)
    if(file_extension == ".jpeg" or file_extension == ".jpg" or file_extension == ".png" or file_extension == ".pbm" or file_extension == ".bmp" ):
        # Format Image
        transformed_text = image_to_text(filePath)
        return(transformed_text)
    elif (file_extension == ".pdf" ):
        # Format PDF
        transformed_text = pdf_to_text(filePath, filename)
        if(transformed_text is None ):
            # print("PDF IS FAILING")
            transformed_text = change_format_and_ocr(filePath, filename)
        return(transformed_text)
    else:
        print("Format Unrecognized. Aborting ...")

# create stopper
# factoryRemover = StopWordRemoverFactory()
# stopword = factoryRemover.create_stop_word_remover()

# create stemmer (disabled, not necessary)
# factoryStemmer = StemmerFactory()
# stemmer = factoryStemmer.create_stemmer()

# tesseract run on subject to raw text
# rawText = pytesseract.image_to_string('./contoh 2 surat tugas.jpeg', lang='ind')
# raw_text = pytesseract.image_to_string('../sample/lembarpengesahan1.jpeg', lang='ind')
# raw_text = textTransform("../sample/tugas/tugas_kolektif3.jpeg")
# raw_text = textTransform("../sample/sertifikat/sertifikat1.jpeg")
# raw_text = textTransform(sys.argv[1])
# raw_text = textTransform(sys.argv[1])
raw_text = textTransform("../../sample/lembar pengesahan/lembarpengesahan1.jpeg")
# raw_text = textTransform("../sample/tugas/tugas_individu1.jpeg")
# raw_text = textTransform("../sample/other/test3.pdf")
# raw_text = textTransform("../sample/pengujian/keputusan1.jpg")
# raw_text = textTransform("../sample/pengujian/lampiran-jurnal.pdf")
# raw_text = textTransform("../sample/pengujian/lembarpengesahan1.jpeg")
# raw_text = textTransform("../sample/pengujian/sertifikat1.jpeg")
# raw_text = textTransform("../sample/sertifikat/sertifikat2.pdf")
# raw_text = textTransform("../sample/sertifikat/tugas_individu2.pdf")
# raw_text = textTransform("../sample/pengujian/tugas_kolektif1.jpeg")
# tokenize text into sentences
sentences = nltk.sent_tokenize(raw_text)
# split sentence into individual word
full_words = []
for i, sentence in enumerate(sentences):
    # change all text to lowercase
    resultLowerCase = sentence.lower()
    # replace enter (\n) with space
    resultNoEnter = re.sub('[\t\n]', ' ', resultLowerCase)
    # replace tabs and multiple spaces with single space
    resultNoTab = re.sub(' +', ' ', resultNoEnter)
    # change text encoding to utf8
    encodedText = resultNoTab
    # encodedText = resultNoTab.encode("utf-8")
    # # apply Sastrawi stopper removal
    # endText = stopword.remove(encodedText)

    word = encodedText.split()
    full_words = full_words + word
    # print words
# text ready to be compared with database
dataDosen = get_data('dosen')
dataJudul = get_data('judul')
dataRegexNomor = get_data('nomor')
dataRegexIsi = get_data('isi')

# sample
# dataDosen = ['ahmadi yuli ananta','ariadi retno tri hayati ririd','arief prasetyo','banni satria andoko','budi harijanto','cahya rahmad','deddy kusbianto purwoko aji','dimas wahyu wibowo''dwi puspitasari','dyah ayu irawati','ekojono','ely setyo astuti','erfan rohadi','faisal rahutomo','gunawan budiprasetyo','hendra pradibta','imam fahrur rozi','indra dharma wijaya','luqman affandi', 'nurudin santoso','putra prima arhandi','rawansyah','ridwan rismanto','rosa andrie asmara','siti romlah','ulla defana rosiani','yan watequlis syaifudin']
# dataJudul = ['surat tugas', 'lembar pengesahan']

# check document type
document_type_matched_array = []
is_multiple = ""
for item in dataJudul:
    trigger_word_array = item['trigger_word'].split(', ') # get trigger word, split by comma and space to get its array form
    for trigger_word in trigger_word_array: 
        a = text_matcher(full_words, trigger_word)
        if a is not None:
            # document_type_matched_array = get_document_type_matched_array(a['text'], item) # get da doc type by checking trigger word with outputted text from difflib checker
            # document_type_matched_array += a['text'] + ', '
            document_type_matched_array.append(item['tipe_judul']) # save tipe judul as doc type ONLY IF text matcher showing FIRST RESULT (FLAW)
            break
        else:
            continue

if(len(document_type_matched_array) == 0):
    document_type_matched_array.append('unknown')

nama_dosen = []

# for is_multiple false, untuk tipe surat yang urutan dosennya tidak berpengaruh
    # for item in dataDosen:
    #     a = text_matcher(full_words, item["nama_dosen"])
    #     if a is not None:
    #         print(a)
    #         nama_dosen.append(a)


for word in full_words:
    for dosen in dataDosen:
        # nama_split = dosen['nama_dosen'].split()
        a = text_matcher_dosen(dosen['nama_dosen'], word)
        if a is not None:
            nama_dosen.append(a)

dosen_array = []
dosen_text = ""
for i, nama in enumerate(nama_dosen):
    for dosen in dataDosen:
        dosennamefull = dosen['nama_dosen'].split()
        part_length = len(dosennamefull)
        counter = 0
        for dosen_name in dosennamefull:
            if(nama_dosen[i+counter] == dosennamefull[counter] and counter <= part_length and i+counter < len(nama_dosen)-1):
                dosen_text = dosen_text + " " + nama_dosen[i+counter]
                counter = counter + 1
                if(counter == part_length):
                    dosen_array.append({"text": dosennamefull, "counter": "1", "nidn": dosen['nidn'], "nip": dosen['nomor_dosen']})
                    dosen_text = ""
            else:
                dosen_text = ""
                break
nama_dosen = dosen_array

dosenAmount = len(nama_dosen)
document_type = '' # tipe dokumen or document type to be outputted
document_is_multiple = '' # tag for whether the tipe's bobot is affected by dosen amount
for item in dataJudul:
    for doc_type in document_type_matched_array: # break document_type_matched_array array and check if inside got is_multiple = true (means dosen amount is matter, and bobot is applied differently)
        if(item['tipe_judul'] == doc_type and item['is_multiple'] == "true" and dosenAmount > 1): # tipe_judul in loop is same as breaked array of matched doc_type PLUS nama dosen in document is more than 1
            # do something here with pembobotan for doc that has dosen > 1
            document_type = item['tipe_judul']
            document_is_multiple = "true"

# print(nama_dosen)
# print(document_type)

if(document_type == ''): # if no dosen or dosen only 1 name in doc, apply first array value
    document_type = document_type_matched_array[0] # if dosen amount doesnt matter, array will ALWAYS has 1 index, so just get the 1st value in the array as legit doc type
    document_is_multiple = "false"

# pembobotan start here
nama_dosen_final = []
for i, nama in enumerate(nama_dosen):
    if(document_is_multiple == "true"):
        bobot = (dosenAmount-i) * 10
    else:
        bobot = 10 # default bobot if dosen amount doesnt matter

    nama_dosen_final.append({"nama_dosen":' '.join(nama['text']), "bobot":bobot, "nidn": nama['nidn'], "nip": nama['nip']})


nomor_surat = []
for regex in dataRegexNomor:
    for word in full_words:
        result = regex_checker(regex['regex_nomor'], word)
        if result is not None:
            nomor_surat.append(result)

tanggal = []
for regex in dataRegexIsi:
    for word in full_words:
        result = regex_checker(regex['regex_isi'], word)
        if result is not None:
            print(result)
            tanggal.append(result)

filepath = "../sample/tugas/tugas_individu1.jpeg"
# filepath = sys.argv[1]
file_name = os.path.basename(filepath)
print(nama_dosen_final)
print("filename: "+file_name)
print("doc_type: "+document_type)
for item in nama_dosen_final:
    # if(len(item)>0):
    print("\tnama_dosen: "+item['nama_dosen'])
    print("\tbobot: "+str(item['bobot']))
    print("\tnip: "+item['nip'])
    print("\tnidn: "+item['nidn'])
print("nomor:" + ' '.join(nomor_surat))
print("tanggal: " + ' '.join(tanggal))



# print(''.join(nomor_surat))
# sys.stdout.flush()
# TODO : regex !!!
# JUDUL
# for item in dataJudul:
    # triggerWord = item['trigger_word']
    # print(triggerWord)
    # print(text_matcher(full_words, item['trigger_word'])) # text_matcher(sourceWord, testedWord):


# check document extension (V)
# check dosen name, and name occurance
# check document type
# check rest info

