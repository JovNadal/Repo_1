from rest_framework import serializers
from .models import PDFDocument, ExtractedText

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['id', 'title', 'file', 'uploaded_at', 'page_count', 'processed']
        read_only_fields = ['id', 'uploaded_at', 'page_count', 'processed']

class ExtractedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedText
        fields = ['document', 'content', 'extracted_at']
        read_only_fields = ['extracted_at']