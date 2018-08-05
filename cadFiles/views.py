from django.shortcuts import render
from django.shortcuts import render,redirect, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.files.uploadedfile import *
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib import messages 
from extractionTools.pdfTextExtractor2 import extract_text, savePdfText, extractImage, extractDxfEntities
from django.core.files.storage import default_storage
import os, csv
from dataExtraction.settings import MEDIA_ROOT
from django.http import FileResponse, Http404
from cadFiles.models import Document, PdfText, PdfImage, DxfDocument, DxfCsvDocument, DxfTextDocument
from django.urls import reverse



# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'cadFiles/simple_upload.html', context=None)

def file_add(request):
    doc_type = request.POST.get("group1", '')
    print(doc_type)
    if request.method == 'POST' and request.FILES['myfile']:
        if doc_type == 'pdf':
            myfile = request.FILES['myfile']
            
            if myfile.name.endswith('.pdf'):
                doc = Document(document=myfile)
                doc.save()
                # fs = FileSystemStorage()
                # filename = fs.save(myfile.name, myfile)
                # uploaded_file_url = fs.url(filename)
                # textData = savePdfText(myfile)
                # extractImage(myfile)
                # this_file_path = MEDIA_ROOT + "\\" + myfile.name
                # print(this_file_path)
                return HttpResponseRedirect(reverse('files'))

        if doc_type == 'dxf':
            myfile = request.FILES['myfile']
            print(myfile.name)
            if myfile.name.endswith('.dxf'):
                doc = DxfDocument(document=myfile)
                doc.save()
                # fs = FileSystemStorage()
                # filename = fs.save(myfile.name, myfile)
                return HttpResponseRedirect(reverse('files'))
        else:
            messages.error(request, 'It is not a text file.')
        return render(request, 'cadFiles/simple_upload.html', {'message': 'Please select an option for pdf or dxf file.'})
        
    return render(request, 'cadFiles/simple_upload.html')

def DocumentView(request):
    # return HttpResponse('Hello from posts.')
    pdfdoc = Document.objects.all()[:10]
    dxfdoc = DxfDocument.objects.all()[:10]

    context = {
        "pdfFiles": pdfdoc,
        "dxfFiles": dxfdoc
    }
    return render(request, 'cadFiles/index.html', context)

def deletePdfFile(request, id):
    doc = Document.objects.all()[:10]
    getDocument = Document.objects.get(id=id)
    documentPath = getDocument.document.path
    delFromPdfText = PdfText.objects.all()
    delFromPdfImage = PdfImage.objects.all()

    if delFromPdfText:
        if getDocument.id in [id.pdfDoc_id for id in delFromPdfText]:
            getPdfTextDoc = PdfText.objects.get(pdfDoc_id=id)
            pdfTextDocPath = getPdfTextDoc.textFile.path
            if getPdfTextDoc.pdfDoc_id == getDocument.id:
                getPdfTextDoc.delete()
                os.remove(pdfTextDocPath)

    if delFromPdfImage:
        if getDocument.id in [id.pdfDoc_id for id in delFromPdfImage]:
            getPdfImageDoc = PdfImage.objects.filter(pdfDoc_id=getDocument.id)
            for i in getPdfImageDoc:
                print(i.imageFile.path)
                pdfImageDocPath = i.imageFile.path
                os.remove(pdfImageDocPath)
            getPdfImageDoc.delete()
            getDocument.delete()
            os.remove(documentPath)
    else:
        getDocument.delete()
        os.remove(documentPath)
    return HttpResponseRedirect(reverse('files'))

def deleteDxfFile(request, id):
    doc = DxfDocument.objects.all()[:10]
    getDocument = DxfDocument.objects.get(id=id)
    DxfDocpath = getDocument.document.path

    delFromDxfCsv = DxfCsvDocument.objects.get(dxfCsv_id = id)
    delFromDxfText = DxfTextDocument.objects.get(dxfText_id = id)

    if delFromDxfCsv:
        if getDocument.id == delFromDxfCsv.dxfCsv_id:
            csvPath = delFromDxfCsv.dxfCsvName.path
            os.remove(csvPath)
            delFromDxfCsv.delete()

    if delFromDxfText:
        if getDocument.id == delFromDxfText.dxfText_id:
            txtPath = delFromDxfText.dxfTextName.path
            os.remove(txtPath)
            delFromDxfText.delete()
            getDocument.delete()
            os.remove(DxfDocpath)
    else:
        getDocument.delete()
        os.remove(DxfDocpath)
    return HttpResponseRedirect(reverse('files'))


def details(request, id):
    doc = Document.objects.get(id=id)
    context = {
        'file': doc
    }
    return render(request, 'cadFiles/details.html', context)

def pdfExtract(request, id):
    doc = Document.objects.get(id=id)
    extText = savePdfText(doc.document, docid=id)
    extImage = extractImage(doc.document, docid=id)

    pdfdoc = Document.objects.all()[:10]
    dxfdoc = DxfDocument.objects.all()[:10]

    context = {
        "pdfFiles": pdfdoc,
        "dxfFiles": dxfdoc
    }
    return render(request, 'cadFiles/index.html', context)

def viewImages(request, id):
    doc = PdfImage.objects.filter(pdfDoc_id=id)
    context = {
        'item': doc
    }
    return render(request, 'cadFiles/viewImages.html', context)

def viewPdfText(request, id):
    doc = PdfText.objects.get(pdfDoc_id=id)
    path = doc.textFile.path
    f = open(path, 'r', encoding='utf-8')
    data = f.read()
    context = {
        'pdfText': data
    }
    return render(request, 'cadFiles/viewPdfText.html', context)

def dxfExtract(request, id):
    doc = DxfDocument.objects.get(id=id)
    extDxfData = extractDxfEntities(doc.document, docid=id)

    pdfdoc = Document.objects.all()[:10]
    dxfdoc = DxfDocument.objects.all()[:10]

    context = {
        "pdfFiles": pdfdoc,
        "dxfFiles": dxfdoc
    }
    return render(request, 'cadFiles/index.html', context)

import pandas as pd
from django_tables2.tables import Table
from tabulate import tabulate

def showText(request, id):
    doc = DxfTextDocument.objects.get(dxfText_id=id)
    filepath = doc.dxfTextName.path

    f = open(filepath, 'r', encoding='utf-8')
    file_content = f.read()
    f.close()
    context = {
    'dxfText': file_content
    }
    return render(request, 'cadFiles/viewPdfText.html', context)

def showCsv(request, id):

    csvDoc = DxfCsvDocument.objects.get(dxfCsv_id = id)
    data = pd.read_csv(csvDoc.dxfCsvName.path)

    f = open(csvDoc.dxfCsvName.path, 'r')
    reader = csv.DictReader(f)

    # data = [r for r in reader1]

    df_table = data.to_dict(orient='dict')
    print(type(df_table))
    for row in df_table:
        print(df_table.get('X'))

    context = {
    'tableX': df_table.get('X').values,
    'tableY': df_table.get('Y').values
    }
    return render(request, 'cadFiles/viewPdfText.html', context)
    
    





