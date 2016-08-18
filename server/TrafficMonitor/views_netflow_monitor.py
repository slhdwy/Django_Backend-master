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
from datetime import datetime , timedelta
from collections import OrderedDict

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
        #对当前时间序列做初始化，初始化为0
        now = datetime.now()
        curmin = int(now.strftime('%M'))
        cur=now.replace(minute=(curmin-curmin%5),second=0,microsecond=0)
        delta = timedelta(minutes=5)
        #数据库
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

        n = Period
        od_all = OrderedDict()
        od_1 = OrderedDict()
        od_2 = OrderedDict()
        od_3 = OrderedDict()
        od_4 = OrderedDict()
        tmp = cur

        while n > 0 :
            #当前时间是第一个值，倒退period个点
            od_all[tmp] = 0
            od_1[tmp] = 0
            od_2[tmp] = 0
            od_3[tmp] = 0
            od_4[tmp] = 0
            tmp = tmp - delta
            n=n-1

        #若数据库中有当前时间序列的值，重新赋值
        for ii in info_all:
            od_all[datetime.fromtimestamp(ii[0])] = int(ii[1])

        for ii in info:
            #ICMP
            if ii[1] == 1:
                od_3[datetime.fromtimestamp(ii[0])] = int(ii[1])
            #TCP
            elif ii[1] == 2:
                od_1[datetime.fromtimestamp(ii[0])] = int(ii[1])
            #UDP
            elif ii[1] == 3:
                od_2[datetime.fromtimestamp(ii[0])] = int(ii[1])
            #OTHERS
            elif ii[1] == 4:
                od_4[datetime.fromtimestamp(ii[0])] = int(ii[1])
             
        TIME = od_all.keys()[:Period]
        TIME = [x.strftime ('%Y-%m-%d %H:%M:%S') for x in TIME] [::-1]
        VALUE0 = od_all.values()[:Period]
        VALUE0 = VALUE0[::-1]
        VALUE1 = od_1.values()[:Period]
        VALUE1 = VALUE1[::-1]
        VALUE2 = od_2.values()[:Period]
        VALUE2 = VALUE2[::-1]
        VALUE3 = od_3.values()[:Period]
        VALUE3 = VALUE3[::-1]
        VALUE4 = od_4.values()[:Period]
        VALUE4 = VALUE4[::-1]

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
