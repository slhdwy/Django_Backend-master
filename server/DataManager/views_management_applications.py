from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class GetAvailableJar(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'GetAvailableJar'})

class UploadJar(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'UploadJar'})

class RunJar(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'RunJar'})