from rest_framework.views import APIView
import json
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import pyhs2
import time


class netflow_query(APIView):
    def get(self, request, format=None):
        data = {}
        SRC_IP = []
        SRC_PORT = []
        DST_IP = []
        DST_PORT = []
        PROTOCOL = []
        FLOWS = []
        PACKETS = []
        BYTES = []

        callback = request.GET.get('callback', 'logIt')
        router = request.GET.get('router', 'THU')
        order = int(request.GET.get('order', 0))
        protocol = int(request.GET.get('protocol', 0))
        topn = int(request.GET.get('topn', 10))
        stime = int(request.GET.get('stime', 0))
        etime = int(request.GET.get('etime', 2000000000))
        srcip = request.GET.get('srcip', '')
        srcport = int(request.GET.get('srcport', -1))
        dstip = request.GET.get('dstip', '')
        dstport = int(request.GET.get('dstport', -1))

        conn = pyhs2.connect(host='10.8.0.5', port=10000, authMechanism="PLAIN", user='pangu',
                             password='thiSiSnoTsecurE', database='default')
        cur = conn.cursor()

        timeArray = time.localtime(stime)
        otherStyleTime = time.strftime("%Y/%m/%d", timeArray)
        location = '/netflow/' + str(router) + '/' + otherStyleTime

        Q_router = ' & router = ' + str(router)

        if order == 0:
            Q_order = ' order by flows desc '
        elif order == 1:
            Q_order = ' order by packets desc '
        elif order == 2:
            Q_order = ' order by bytes desc '

        if protocol == 0:
            Q_protocol = ' '
        else:
            Q_protocol = ' & proto = ' + str(protocol)

        Q_topn = ' limit ' + str(topn)
        Q_stime = ' stime > ' + str(stime)
        Q_etime = ' & etime < ' + str(etime)

        DropTB = 'DROP TABLE NETFLOW_QUERY'

        CreateTB = 'CREATE EXTERNAL TABLE NETFLOW_QUERY(STIME INT,ETIME INT,SRC_IP STRING,SRC_PORT INT,DST_IP STRING,DST_PORT INT,PROTO INT,PKT BIGINT,BYTES BIGINT)ROW FORMAT SERDE \'com.pangu.Hive.NetflowSerDe\' STORED AS INPUTFORMAT \'com.pangu.Netflow.Netflow_IO.NetflowHiveInputFormat\'  OUTPUTFORMAT \'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat\' LOCATION \'' + location + '\''

        if srcip == '':
            Q_srcip = ''
        else:
            Q_srcip = ' & src_ip = \"' + str(srcip) + '\"'

        if srcport == -1:
            Q_srcport = ''
        else:
            Q_srcport = ' & src_port = ' + str(srcport)

        if dstip == '':
            Q_dstip = ''
        else:
            Q_dstip = ' & dst_ip = \"' + str(dstip) + '\"'

        if dstport == -1:
            Q_dstport = ''
        else:
            Q_dstport = ' & dst_port = ' + str(dstport)

        SQL = 'select src_ip, src_port, dst_ip, dst_port, proto, count(proto) as flows, sum(pkt) as packets, sum(bytes) as bytes from NETFLOW_QUERY where ' + Q_stime + Q_etime + Q_srcip + Q_srcport + Q_dstip + Q_dstport + ' group by src_ip, src_port, dst_ip, dst_port, proto ' + Q_order + Q_topn

        cur.execute(DropTB)
        cur.execute(CreateTB)
        cur.execute(SQL)

        for i in cur.fetch():
            SRC_IP.append(i[0])
            SRC_PORT.append(i[1])
            DST_IP.append(i[2])
            DST_PORT.append(i[3])
            PROTOCOL.append(i[4])
            FLOWS.append(i[5])
            PACKETS.append(i[6])
            BYTES.append(i[7])
        data['SRC_IP'] = SRC_IP
        data['SRC_PORT'] = SRC_PORT
        data['DST_IP'] = DST_IP
        data['DST_PORT'] = DST_PORT
        data['PROTOCOL'] = PROTOCOL
        data['FLOWS'] = FLOWS
        data['PACKETS'] = PACKETS
        data['BYTES'] = BYTES
        data['dropTB'] = DropTB
        data['createTB'] = CreateTB
        data['sql1'] = SQL
        D = '%s(%s)' % (callback, json.dumps(data))
        return HttpResponse(D, content_type="application/json")
