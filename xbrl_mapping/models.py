from django.db import models

# Create your models here.
from django.db import models
from pdf_extraction.models import PDFDocument, ExtractedText
import uuid


class MappingJob(models.Model):
    """Model to track mapping jobs"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='mapping_jobs')
    extracted_text = models.ForeignKey(ExtractedText, on_delete=models.CASCADE, related_name='mapping_jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Mapping job {self.id} - {self.document.title} ({self.status})"


class XBRLMapping(models.Model):
    """Model to store mapped XBRL data"""
    job = models.OneToOneField(MappingJob, on_delete=models.CASCADE, related_name='xbrl_mapping')
    filing_information = models.JSONField()
    financial_position = models.JSONField()
    income_statement = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"XBRL Mapping for {self.job.document.title}"