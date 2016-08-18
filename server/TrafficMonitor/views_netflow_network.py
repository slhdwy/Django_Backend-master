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


class network(APIView):
    def get(self, request, format=None):
        data = {}
        TIME = []
        od_CHINA = OrderedDict()
        od_RUSSIA = OrderedDict()
        od_CANADA = OrderedDict()
        od_GERMANY = OrderedDict()
        od_JAPAN = OrderedDict()
        od_US = OrderedDict()
        od_UK = OrderedDict()
        od_INDIA = OrderedDict()
        od_HK = OrderedDict()
        od_OTHERS = OrderedDict()
        od_VALUE = OrderedDict()
        Con = MySQLdb.connect(host='localhost', user='root', passwd='root', db='netflow')
        cursor = Con.cursor()

        type = int(request.GET.get('type', 1))
        realtime = int(request.GET.get('realtime', 1))
        router = int(request.GET.get('router', 0))
        Stime = int(request.GET.get('Stime', 1000000))
        Etime = int(request.GET.get('Etime', 4294836225))
        Period = int(request.GET.get('period', 1))
        Country = int(request.GET.get('country', 0))
        Direction = int(request.GET.get('direction', 0))
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

        if Country == 0:
            #Country : 0 所有国家
            Q_country = ''
            Period = Period * 10
        else:
            Q_country = ' && country=' + str(Country)

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

        Q_direction = ' && direction=' + str(Direction)

        sql = "select timestamp, country, " + Q_unit + " from Netflow_Network where " + Q_stime + " && " + Q_etime + Q_direction + Q_router + Q_country + " group by timestamp, country order by timestamp desc" + Q_period

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
            od_CHINA[tmp] = 0
            od_RUSSIA[tmp] = 0
            od_CANADA[tmp] = 0
            od_GERMANY[tmp] = 0
            od_JAPAN[tmp] = 0
            od_US[tmp] = 0
            od_UK[tmp] = 0
            od_INDIA[tmp] = 0
            od_HK[tmp] = 0
            od_OTHERS[tmp] = 0
            od_VALUE[tmp] = 0
            tmp = tmp - delta
            n=n-1

        if Country == 0:
            for ii in info:
                if ii[1] == 10:
                    od_OTHERS[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 9:
                    od_HK[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 8:
                    od_INDIA[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 7:
                    od_UK[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 6:
                    od_US[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 5:
                    od_JAPAN[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 4:
                    od_GERMANY[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 3:
                    od_CANADA[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 2:
                    od_RUSSIA[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 1:
                    od_CHINA[datetime.fromtimestamp(ii[0])]=(int(ii[2]))
            TIME = od_CHINA.keys()[:Period]
            data['TIME'] = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1]
            data['CHINA'] = od_CHINA.values()[:Period][::-1]
            data['RUSSIA'] = od_RUSSIA.values()[:Period][::-1]
            data['CANADA'] = od_CANADA.values()[:Period][::-1]
            data['GERMANY'] = od_GERMANY.values()[:Period][::-1]
            data['JAPAN'] = od_JAPAN.values()[:Period][::-1]
            data['US'] = od_US.values()[:Period][::-1]
            data['UK'] = od_UK.values()[:Period][::-1]
            data['INDIA'] = od_INDIA.values()[:Period][::-1]
            data['HK'] = od_HK.values()[:Period][::-1]
            data['OTHERS'] = od_OTHERS.values()[:Period][::-1]
            #data['sql'] = sql
        else:
            for ii in info:
                od_VALUE[datetime.fromtimestamp(ii[0])]=(int(ii[2]))
            TIME = od_VALUE.keys()[:Period]
            data['TIME'] = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1]
            data['VALUE'] = od_VALUE.values()[:Period][::-1]

        callback = request.GET.get('callback', 'logIt')
        D = '%s(%s)' % (callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")
