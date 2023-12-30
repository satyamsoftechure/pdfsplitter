from django import forms

class UploadPDFForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')

    # border: coral;
    # border-style: dotted;
    # padding: 25px;
    # border-width: thick;
    # border-radius: 30px;
