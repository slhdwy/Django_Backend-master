from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
import MySQLdb
import json
# Create your views here.
class JobManagement(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        #
        #include method here
        #
        Con=MySQLdb.connect(host='localhost',user='pangu',passwd='pangu',db='nagios')
        cursor=Con.cursor()
        aa=cursor.execute("select * from pangu_service where HostName='client9'")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        for ii in info:
            data = {}
            data['ServiceName'] = ii[0]
            data['HostName'] = ii[1]
            data['LastCheck'] = ii[2]
            data['PerformanceData'] = ii[3]
            data['PluginOutput'] = ii[4]
            data['Attempt'] = ii[5]
            data['Duration'] = ii[6]
            data['HostId'] = ii[7]
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")
