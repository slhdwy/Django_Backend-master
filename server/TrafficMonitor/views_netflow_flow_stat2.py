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

class flow_stat(APIView):

    def get(self, request, format=None):
        data = {}
        TIME = []
        VALUE = []

        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='netflow')
        cursor=Con.cursor()

        type = int(request.GET.get('type', 1))
        realtime = int(request.GET.get('realtime', 1))
        Stime = int(request.GET.get('Stime', 10000000))
        Etime = int(request.GET.get('Etime', 4294836225))
        Period = int(request.GET.get('period', 288))
        Q_stime = 'timestamp>'+str(Stime)
        Q_etime = 'timestamp<'+str(Etime)


        if type == 1:
            Q_unit = 'sum(flows)/300'
	    TITLE = 'Flow/s    '
        elif type == 2:
            Q_unit = 'sum(packets)/300'
	    TITLE = 'Packets/s'
        else:
            Q_unit = 'sum(bytes)*8/300'
	    TITLE = 'Bits/s'

        if realtime == 1:
            Q_period = ' limit '+str(Period)+';'
        else:
            Q_period = ';'

        sql = "select timestamp, " + Q_unit + " from Netflow_Transport where " + Q_stime + " && " + Q_etime + " group by timestamp order by timestamp desc" + Q_period

        aa=cursor.execute(sql)
        info = cursor.fetchmany(aa)
	
	TITLE = TITLE+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info[-1][0]))+' - '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info[0][0]))

        for ii in info[::-1]:
	    if Period == 288:
		TIME.append(time.strftime('%H:%M',time.localtime(ii[0])))
	    elif Period == 288*7:
		TIME.append(time.strftime('%m-%d %H',time.localtime(ii[0])))
	    elif Period == 288*30:
		TIME.append(time.strftime('%Y-%m-%d',time.localtime(ii[0])))
	    else:
                TIME.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ii[0])))
            VALUE.append(int(ii[1]))	

        data['TIME'] = TIME
        data['VALUE'] = VALUE
	data['TITLE'] = TITLE
        callback = request.GET.get('callback','logIt')
        D = '%s(%s)'%(callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")
