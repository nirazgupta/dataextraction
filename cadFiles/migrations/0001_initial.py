# Generated by Django 2.0.7 on 2018-08-05 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DxfCsvDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dxfCsvName', models.FileField(blank=True, upload_to='media/dxfStore')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DxfDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='')),
                ('dxfVesion', models.CharField(max_length=100)),
                ('header_var_count', models.IntegerField(default=0)),
                ('layer_count', models.IntegerField(default=0)),
                ('block_definition_count', models.IntegerField(default=0)),
                ('entity_count', models.IntegerField(default=0)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DxfTextDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dxfTextName', models.FileField(blank=True, upload_to='media/dxfStore')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dxfText', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadFiles.DxfDocument')),
            ],
        ),
        migrations.CreateModel(
            name='PdfImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageFile', models.ImageField(blank=True, upload_to='media/imageStore')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pdfDoc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadFiles.Document')),
            ],
        ),
        migrations.CreateModel(
            name='PdfText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textFile', models.FileField(blank=True, upload_to='media/pdfStore')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pdfDoc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadFiles.Document')),
            ],
        ),
        migrations.AddField(
            model_name='dxfcsvdocument',
            name='dxfCsv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadFiles.DxfDocument'),
        ),
    ]
