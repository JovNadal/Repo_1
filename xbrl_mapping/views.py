from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MappingJob, XBRLMapping
from .serializers import MappingJobSerializer, XBRLMappingSerializer


class MappingJobViewSet(viewsets.ModelViewSet):
    queryset = MappingJob.objects.all()
    serializer_class = MappingJobSerializer
    
    @action(detail=True, methods=['post'])
    def start_mapping(self, request, pk=None):
        mapping_job = self.get_object()
        
        # Check if job is already completed or in progress
        if mapping_job.status in ['completed', 'processing']:
            return Response(
                {"message": f"Mapping job is already {mapping_job.status}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update job status to processing
        mapping_job.status = 'processing'
        mapping_job.save()
        