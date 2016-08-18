from rest_framework.views import APIView
from rest_framework.response import Response

#from pydoop.hdfs import hdfs
import json
import string
from django.http import HttpResponse
# Create your views here.
class OfflineApplicationLayerResults(APIView):
    def get(self, request, format=None):
        callback = request.GET.get('callback','logIt')
        data = {}
        time = []
        DNS = []
        HTTP = []
        NBNS = []
        RPC = []
        SNMP = []
        SSDP = []
        TELNET = []
        UNKNOW = []

        IP = "localhost"
        Port = 9000
        ResultDir = "/hduser/application_result/state1/1442246400000/bc-m-00000"
        minute = 60 * 1000
        hour = 60 * minute
        day = 24 * hour
        fs = hdfs(IP, Port)
        f = fs.open_file(ResultDir)
        line = f.readline()
        array = line.split('\t')

        while line:
            time.append(array[1])
            if array[2] == 'DNS' and line:
                DNS.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                DNS.append(0)

            if array[2] == 'HTTP' and line:
                HTTP.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                HTTP.append(0)

            if array[2] == 'NBNS' and line:
                NBNS.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                NBNS.append(0)

            if array[2] == 'RPC' and line:
                RPC.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                RPC.append(0)

            if array[2] == 'SNMP' and line:
                SNMP.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                SNMP.append(0)

            if array[2] == 'SSDP' and line:
                SSDP.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                SSDP.append(0)

            if array[2] == 'TELNET' and line:
                TELNET.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                TELNET.append(0)

            if array[2] == 'UNKNOW' and line:
                UNKNOW.append(string.atoi(array[3].split('\n')[0]))
                line = f.readline()
                array = line.split('\t')
            else:
                UNKNOW.append(0)

        data['TIME'] = time
        data['DNS'] = DNS
        data['HTTP'] = HTTP
        data['NBNS'] = NBNS
        data['RPC'] = RPC
        data['SNMP'] = SNMP
        data['TELNET'] = TELNET
        data['UNKNOW'] = UNKNOW
        D = '%s(%s)'%(callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")


class OfflineTransportLayerResults(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'OfflineTransportLayerResults'})

class OfflineNetworkLayerResults(APIView):
    def get(self, request, format=None):
        #
        #include method here
        #
        return Response({'Response':'OfflineNetworkLayerResults'})
