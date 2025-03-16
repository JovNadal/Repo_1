from django.db import models
import os
import uuid


class PDFDocument(models.Model):
    """Model to store uploaded PDF financial statements"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    page_count = models.IntegerField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class ExtractedText(models.Model):
    """Model to store text extracted from PDF documents"""
    document = models.OneToOneField(PDFDocument, on_delete=models.CASCADE, related_name='extracted_text')
    content = models.JSONField(help_text="JSON structure containing extracted text by page")
    extracted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Extracted text from {self.document.title}"