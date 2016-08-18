# coding=utf-8
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

class transport(APIView):
    def get(self, request, format=None):
        data = {}
        TIME = []
        od_ICMP = OrderedDict()
        od_TCP = OrderedDict()
        od_UDP = OrderedDict()
        od_OTHER = OrderedDict()
        od_VALUE = OrderedDict()

        Con = MySQLdb.connect(host='localhost', user='root', passwd='root', db='netflow')
        cursor = Con.cursor()

        type = int(request.GET.get('type', 1))
        realtime = int(request.GET.get('realtime', 1))
        router = int(request.GET.get('router', 0))
        Stime = int(request.GET.get('Stime', 1000000))
        Etime = int(request.GET.get('Etime', 4294836225))
        Period = int(request.GET.get('period', 2880))
        Protocol = int(request.GET.get('protocol', 0))

        if Period == 0:
            Period = 288
            realtime = 1
        elif Period == 1:
            Period = 288
            realtime = 0
        elif Period == 2:
            Period = 288 * 7
            realtime = 0
        elif Period == 3:
            Period = 288 * 30
            realtime = 0
        elif Period == 4:
            Period = 288 * 365
            realtime = 0

        if Protocol == 0:
            Q_protocol = ''
            Period = Period * 4
        else:
            Q_protocol = ' && protocol=' + str(Protocol)

        if router == 0:
            Q_router = ' '
        else:
            Q_router = ' && router=' + str(router)

        Q_stime = 'timestamp>' + str(Stime)
        Q_etime = 'timestamp<' + str(Etime)

        if type == 1:
            Q_unit = 'sum(flows)/300'
        elif type == 2:
            Q_unit = 'sum(packets)/300'
        else:
            Q_unit = 'sum(bytes)*8/300'

        if realtime == 1:
            Q_period = ' limit ' + str(Period) + ';'
        else:
            Q_period = ';'

        sql = "select timestamp, protocol, " + Q_unit + " from Netflow_Transport where " + Q_stime + " && " + Q_etime + Q_router + Q_protocol + " group by timestamp, protocol order by timestamp desc" + Q_period

        aa = cursor.execute(sql)
        info = cursor.fetchmany(aa)

        #对当前时间序列做初始化，初始化为0
        now = datetime.now()
        curmin = int(now.strftime('%M'))
        cur=now.replace(minute=(curmin-curmin%5),second=0,microsecond=0)
        delta = timedelta(minutes=5)

        n = Period
        tmp = cur

        while n > 0 :
            #当前时间是第一个值，倒退period个点
            od_ICMP[tmp] = 0
            od_TCP[tmp] = 0
            od_UDP[tmp] = 0
            od_OTHER[tmp] = 0
            od_VALUE[tmp] = 0
            tmp = tmp - delta
            n=n-1

        if Protocol == 0:
            for ii in info:
                if ii[1] == 4:
                    od_OTHER[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 3:
                    od_UDP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 2:
                    od_TCP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 1:
                    od_ICMP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))
            TIME = od_ICMP.keys()[:Period]
            data['TIME'] = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1]
            data['ICMP'] = od_ICMP.values()[:Period][::-1]
            data['TCP'] = od_TCP.values()[:Period][::-1]
            data['UDP'] = od_UDP.values()[:Period][::-1]
            data['OTHER'] = od_OTHER.values()[:Period][::-1]
            #data['sql'] = sql
            #data['mes'] = info[0][0]

        else:
            for ii in info:
                od_VALUE[datetime.fromtimestamp(ii[0])]=(int(ii[2]))
            TIME = od_VALUE.keys()[:Period]
            data['TIME'] = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1]
            data['VALUE'] = od_VALUE.values()[:Period][::-1]

        callback = request.GET.get('callback', 'logIt')
        D = '%s(%s)' % (callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")
