# -*- coding: utf-8 -*-
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
from datetime import datetime , timedelta
from collections import OrderedDict


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
    
        #对当前时间序列做初始化，初始化为0
        now = datetime.now()
        curmin = int(now.strftime('%M'))
        cur=now.replace(minute=(curmin-curmin%5),second=0,microsecond=0)
        delta = timedelta(minutes=5)

        n = Period
        od = OrderedDict()
        tmp = cur

        while n > 0 :
            #当前时间是第一个值，倒退period个点
            od[tmp] = 0
            tmp = tmp - delta
            n=n-1
    
        #若数据库中有当前时间序列的值，重新赋值
        for ii in info:
            od[datetime.fromtimestamp(ii[0])] = int(ii[1])

        TIME = od.keys()[:Period]
        VALUE = od.values()[:Period][::-1]
        TIME = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1]
        
        """
        if Period == 288:
            TIME = [x.strftime ('%H:%M') for x in TIME] [::-1]
        elif Period == 288*7:
            TIME = [x.strftime ('%m-%d %H') for x in TIME] [::-1]
        elif Period == 288*30:
            TIME = [x.strftime ('%Y-%m-%d') for x in TIME] [::-1]
        else:
            TIME = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1] 
        """

        #TITLE = TITLE+od.keys()[-1].strftime ('%Y-%m-%d %H:%M:%S')+' - '+od.keys()[0].strftime ('%Y-%m-%d %H:%M:%S')
        TITLE = TITLE+TIME[0]+' - '+TIME[-1]
        data['TIME'] = TIME
        data['VALUE'] = VALUE
        data['TITLE'] = TITLE
        callback = request.GET.get('callback','logIt')
        D = '%s(%s)'%(callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")

