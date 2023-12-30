from django.urls import path, include
from pdfhandler import views

urlpatterns = [
        path('',views.process_pdf, name="process_pdf"),
]