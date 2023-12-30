from django.shortcuts import render, redirect
from .forms import UploadPDFForm
from django.conf import settings
from django.http import HttpResponse
import os
import PyPDF2
from zipfile import ZipFile

def split_pdf(input_pdf, output_folder):
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Split PDF into separate pages
        for page_number in range(len(pdf_reader.pages)):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_number])
            
            # Save each page as a separate PDF
            output_page_path = os.path.join(output_folder, f'page_{page_number + 1}.pdf')
            with open(output_page_path, 'wb') as output_page_file:
                pdf_writer.write(output_page_file)

def create_zip(folder_path, zip_file):
    with ZipFile(zip_file, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def process_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']

            # Set the paths
            input_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
            output_folder_path = os.path.join(settings.MEDIA_ROOT, 'output_pages')
            zip_file_path = os.path.join(settings.MEDIA_ROOT, 'output.zip')

            # Save the uploaded PDF
            with open(input_pdf_path, 'wb') as pdf_upload:
                for chunk in pdf_file.chunks():
                    pdf_upload.write(chunk)

            # Process the PDF
            split_pdf(input_pdf_path, output_folder_path)
            create_zip(output_folder_path, zip_file_path)

            # Provide the ZIP file for download
            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_file_path)}'
            
            with open(zip_file_path, 'rb') as zip_file:
                response.write(zip_file.read())

            return response
    else:
        form = UploadPDFForm()

    return render(request, 'process_pdf.html', {'form': form})
