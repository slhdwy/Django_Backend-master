from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class StandardDatasetList(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'StandardDatasetList'})

class StandardDatasetsDetail(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'StandardDatasetsDetail'})

class StandardDatasetQuery(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'StandardDatasetQuery'})