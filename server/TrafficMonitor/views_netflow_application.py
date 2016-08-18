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

class application(APIView):
    def get(self, request, format=None):
        data = {}
        TIME = []
        od_HTTP = OrderedDict()
        od_DNS = OrderedDict()
        od_SNMP = OrderedDict()
        od_POP3 = OrderedDict()
        od_TELNET = OrderedDict()
        od_HTTPS = OrderedDict()
        od_SMTP = OrderedDict()
        od_FTP = OrderedDict()
        od_TFTP = OrderedDict()
        od_IMAP = OrderedDict()
        od_VALUE = OrderedDict()
        Con = MySQLdb.connect(host='localhost', user='root', passwd='root', db='netflow')
        cursor = Con.cursor()

        type = int(request.GET.get('type', 1))
        realtime = int(request.GET.get('realtime', 1))
        router = int(request.GET.get('router', 0))
        Stime = int(request.GET.get('Stime', 1000000))
        Etime = int(request.GET.get('Etime', 4294836225))
        Period = int(request.GET.get('period', 1))
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
            Period = Period * 10
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

        sql = "select timestamp, protocol, " + Q_unit + " from Netflow_Application where " + Q_stime + " && " + Q_etime + Q_router + Q_protocol + " group by timestamp, protocol order by timestamp desc" + Q_period

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
            od_HTTP[tmp] = 0
            od_DNS[tmp] = 0
            od_SNMP[tmp] = 0
            od_POP3[tmp] = 0
            od_TELNET[tmp] = 0
            od_HTTPS[tmp] = 0
            od_SMTP[tmp] = 0
            od_FTP[tmp] = 0
            od_TFTP[tmp] = 0
            od_IMAP[tmp] = 0
            od_VALUE[tmp] = 0
            tmp = tmp - delta
            n=n-1

        if Protocol == 0:
            for ii in info:
                print ii[2]
                if ii[1] == 10:
                    od_IMAP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 9:
                    od_TFTP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 8:
                    od_FTP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 7:
                    od_SMTP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 6:
                    od_HTTPS[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 5:
                    od_TELNET[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 4:
                    od_POP3[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 3:
                    od_SNMP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 2:
                    od_DNS[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

                if ii[1] == 1:
                    od_HTTP[datetime.fromtimestamp(ii[0])]=(int(ii[2]))

            TIME = od_HTTP.keys()[:Period]
            data['TIME'] = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1]
            data['HTTP'] = od_HTTP.values()[:Period][::-1]
            data['DNS'] = od_DNS.values()[:Period][::-1]
            data['SNMP'] = od_SNMP.values()[:Period][::-1]
            data['POP3'] = od_POP3.values()[:Period][::-1]
            data['TELNET'] =od_TELNET.values()[:Period][::-1]
            data['HTTPS'] = od_HTTPS.values()[:Period][::-1]
            data['SMTP'] = od_SMTP.values()[:Period][::-1]
            data['FTP'] = od_FTP.values()[:Period][::-1]
            data['TFTP'] = od_TFTP.values()[:Period][::-1]
            data['IMAP'] = od_IMAP.values()[:Period][::-1]
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
