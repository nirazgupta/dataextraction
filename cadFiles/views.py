from django.shortcuts import render
from django.shortcuts import render,redirect, render_to_response, get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.files.uploadedfile import *
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib import messages 
from extractionTools.pdfTextExtractor2 import extract_text, savePdfText, extractImage, extractDxfEntities, pdfToTable
from django.core.files.storage import default_storage
import os, csv
from dataExtraction.settings import MEDIA_ROOT
from django.http import FileResponse, Http404
from cadFiles.models import Document, PdfText, PdfImage, DxfDocument, DxfCsvDocument, DxfTextDocument, PdfCsv
from django.urls import reverse
import pandas as pd
from django_tables2.tables import Table
from tabulate import tabulate
import pyexcel as p
import django_excel as excel



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
                return HttpResponseRedirect(reverse('pdffiles'))

        if doc_type == 'dxf':
            myfile = request.FILES['myfile']
            print(myfile.name)
            if myfile.name.endswith('.dxf'):
                doc = DxfDocument(document=myfile)
                doc.save()
                return HttpResponseRedirect(reverse('dxffiles'))
        else:
            messages.error(request, 'It is not a text file.')
        return render(request, 'cadFiles/simple_upload.html', {'message': 'Please select an option for pdf or dxf file.'})
        
    return render(request, 'cadFiles/simple_upload.html')

    
def PdfView(request):
    pdfdoc = Document.objects.all()[:10]

    context = {
        "pdfFiles": pdfdoc,
    }
    return render(request, 'cadFiles/file_list.html', context)

def DxfView(request):
    dxfdoc = DxfDocument.objects.all()[:10]
    context = {
        "dxfFiles": dxfdoc
    }
    return render(request, 'cadFiles/file_list.html', context)

def deletePdfFile(request, id):
    getDocument = Document.objects.get(id=id)
    documentPath = getDocument.document.path

    getDocument.delete()
    os.remove(documentPath)
    return HttpResponseRedirect(reverse('pdffiles'))

def deleteDxfFile(request, id):
    getDocument = DxfDocument.objects.get(id=id)
    DxfDocpath = getDocument.document.path
    
    getDocument.delete()
    os.remove(DxfDocpath)
    return HttpResponseRedirect(reverse('dxffiles'))


def details(request, id):
    doc = Document.objects.get(id=id)
    context = {
        'file': doc
    }
    return render(request, 'cadFiles/details.html', context)


def viewImages(request, id):
    if PdfImage.objects.filter(pdfDoc_id=id).exists():
        doc = PdfImage.objects.filter(pdfDoc_id=id)
        context = {
            'item': doc
        }
        return render(request, 'cadFiles/viewImages.html', context)
    else:
        context = {
            'pdfText': 'Please extract the file first.'
        }
        return render(request, 'cadFiles/viewImages.html', context)

def viewPdfText(request, id):
    if PdfText.objects.filter(pdfDoc_id=id).exists(): 
        doc = PdfText.objects.get(pdfDoc_id=id)
        path = doc.textFile.path
        f = open(path, 'r', encoding='utf-8')
        data = f.read()
        context = {
            'pdfText': data
        }
        return render(request, 'cadFiles/viewPdfText.html', context)
    else:
        context = {
            'pdfText': 'Please extract the file first.'
        }
        return render(request, 'cadFiles/viewPdfText.html', context)

def viewPdfCsv(request, id):
    doc = Document.objects.get(id=id)
    pdfToTable(doc.document, docid=id)

    csvDoc = PdfCsv.objects.get(csvDoc_id = id)
    if PdfCsv.objects.filter(csvDoc_id = id).exists():
        path = csvDoc.csvFile.path
        f = open(path, 'r')

        csvRead = csv.reader(f, delimiter=",")
        data = [i for i in csvRead]

        filename = os.path.basename(path)
        sheet = excel.pe.Sheet(data)
        return excel.make_response_from_array(sheet, "csv", file_name=filename)


def pdfExtract(request, id):
    doc = Document.objects.get(id=id)
    savePdfText(doc.document, docid=id)
    extractImage(doc.document, docid=id)
    
    return HttpResponseRedirect(reverse('pdffiles'))

def dxfExtract(request, id):
    doc = DxfDocument.objects.get(id=id)
    extractDxfEntities(doc.document, docid=id)
    return HttpResponseRedirect(reverse('dxffiles'))

def showText(request, id):
    if DxfTextDocument.objects.filter(dxfText_id=id).exists():
        doc = DxfTextDocument.objects.get(dxfText_id=id)
        filepath = doc.dxfTextName.path

        f = open(filepath, 'r', encoding='utf-8')
        file_content = f.read()
        f.close()
        context = {
        'dxfText': file_content
        }
        return render(request, 'cadFiles/viewPdfText.html', context)
    else:
        context = {
        'dxfText': 'Please extract the file first.'
        }
        return render(request, 'cadFiles/viewPdfText.html', context)

def showCsv(request, id):
    if DxfCsvDocument.objects.filter(dxfCsv_id = id).exists():
        csvDoc = DxfCsvDocument.objects.get(dxfCsv_id = id)
        data = pd.read_csv(csvDoc.dxfCsvName.path)
        df_table = data.to_dict(orient='dict')

        context = {
        'tableX': df_table.get('X').values,
        'tableY': df_table.get('Y').values
        }
        return render(request, 'cadFiles/viewPdfText.html', context)
    return HttpResponseRedirect(reverse('dxffiles'))
    
    





