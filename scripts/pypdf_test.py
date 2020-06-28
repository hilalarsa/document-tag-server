
# importing required modules 
from PyPDF2 import PdfFileReader
import nltk


def pdf_to_text(filePath, filename):
    # creating a pdf file object 
    # print(result)
    pdfFileObj = open(filePath, 'rb') 
    # creating a pdf reader object 
    pdfReader = PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file 

    # creating a page object 
    pageObj = ""
    try:
        pageObj = pdfReader.getPage(1) 
        pass
    except Exception:
        pass

    if(len(pageObj)>0):
        result = pageObj.extractText()
        pdfFileObj.close()
        return result
    else:
        pass


# print(pdf_to_text('../sample/other/test2.pdf', 'ching chong'))