from rest_framework.response import Response
from rest_framework import viewsets,status


from .serializers import *


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return VehicleGetSerializer
        return VehicleSerializer

class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()

class VehicleAllocationViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleAllocationSerializer
    queryset = VehicleAllocation.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return VehicleAllocationGetSerializer
        return VehicleAllocationSerializer

