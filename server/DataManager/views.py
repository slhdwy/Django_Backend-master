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

class collectreq(APIView):

    def get(self,req, format=None):
        print "collectreq"
        data = {}
        data['message'] = None
        data['username'] = None
        data['datasetname'] = None
        data['srcport'] = None
        data['dstport'] = None
        data['srcip'] = None
        data['dstip'] = None
        data['pro'] = None
        data['link'] = None
        data['num'] = None
        data['date'] = None
        data['time'] = None
        data['duration'] = None
        data['period'] = None
        username = None
        datasetname = None
        srcport = None
        dstport = None
        srcip = None
        dstip = None
        pro = None
        link = None
        num = None
        date = None
        time = None
        duration = None
        period = None

        callback = req.GET.get('callback')
        print "liwei1"

        username = req.GET.get('username')
        print("username:%s" %(username))
        if not req.GET.get('username'):
            data['message'] = '请输入用户名!'
            D = '%s(%s)'%(callback, json.dumps(data))
            print("Please enter username")
            return HttpResponse(D, content_type="application/json")
        else:
            if not req.GET.get('datasetname'):
                data['message'] = '请输入数据集名称!'
                D = '%s(%s)'%(callback, json.dumps(data))
                print("Please enter datasetname")
                return HttpResponse(D, content_type="application/json")
            else:
                datasetname = req.GET.get('datasetname')
                print("datasetname:%s" %(datasetname))

                if not req.GET.get('date'):
                    data['message'] = '请输入采集日期!'
                    D = '%s(%s)'%(callback, json.dumps(data))
                    print("Please enter date!")
                    return HttpResponse(D, content_type="application/json")
                else:
                    date = req.GET.get('date')
                    print("date:%s" %(date))

                    if not req.GET.get('time'):
                        data['message'] = '请输入采集时间!'
                        D = '%s(%s)'%(callback, json.dumps(data))
                        print("Please enter time!")
                        return HttpResponse(D, content_type="application/json")
                    else:
                        time = req.GET.get('time')
                        print("time:%s" %(time))

                        if not req.GET.get('duration'):
                            data['message'] = '请输入采集时长!'
                            D = '%s(%s)'%(callback, json.dumps(data))
                            print("Please enter duration!")
                            return HttpResponse(D, content_type="application/json")
                        else:
                            duration = req.GET.get('duration')
                            print("duration:%s" %(duration))
                            if not req.GET.get('period'):
                                data['message'] = '请输入采集周期!'
                                D = '%s(%s)'%(callback, json.dumps(data))
                                print("Please enter period!")
                                return HttpResponse(D, content_type="application/json")
                            else:
                                period = req.GET.get('period')
                                print("period:%s" %(period))
                                if not req.GET.get('link'):
                                    data['message'] = '请输入采集链路!'
                                    D = '%s(%s)'%(callback, json.dumps(data))
                                    print("Please enter link!")
                                    return HttpResponse(D, content_type="application/json")
                                else:
                                    link = req.GET.get('link')
                                    print("link:%s" %(link))
                                    if not req.GET.get('num'):
                                        data['message'] = '请输入采集编号!'
                                        D = '%s(%s)'%(callback, json.dumps(data))
                                        print("Please enter num!")
                                        return HttpResponse(D, content_type="application/json")
                                    else:
                                        num = req.GET.get('num')
                                        print("num:%s" %(num))
                                        if not req.GET.get('srcip'):
                                            srcip = 'no'
                                        else:
                                            srcip = req.GET.get('srcip')
                                        print("srcip:%s" %(srcip))
                                        if not req.GET.get('dstip'):
                                            dstip = 'no'
                                        else:
                                            dstip = req.GET.get('dstip')
                                        print("dstip:%s" %(dstip))
                                        if not req.GET.get('srcport'):
                                            srcport = '100000'
                                        else:
                                            srcport = req.GET.get('srcport')
                                        print("srcport:%s" %(srcport))
                                        if not req.GET.get('dstport'):
                                            dstport = '100000'
                                        else:
                                            dstport = req.GET.get('dstport')
                                        print("dstport:%s" %(dstport))
                                        pro = req.GET.get('pro')
                                        print("pro:%s" %(pro))

                                        usercheck = datacolreq.objects.filter(username=username,datasetname=datasetname)
                                        if not len(usercheck) == 0:
                                            data['message'] = '该用户已有此数据集！'
                                            D = '%s(%s)'%(callback, json.dumps(data))
                                            print("This user has the dataset!")
                                            return HttpResponse(D, content_type="application/json")
                                        else:   #user exit but do not have the dataset, new it
                                            req = datacolreq()
                                            req.username = username
                                            req.datasetname = datasetname
                                            req.srcport = srcport
                                            req.dstport = dstport
                                            req.srcip = srcip
                                            req.dstip = dstip
                                            req.pro = pro
                                            req.link = link
                                            req.num = num
                                            req.date = date
                                            req.time = time
                                            req.duration = duration
                                            req.period = period
                                            req.save()

                                            data['message'] = "提交成功！请等待审核结果。"
                                            data['username'] = username
                                            data['datasetname'] = datasetname
                                            data['srcport'] = srcport
                                            data['dstport'] = dstport
                                            data['srcip'] = srcip
                                            data['dstip'] = dstip
                                            data['pro'] = pro
                                            data['link'] = link
                                            data['num'] = num
                                            data['date'] = date
                                            data['time'] = time
                                            data['duration'] = duration
                                            data['period'] = period
                                            D = '%s(%s)'%(callback, json.dumps(data))
                                            return HttpResponse(D, content_type="application/json")


class datasetshow(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):

        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='bigdata')
        cursor=Con.cursor()
        aa=cursor.execute("select * from DataManager_dataset")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)

        for ii in info:
            data = {}
            data['datasetid'] = ii[0]
            data['datasetname'] = ii[1]
            data['username'] = ii[2]
            data['status'] = ii[3]
            data['category'] = ii[4]
            data['source'] = ii[5]
            data['anonymization'] = ii[6]
            data['releasedate'] = ii[7].strftime('%Y-%m-%d')
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")


class colreqshow(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):

        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='bigdata')
        cursor=Con.cursor()
        aa=cursor.execute("select * from DataManager_datacolreq")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)

        for ii in info:
            data = {}
            data['username'] = ii[0]
            data['datasetname'] = ii[1]
            data['date'] = ii[2]
            data['time'] = ii[3]
            data['duration'] = ii[4]
            data['period'] = ii[5]
            data['link'] = ii[6]
            data['num'] = ii[7]
            data['srcport'] = ii[8]
            data['dstport'] = ii[9]
            data['srcip'] = ii[10]
            data['dstip'] = ii[11]
            data['pro'] = ii[12]
            # print ii[2].strftime('%Y-%m-%d')
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

class deleteds(APIView):
    parser_classes = (JSONParser,)
    def get(self, req, format=None):
        data = {}
     #  data['datasetname'] = None
        data['datarow'] = None
        data['message'] = None
     #  datasetname = req.GET.get('datasetname')
        rowtemp = req.GET.get('row')
        rowtemp1 = rowtemp.encode("utf-8")
        print int(rowtemp1)
        row = int(rowtemp1)
     #  data['datasetname'] = datasetname
        data['datarow'] = row
        Con=MySQLdb.connect(host='localhost', user='root', passwd='root', db='bigdata')
        cursor=Con.cursor()
        cursor.execute("delete a from DataManager_dataset a inner join (select * from DataManager_dataset limit %s,1) b on a.datasetid = b.datasetid", row)
        cursor.execute("commit")
        cursor.close()
        Con.commit()
        Con.close()
        callback = req.GET.get('callback')
        data['message'] = "删除成功！"
        D = '%s(%s)'%(callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")

class selectds(APIView):
    parser_classes = (JSONParser,)
    def get(self, req, format=None):

        username = req.GET.get('username')
        print username
        data = {}
        data['message'] = None
        data['datasetid'] = None
        data['datasetname'] = None
        data['username'] = None
        data['status'] = None
        data['anonymization'] = None
        data['category'] = None
        data['source'] = None
        data['releasedate'] = None

        usercheck = dataset.objects.filter(username=username)
        if len(usercheck) == 0:
           data['message'] = "该用户没有数据集！"
           callback = req.GET.get('callback')
           D = '%s(%s)'%(callback, json.dumps(data))
           print("This user has no dataset!")
           return HttpResponse(D, content_type="application/json")

        else:
           Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='bigdata')
           cursor=Con.cursor()
           aa=cursor.execute("select * from DataManager_dataset where username= %s", username)
           packet=[]
           callback = req.GET.get('callback')
           info = cursor.fetchmany(aa)

           for ii in info:

             data['datasetid'] = ii[0]
             data['datasetname'] = ii[1]
             data['username'] = ii[2]
             data['status'] = ii[3]
             data['category'] = ii[4]
             data['source'] = ii[5]
             data['anonymization'] = ii[6]
             data['releasedate'] = ii[7].strftime('%Y-%m-%d')
             packet.append(data)
           D = '%s(%s)'%(callback, json.dumps(packet))
           cursor.close()
           Con.commit()
           Con.close()
           return HttpResponse(D, content_type="application/json")






















