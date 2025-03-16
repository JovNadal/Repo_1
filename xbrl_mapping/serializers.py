from rest_framework import serializers
from .models import MappingJob, XBRLMapping


class MappingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappingJob
        fields = ['id', 'document', 'extracted_text', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class XBRLMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = XBRLMapping
        fields = ['id', 'job', 'filing_information', 'financial_position', 'income_statement', 'created_at']
        read_only_fields = ['id', 'created_at']