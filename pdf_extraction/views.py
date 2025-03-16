from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PDFDocument, ExtractedText
from .serializers import PDFDocumentSerializer, ExtractedTextSerializer
from .services.pdf_extractor import PDFExtractor
import os
from django.conf import settings
import pdfplumber

class PDFDocumentViewSet(viewsets.ModelViewSet):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        # Count pages in the PDF
        try:
            with pdfplumber.open(instance.file.path) as pdf:
                instance.page_count = len(pdf.pages)
                instance.save()
        except Exception as e:
            instance.processing_error = str(e)
            instance.save()
    
    @action(detail=True, methods=['post'])
    def extract(self, request, pk=None):
        document = self.get_object()
        
        # Check if extraction already exists
        if hasattr(document, 'extracted_text'):
            return Response({"message": "Text already extracted for this document"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Extract text
            extractor = PDFExtractor(document.file.path)
            extracted_content = extractor.extract_text_with_pdfplumber()
            
            # Save extracted text
            extracted_text = ExtractedText.objects.create(
                document=document,
                content=extracted_content
            )
            
            # Mark document as processed
            document.processed = True
            document.save()
            
            serializer = ExtractedTextSerializer(extracted_text)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            document.processing_error = str(e)
            document.save()
            return Response(
                {"error": f"Failed to extract text: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )