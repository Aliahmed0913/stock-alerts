
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Alert, TriggeredAlert
from .serializers import AlertCreateSerializer, AlertReadSerializer, TriggeredAlertSerializer
from .permissions import IsOwner
# Create your views here.

class AlertViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
      
    def get_queryset(self):
        return Alert.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer:AlertCreateSerializer):
        serializer.save(user = self.request.user)
    
    @action(detail = False, methods = ['GET'], url_path ='triggered')
    def triggered_alerts(self, request):
        triggered = TriggeredAlert.objects.filter(alert__user = self.request.user)
        if triggered.exists():
            serializer = TriggeredAlertSerializer(triggered, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Not found':'There is no triggered alert yet.'},status=status.HTTP_404_NOT_FOUND)
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AlertCreateSerializer
        return AlertReadSerializer
