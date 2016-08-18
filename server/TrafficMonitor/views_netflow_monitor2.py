#coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from DataManager.models import dataset
from DataManager.models import datacolreq
from rest_framework.views import APIView
from django import forms
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import MySQLdb
import json
import datetime
import time

class netflow_monitor(APIView):

    def get(self, request, format=None):
        data = {}
        TIME = []
        VALUE = []
        VALUE0 = []
        VALUE1 = []
        VALUE2 = []
        VALUE3 = []
        VALUE4 = []

        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='netflow')
        cursor=Con.cursor()

        type = int(request.GET.get('type', 1))
        Period = int(request.GET.get('period', 288))

        if type == 1:
            Q_unit = 'sum(flows)/300'
        elif type == 2:
            Q_unit = 'sum(packets)/300'
        else:
            Q_unit = 'sum(bytes)*8/300'

        Q_period_all = ' limit '+str(Period)+';'
        Q_period = ' limit '+str(Period*4)+';'
        sql_all = "select timestamp, " + Q_unit + " from Netflow_Transport group by timestamp order by timestamp desc" + Q_period_all
        aa=cursor.execute(sql_all)
        info_all = cursor.fetchmany(aa)
	
        sql = "select timestamp, protocol, " + Q_unit + " from Netflow_Transport group by timestamp, protocol order by timestamp desc" + Q_period
        aa=cursor.execute(sql)
        info = cursor.fetchmany(aa)

        for ii in info_all[::-1]:
            TIME.append(time.strftime('%H:%M',time.localtime(ii[0])))
            VALUE0.append(int(ii[1]))

        for ii in info[::-1]:
            if ii[1] == 1:
                VALUE3.append(int(ii[2]))
            elif ii[1] == 2:
                VALUE1.append(int(ii[2]))
            elif ii[1] == 3:
                VALUE2.append(int(ii[2]))
            elif ii[1] == 4:
                VALUE4.append(int(ii[2]))

        VALUE.append(VALUE0)
        VALUE.append(VALUE1)
        VALUE.append(VALUE2)
        VALUE.append(VALUE3)
        VALUE.append(VALUE4)

        data['TIME'] = TIME
        data['VALUE'] = VALUE

        callback = request.GET.get('callback','logIt')
        D = '%s(%s)'%(callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")



class netflow_monitor_table(APIView):

    def get(self, request, format=None):
        data = {}
        #0:ALL, 1:THU, 2:PKU, 3:BUPT, 4:BUAA, 5:Fudan, 6:HUST, 7:Tongji 8:CQU  9:CSU 10: DLUT   11:HIT  12:JLU  13:LZU  14:NEU  15:SCUT  16:SDU  17:SEU  18:SJTU   19:TJU   20:UESTC  21:USTC  22:XJTU  23:XMU  24:ZJU  25:ZZU
        ROUTER = ['ALL', 'THU', 'PKU', 'BUPT', 'BUAA', 'Fudan', 'HUST', 'Tongji', 'CQU', 'CSU', 'DLUT', 'HIT', 'JLU', 'LZU', 'NEU', 'SCUT', 'SDU', 'SEU', 'SJTU', 'TJU', 'UESTC', 'USTC', 'XJTU', 'XMU', 'ZJU', 'ZZU']
        FLOWS = []
        PACKETS = []
        BYTES = []

        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='netflow')
        cursor=Con.cursor()

        for ii in range(1,26):
            sql = "select sum(flows)/300, sum(packets)/300, sum(bytes)*8/300 from Netflow_Transport where router="+str(ii)+" group by timestamp order by timestamp desc limit 3;"
            aa = cursor.execute(sql)
            info = cursor.fetchmany(aa)
            if len(info) == 0:
        	FLOWS.append(0)
        	PACKETS.append(0)
        	BYTES.append(0)
            else:
        	FLOWS.append(int(info[2][0]))
        	PACKETS.append(int(info[2][1]))
        	BYTES.append(int(info[2][2]))
	
        FLOWS.insert(0, sum(FLOWS))
        PACKETS.insert(0, sum(PACKETS))
        BYTES.insert(0, sum(BYTES))

        data['ROUTER'] = ROUTER
        data['FLOWS'] = FLOWS
        data['PACKETS'] = PACKETS
        data['BYTES'] = BYTES
	
        callback = request.GET.get('callback','logIt')
        D = '%s(%s)'%(callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")
