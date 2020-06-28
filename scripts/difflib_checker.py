import difflib
from difflib import SequenceMatcher

import re

# sourceWord = ['kementerian', 'riset,', 'teknologi', 'dan', 'pendidikan', 'tinggi', 'politeknik', 'negeri', 'malang', 'jalan', 'soekarno', 'hatta', 'no.9', 'malang', '65141', 'telepon', '(0341)', '404424', '-', '404425.', 'fax', '(oja1)', '404420', 'sid', 'ti', 'surat', 'tugas', 'nomor:', '10116/pl2/kp/2019', 'direktur', 'politeknik', 'negeri', 'malang', 'memberi', 'tugas', 'kepada:', 'nama', 'peneliti', 'nidn', 'jabatan', 'putra', 'prima', 'arhandi,', 's.t.,', 'mkom', '0003118602', '\xe2\x80\x94', '|', 'ketua', 'luoman', 'affandi,', 's.kom.,', 'm.msi', '0730118201', 'anggota', 'dimas', 'wahyu', 'wibowo,', 's.t,', 'm.t', '0009108402', 'anggota', 'untuk', 'melaksanakan', 'kegiatan', 'penelitian', 'reguler', 'kompetisi', 'yang', 'dibiayai', 'dengan', 'dana', 'dipa', 'nomor:', 'sp', 'dipa-042.01-2401004/2019', 'dengan', 'surat', 'perjanjian', 'no:', '9675/pl2.1/hk/2019.', 'dengan', 'judul', ':', 'aplikasi', 'whatsapp', 'gateway', 'dengan', 'nomor', 'kontak', 'otomatis', 'untuk', 'notifikasi', 'surat', 'peringatan', 'mahasiswa', 'menggunakan', 'metode', 'mesin', 'turing', 'dan', 'rest', 'politeknik', 'negeri', 'malang', '1', 'april', 's/d', '31', 'oktober', '2019', 'tempat', 'pelaksanaan', 'waktu', 'pelaksanaan', 'demikian', 'surat', 'tugas', 'ini', 'dibuat', 'untuk', 'dilaksanakan', 'dengan', 'sebaik-baiknya.', 'setiawan,', 'mmt.,', 'mm', 'nip.1195909101986031002', 'tembusan:', '1.', 'pembantu', 'direktur', 'i:', '2.', 'pembantu', 'direktur', 'il:', '3.', 'ketua', 'jurusar/', 'program', 'studi', 'teknologi', 'informasi']
# dictFromApi = ['putra prima arhandi', 'luqman affandi', 'dimas wahyu wibowo']
# testedWord = 'kementrian'

# to check whether testedWord is inside sourceWord, return ratio and the word itself
def text_matcher(sourceWord, testedWord):
    result = [] # final result
    tempOutput = [] # temporary var to save output per name/word

    counter = 0
    for word in sourceWord:

        singleNameArray = testedWord.split() # get per name/rows from api
        
        partLength = len(singleNameArray) # save name length for checker start-end indicator 
        for singleName in singleNameArray: #get per name word from splitted name/row from api
            # print(part + " " + word)
            # n = 0 #set counter for end condition when n == nameLength
            seq = SequenceMatcher(a=word,b=singleName)
            
            # while n < partLength: # stop appending when reached end of each name
            if(seq.ratio() > 0.8): # if ratio is more than 80%, place data from api to output text
                # print(seq.ratio()) # sequence ratio
                tempOutput.append(singleName) # add singleName to tempOutput array to get outputed
                checkAgain = array_merge(tempOutput) # full string result after merged and match on each iteration
                seq2 = SequenceMatcher(a=testedWord,b=checkAgain) # check ratio AGAIN if each text in unmerged array is good enough
                
                if(seq2.ratio() > 0.8):
                    result = tempOutput # save output tempOutput and reset it
                    # output["nama_dosen"] = result
                    # output["ratio"] = seq.ratio()
                    tempOutput = [] # reset output
                    counter = counter + 1
                    break
                elif(len(tempOutput) >= partLength):
                    tempOutput = [] # reset output
    if(counter > 0):
        return {"text": array_merge(result), "counter": counter}


def text_matcher_dosen(sourceWord, testedWord):
    result = [] # final result
    tempOutput = [] # temporary var to save output per name/word
    counter = 0
    name_counter = 0
    nama_asli_dosen = sourceWord
    array_dosen = sourceWord.split()
    partLength = len(array_dosen)
    for single_name in array_dosen:
        # singleNameArray = testedWord.split() # get per name/rows from api
        
        # partLength = len(singleNameArray) # save name length for checker start-end indicator 
        # for singleName in singleNameArray: #get per name word from splitted name/row from api
            # n = 0 #set counter for end condition when n == nameLength
        seq = SequenceMatcher(a=single_name,b=testedWord)
        
        # while n < partLength: # stop appending when reached end of each name

        if(seq.ratio() > 0.8): # if ratio is more than 80%, place data from api to output text
            return single_name
    
def array_merge(array):
    limiter = ' '
    return limiter.join(array)

def get_document_type(source_word, judul_array):
    tipe_judul = judul_array['tipe_judul']
    trigger_word_array = judul_array['trigger_word'].split(', ')
    for item in trigger_word_array:
        if(source_word == item):
            return tipe_judul

def regex_checker(pattern, text):
    prog = re.compile(pattern)
    result = prog.match(text)
    if result:
        return result.group(0)