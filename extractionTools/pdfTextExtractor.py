from __future__ import print_function
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
from dataExtraction.settings import MEDIA_ROOT
import fitz
import sys, time, re
import PyPDF2
import requests 
from django.http import HttpResponse

def extension(file):
        name, extension = os.path.splitext(file.name)
        return name

def extract_text(pdfFilePath):
    password = ""
    extracted_text = ""

    # Open the file in binary mode
    fp = open(pdfFilePath, "rb")

    # Create parser object on the pdf content 
    parser = PDFParser(fp)

    document = PDFDocument(parser, password)

    # verify if docoment is extracttable 
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()

    # set parameters for analysis
    laparams = LAParams()

    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
                
    #close the pdf file
    fp.close()
    return extracted_text


def extractImage(myfile):
    checkXO = r"/Type(?= */XObject)"       # finds "/Type/XObject"   
    checkIM = r"/Subtype(?= */Image)"      # finds "/Subtype/Image"

    this_file_path = MEDIA_ROOT + "/" + myfile.name

    dest_file = MEDIA_ROOT + r'\imageStore\\'
    if not os.path.exists(dest_file):
        os.makedirs(dest_file)

    doc = fitz.open(this_file_path)
    imgcount = 0
    lenXREF = doc._getXrefLength()         # number of objects - do not use entry 0!

    for i in range(1, lenXREF):            # scan through all objects
        text = doc._getObjectString(i)     # string defining the object
        isXObject = re.search(checkXO, text)    # tests for XObject
        isImage   = re.search(checkIM, text)    # tests for Image
        if not isXObject or not isImage:   # not an image object if not both True
            continue
        imgcount += 1
        pix = fitz.Pixmap(doc, i)          # make pixmap from image
        if pix.n < 5:                      # can be saved as PNG
            pix.writePNG(dest_file + extension(myfile) + "-" + "img-%s.png" % (i,))
        else:                              # must convert the CMYK first
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(dest_file +  extension(myfile) + "-" + "img-%s.png" % (i,))
            pix0 = None                    # free Pixmap resources
        pix = None                         # free Pixmap resources
            
    t1 = time.clock()

# def pdfToTable(myfile):
#     this_file_path = MEDIA_ROOT + "/" + myfile.name
#     fileData = (this_file_path, open(this_file_path, 'rb')) #"rb" stands for "read bytes"
#     files = {'f': fileData} 
#     apiKey = "88sfqs4nmin1" 
#     fileExt = "csv" #format/file extension of final document
#     postUrl = "https://pdftables.com/api?key={0}&format={1}".format(apiKey, fileExt)
#     #the .format puts value of apiKey where {0} is, etc
#     response = requests.post(postUrl, files=files)
#     response.raise_for_status() # ensure we notice bad responses
#     downloadDir = "D:\\autocad\\example1.csv" #directory where you want your file downloaded to 
#     with open(downloadDir, "wb") as f:
#         f.write(response.content) #write data to csv
#     return response.content

def savePdfText(myfile):
    this_file_path = MEDIA_ROOT + "\\" + myfile.name
    dest_file = MEDIA_ROOT + r'\pdfStore'
    if not dest_file:
        os.mkdir(dest_file)
    content = extract_text(this_file_path)
    destFileName = dest_file + "\\" + extension(myfile) + '.txt'

    f = open(destFileName, 'w', encoding='utf-8')
    f.write(content)
    f.close()

    my_file =  open(destFileName, 'r', encoding='utf-8') 
    response = HttpResponse(my_file.read(), mimetype='text/plain')
    response['Content-Disposition'] = 'inline;filename=some_file.txt'
    return response


