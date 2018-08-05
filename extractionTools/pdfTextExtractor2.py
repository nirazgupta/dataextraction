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
import fitz, csv
import sys, time, re
import PyPDF2
import requests 
from django.http import HttpResponse
from cadFiles.models import PdfText, PdfImage, DxfDocument, DxfCsvDocument, DxfTextDocument
from os.path import join
from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from urllib.parse import urlparse
import dxfgrabber
from django.core.files.temp import NamedTemporaryFile
from base64 import b64encode

# Get the name of file from path by using split
def extension(file):
        name, extension = os.path.splitext(file.name)
        return name

# This function extracts the text from the supplied pdf file and returns the extracted text
def extract_text(doc):
    password = ""
    extracted_text = ""

    # Open the file in binary mode
    fp = doc.open(mode='rb')

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

# Scans and extracts images from pdf file
def extractImage(myfile, docid):
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
            pix.writePNG(dest_file + "img-%s.png" % (i,))    
            path = join(MEDIA_ROOT, 'imageStore',  "img-%s.png" % (i,))

            file = PdfImage()
            file.pdfDoc_id = docid
            file.imageFile = path 
            file.save()
        else:                              # must convert the CMYK first
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG("img-%s.png" % (i,))

            path = join(MEDIA_ROOT, 'imageStore',  "img-%s.png" % (i,))

            file = PdfImage()
            file.pdfDoc_id = docid
            file.imageFile = path 
            file.save()
            pix0 = None  
        pix = None                         # free Pixmap resources
            
# writes the extracted text to a text file and returns content to the view.
def savePdfText(doc, docid):

    content = extract_text(doc)
    split = os.path.splitext(doc.name)
    fname =  split[0] + '.txt'

    path = join(MEDIA_ROOT, 'pdfStore', fname)
    print(path)
    f = open(path, "w", encoding='utf-8')

    #wipe the existing content
    f.truncate()
    f.write(content)
    # f.close()
    f = File(f)
    # filename = os.path.basename(path)
    file = PdfText()
    file.pdfDoc_id = docid
    file.textFile = path
    file.save()
    return content

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


# Extracts data points and text from the dxf file.
def extractDxfEntities(doc, docid):
    DEFAULT_OPTIONS = {
        "grab_blocks": True,
        "assure_3d_coords": False,
        "resolve_text_styles": True,
    }
    print(doc.name)
    split = os.path.splitext(doc.name)

    fnameCsv =  split[0] + '.csv'
    fnameTxt=  split[0] + '.txt'
    print(fnameCsv)
    # fp = doc.open(mode='rb')
    # print(type(fp))
    dxf = dxfgrabber.readfile(doc.path, DEFAULT_OPTIONS)
   
    dxfVesion  = "DXF version: {}".format(dxf.dxfversion) 
    header_var_count = len(dxf.header) # dict of dxf header vars
    layer_count = len(dxf.layers) # collection of layer definitions
    block_definition_count = len(dxf.blocks) # dict like collection of block definitions
    entity_count = len(dxf.entities) # list like collection of entities


    output = [entity for entity in dxf.entities if entity.layer == '0']

    text = [entity.plain_text(split=False) for entity in output if entity.dxftype == 'MTEXT']

    dest_file = MEDIA_ROOT + r'\dxfStore\\'
    if not os.path.exists(dest_file):
        os.makedirs(dest_file)

    csvPath = join(MEDIA_ROOT, 'dxfStore', fnameCsv)
    txtPath = join(MEDIA_ROOT, 'dxfStore', fnameTxt)

    with open(csvPath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['X', 'Y'])
        for entity in output:
            if entity.dxftype == 'LWPOLYLINE':
                for row in entity.points:
                    writer.writerow(row)

    with open(txtPath, 'w', encoding='utf-8') as f2:
        for item in text:
            f2.write("%s\n" % item)
    
    
    dxfTextObj = DxfTextDocument()
    dxfCsvObj = DxfCsvDocument()
    dxfdoc = DxfDocument.objects.get(id=docid)

    dxfdoc.dxfVesion = dxfVesion
    dxfdoc.header_var_count = header_var_count
    dxfdoc.layer_count = layer_count
    dxfdoc.block_definition_count = block_definition_count
    dxfdoc.entity_count = entity_count
    dxfdoc.save()

    dxfCsvObj.dxfCsv_id = docid
    dxfCsvObj.dxfCsvName = csvPath
    dxfCsvObj.save()

    dxfTextObj.dxfText_id = docid
    dxfTextObj.dxfTextName = txtPath
    dxfTextObj.save()
