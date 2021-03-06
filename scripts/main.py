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
# raw_text = textTransform("../../sample/lembar pengesahan/lembarpengesahan1.jpeg")
# raw_text = textTransform("../sample/other/test3.pdf")
# raw_text = textTransform("../../sample/pengujian/keputusan1.jpg")
# raw_text = textTransform("../../sample/pengujian/lampiran-jurnal.jpeg")
# raw_text = textTransform("../../sample/pengujian/lampiran-jurnal.pdf")
# raw_text = textTransform("../../sample/pengujian/lembarpengesahan1.jpeg")
# raw_text = textTransform("../../sample/pengujian/sertifikat1.jpeg")
# raw_text = textTransform("../../sample/pengujian/sertifikat2.jpg")
# raw_text = textTransform("../../sample/pengujian/surat-pengangkatan1.jpeg")
# raw_text = textTransform("../../sample/pengujian/surat-pengangkatan1.pdf")
# raw_text = textTransform("../../sample/pengujian/testpdf.pdf")
raw_text = textTransform(sys.argv[1])
# raw_text = textTransform("../../sample/bank/bca1.jpeg")
# raw_text = textTransform("../../sample/bank/bca2.jpeg")
# raw_text = textTransform("../../sample/bank/bca2.jpg")
# raw_text = textTransform("../../sample/bank/bca4.png")
# raw_text = textTransform("../../sample/bank/bca7.jpg")
# raw_text = textTransform("../../sample/ajar/ajar1.jpeg")
# raw_text = textTransform("../../sample/ajar/ajar2.pdf")
# raw_text = textTransform("../../sample/ajar/ajar3.jpg")
# raw_text = textTransform("../../sample/ajar/ajar4.jpg")
# raw_text = textTransform("../../sample/tugas/tugas_individu1.jpeg")
# filepath = sys.argv[1]
# filepath = "../../sample/good_image/tugas_individu2.pdf"
# raw_text = textTransform(filepath)
# raw_text = textTransform(sys.argv[1])
# print(raw_text.replace("\n", "\\n"))
# tokenize text into sentences
sentences = nltk.sent_tokenize(raw_text)
# print(sentences)
# split sentence into individual word
full_words = []
for i, sentence in enumerate(sentences):
    # remove symbols and weird char
    resultClearChar = re.sub('[@?!#$%^&*(),.|]', '', sentence)
    # change all text to lowercase
    resultLowerCase = resultClearChar.lower()
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
# print(full_words)
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
            if(nama_dosen[i+counter] == dosennamefull[counter] and counter <= part_length and i+counter < len(nama_dosen)-1): # change to len(nama_dosen)-1 cz dosen name is bugged
                dosen_text = dosen_text + " " + nama_dosen[i+counter]
                counter = counter + 1
                if(counter == part_length):
                    # print(dosen_text)
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
    for i, word in enumerate(full_words):
        result = regex_checker(regex['regex_isi'], word)
        checkAgain = re.findall('(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember|jan|feb|mar|apr|may|jun|jul|aug|sept|sep|okt|nov|des)', word)
        if result is not None:
            tanggal.append(result)
        if len(checkAgain) > 0:
            left = ''
            right = ''
            if re.match('([0-9]|[0-3][0-9])',full_words[i-1]):
                left = full_words[i-1]
            if re.match('([0-9]|[0-3][0-9])',full_words[i+1]):
                right = full_words[i+1]
            tanggalTemp = left + ' ' + word + ' ' + right
            result2 = regex_checker(regex['regex_isi'], tanggalTemp)
            if result2 is not None:
                tanggal.append(result2)

nominal = ""
rekening = ""
pemilik_rek = ""

pangkat = ""
jabatan = ""
jurusan = ""
semester = ""
tahun_akademik = ""

if(document_type == 'bukti transfer digital'):
    for i, word in enumerate(full_words):
        if(re.match('(\d{2}\/\d{2})',word)):
            tanggal = word + ' ' + full_words[i+1]
        if(word == 'rp'):
            nominal = full_words[i+1]
        if(word == 'ke'):
            pemilik_rek = full_words[i+1]
        if(re.match('(\d){10,}',word)):
            rekening = word
        # if(word == '')
        # if(re.match('(\d{2}\/\d{2})',word)):

if(document_type == 'surat tugas individu'):
    document_type = 'surat tugas mengajar'
    for i, word in enumerate(full_words):
        if(word == 'ruang' and re.match(':', full_words[i+1])):
            pangkat = full_words[i+2] + ' ' +  full_words[i+3] + ' ' +  full_words[i+4] + ' ' +  full_words[i+5]
        if(word == 'fungsional' and re.match(':', full_words[i+1])):
            jabatan = full_words[i+2] + ' ' +  full_words[i+3]
        if(word == 'studi' and re.match(':', full_words[i+1])):
            jurusan = full_words[i+2] + ' ' + full_words[i+3]
        if(word == 'semester'):
            semester = full_words[i+1]
        if(word == 'tahun' and full_words[i+1] == "akademik"):
            tahun_akademik = full_words[i+2]

temp_nomor = re.sub(' ', '',' '.join(nomor_surat))
temp_tanggal = ' '.join(tanggal)

filepath = "test.jpeg"
# filepath = sys.argv[1]
file_name = os.path.basename(filepath)

text_file = []
# if(document_type != ""):
# if(file_name != ""):
#     text_file.append({"file_name": file_name})
# if(nama_dosen_final != ""):
#     text_file.append({"nama_dosen_final": nama_dosen_final})
# if(temp_nomor != ""):
#     text_file.append({"nomor": temp_nomor})
# if(' '.join(tanggal) != ""):
#     text_file.append({"tanggal": temp_tanggal})
# if(nominal != ""):
#     text_file.append({"nominal": nominal})
# if(rekening != ""):
#     text_file.append({"rekening": rekening})
# if(pemilik_rek != ""):
#     text_file.append({"pemilik_rek": pemilik_rek})
# if(pangkat != ""):
#     text_file.append({"pangkat": pangkat})
# if(jabatan != ""):
#     text_file.append({"jabatan": jabatan})
# if(jurusan != ""):
#     text_file.append({"jurusan": jurusan})
# if(semester != ""):
#     text_file.append({"semester": semester})
# if(tahun_akademik != ""):
#     text_file.append({"tahun_akademik": tahun_akademik})
nama_dosen_haha = ""
for i, item in enumerate(nama_dosen_final):
    nama_dosen_haha += '{"nama_dosen":"'+item['nama_dosen']+'",'
    nama_dosen_haha += '"bobot":"'+str(item['bobot'])+'",'
    nama_dosen_haha += '"nip":"'+item['nip']+'",'
    nama_dosen_haha += '"nidn":"'+item['nidn']+'"}'
    if(len(nama_dosen_final) > 1 and i+1 != len(nama_dosen_final)):
        nama_dosen_haha += ','

print('{"doc_type":"'+document_type+'",'+
        '"file_name":"'+file_name+'",'+
        '"nama_dosen":['+nama_dosen_haha+'],'+
        '"nomor":"'+temp_nomor+'",'+
        '"tanggal":"'+temp_tanggal+'",'+
        '"nominal":"'+nominal+'",'+
        '"rekening":"'+rekening+'",'+
        '"pemilik_rek":"'+pemilik_rek+'",'+
        '"pangkat":"'+pangkat+'",'+
        '"jabatan":"'+jabatan+'",'+
        '"jurusan":"'+jurusan+'",'+
        '"semester":"'+semester+'",'+
        '"tahun_akademik":"'+tahun_akademik+'"}')


# Create input for text file
# text_file.append("\nfilename: "+file_name)
# text_file.append("\ndoc_type: "+document_type)
# for item in nama_dosen_final:
#     # if(len(item)>0):
#     text_file.append("\n\tnama_dosen: "+item['nama_dosen'])
#     text_file.append("\n\tbobot: "+str(item['bobot']))
#     text_file.append("\n\tnip: "+item['nip'])
#     text_file.append("\n\tnidn: "+item['nidn'])
# text_file.append("\nnomor: " + re.sub(' ', '',' '.join(nomor_surat)))
# text_file.append("\ntanggal:" + ' '.join(tanggal))
# if(nominal != ""):
#     text_file.append("nominal:" +nominal)
# if(rekening != ""):
#     text_file.append("rekening:" +rekening)
# if(pemilik_rek != ""):
#     text_file.append("pemilik_rek:" +pemilik_rek)
# if(pangkat != ""):
#     text_file.append("pangkat: " +pangkat)
# if(jabatan != ""):
#     text_file.append("jabatan: " +jabatan)
# if(jurusan != ""):
#     text_file.append("jurusan: " +jurusan)
# if(semester != ""):
#     text_file.append("semester: " +semester)
# if(tahun_akademik != ""):
#     text_file.append("tahun_akademik: " +tahun_akademik)


# Create output to python print
# print("filename: "+file_name)
# print("doc_type: "+document_type)
# for item in nama_dosen_final:
#     # if(len(item)>0):
#     print("\tnama_dosen: "+item['nama_dosen'])
#     print("\tbobot: "+str(item['bobot']))
#     print("\tnip: "+item['nip'])
#     print("\tnidn: "+item['nidn'])
# print("nomor:" + re.sub(' ', '',' '.join(nomor_surat)))
# print("tanggal:" + ' '.join(tanggal))
# if(nominal != ""):
#     print("nominal:" +nominal)
# if(rekening != ""):
#     print("rekening:" +rekening)
# if(pemilik_rek != ""):
#     print("pemilik_rek:" +pemilik_rek)
# if(pangkat != ""):
#     print("pangkat: " +pangkat)
# if(jabatan != ""):
#     print("jabatan: " +jabatan)
# if(jurusan != ""):
#     print("jurusan: " +jurusan)
# if(semester != ""):
#     print("semester: " +semester)
# if(tahun_akademik != ""):
#     print("tahun_akademik: " +tahun_akademik)


# f = open("../routes/output_py/"+file_name+".txt", "w")
# f.writelines(text_file)
# f.close()

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

