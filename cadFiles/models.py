from django.db import models

# Create your models here.
class Document(models.Model):
    # description = models.CharField(max_length=255, blank=True)
    document = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PdfText(models.Model):
    textFile = models.FileField(upload_to='media/pdfStore', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pdfDoc = models.ForeignKey(Document, on_delete=models.CASCADE)

class PdfImage(models.Model):
    imageFile = models.ImageField(upload_to='media/imageStore', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pdfDoc = models.ForeignKey(Document, on_delete=models.CASCADE)


class DxfDocument(models.Model):
    document = models.FileField()
    dxfVesion = models.CharField(max_length=100)
    header_var_count = models.IntegerField(default=0)
    layer_count = models.IntegerField(default=0)
    block_definition_count = models.IntegerField(default=0)
    entity_count = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DxfCsvDocument(models.Model):
    dxfCsvName = models.FileField(upload_to='media/dxfStore', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dxfCsv = models.ForeignKey(DxfDocument, on_delete=models.CASCADE)

class DxfTextDocument(models.Model):
    dxfTextName = models.FileField(upload_to='media/dxfStore', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dxfText = models.ForeignKey(DxfDocument, on_delete=models.CASCADE)

