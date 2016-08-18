from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
import MySQLdb
import json
# Create your views here.
class centosdisk7(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        #
        #include method here
        #
        Con=MySQLdb.connect(host='localhost',user='pangu',passwd='pangu',db='nagios')
        cursor=Con.cursor()
        aa=cursor.execute("select * from pangu_service where HostName = 'client7' and ServiceName = 'centosdisk'")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        for ii in info:
            data = {}
            data['LastCheck'] = ii[2]
            data['PluginOutput'] = ii[4]
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

class centosdisk8(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        #
        #include method here
        #
        Con=MySQLdb.connect(host='localhost',user='pangu',passwd='pangu',db='nagios')
        cursor=Con.cursor()
        aa=cursor.execute("select * from pangu_service where HostName = 'client8' and ServiceName = 'centosdisk'")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        for ii in info:
            data = {}
            data['LastCheck'] = ii[2]
            data['PluginOutput'] = ii[4]
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

class centosdisk9(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        #
        #include method here
        #
        Con=MySQLdb.connect(host='localhost',user='pangu',passwd='pangu',db='nagios')
        cursor=Con.cursor()
        aa=cursor.execute("select * from pangu_service where HostName = 'client9' and ServiceName = 'centosdisk'")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        for ii in info:
            data = {}
            data['LastCheck'] = ii[2]
            data['PluginOutput'] = ii[4]
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

class centosdisk10(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        #
        #include method here
        #
        Con=MySQLdb.connect(host='localhost',user='pangu',passwd='pangu',db='nagios')
        cursor=Con.cursor()
        aa=cursor.execute("select * from pangu_service where HostName = 'client10' and ServiceName = 'centosdisk'")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        for ii in info:
            data = {}
            data['LastCheck'] = ii[2]
            data['PluginOutput'] = ii[4]
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

class centosdisk(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        #
        #include method here
        #
        Con=MySQLdb.connect(host='localhost',user='pangu',passwd='pangu',db='nagios')
        cursor=Con.cursor()
        aa=cursor.execute("select * from pangu_service where ServiceName = 'centosdisk' order by LastCheck desc limit 4")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        for ii in info:
            data = {}
            data['LastCheck'] = ii[2]
            data['PluginOutput'] = ii[4]
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

