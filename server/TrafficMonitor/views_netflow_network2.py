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
import time


class network(APIView):
    def get(self, request, format=None):
        data = {}
        TIME = []
        CHINA = []
        RUSSIA = []
        CANADA = []
        GERMANY = []
        JAPAN = []
        US = []
        UK = []
        INDIA = []
        HK = []
        OTHERS = []
        VALUE = []
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

        if Country == 0:
            info = info[::-1]
            ii = 0
            while (ii < len(info)):
                TIME.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info[ii][0])))
                if info[ii][1] == 10:
                    OTHERS.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    OTHERS.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 9:
                    HK.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    HK.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 8:
                    INDIA.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    INDIA.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 7:
                    UK.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    UK.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 6:
                    US.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    US.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 5:
                    JAPAN.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    JAPAN.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 4:
                    GERMANY.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    GERMANY.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 3:
                    CANADA.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    CANADA.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 2:
                    RUSSIA.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    RUSSIA.append(0)
                if ii >= len(info):
                    break

                if info[ii][1] == 1:
                    CHINA.append(int(info[ii][2]))
                    ii = ii + 1
                else:
                    CHINA.append(0)
                if ii >= len(info):
                    break

            data['TIME'] = TIME
            data['CHINA'] = CHINA
            data['RUSSIA'] = RUSSIA
            data['CANADA'] = CANADA
            data['GERMANY'] = GERMANY
            data['JAPAN'] = JAPAN
            data['US'] = US
            data['UK'] = UK
            data['INDIA'] = INDIA
            data['HK'] = HK
            data['OTHERS'] = OTHERS
            data['sql'] = sql

        else:
            for ii in info[::-1]:
                TIME.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ii[0])))
                VALUE.append(int(ii[2]))
            data['TIME'] = TIME
            data['VALUE'] = VALUE

        callback = request.GET.get('callback', 'logIt')
        D = '%s(%s)' % (callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")
