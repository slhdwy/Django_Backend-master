from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import json
import httplib
import paramiko   
# Create your views here.
class LogManagement(APIView):
    def get(self, request, format=None):
        #
        #include method here
	#
	callback = request.GET.get('callback', 'logIt')
	body = {}
	data={}
	packet=[]
	storm_h_z = request.GET.get('type', 1);	
 	want_time =request.GET.get('tim',1);
	pag_cur=request.GET.get('pageIndex',1);
	pag_num=request.GET.get('pag',1);
	sel_type=request.GET.get('seltype',1);
	host_type=request.GET.get('hosttype',1);
	type_type=request.GET.get('typetype',1);
	if storm_h_z == '1' : #read storm file log
		#t = paramiko.Transport(("2001:da8:a0:500::1:9",22))
#		t = paramiko.Transport(("166.111.143.200",22))	
		#t.connect(useTrname="pangu", password ="thiSiSnoTsecurE")
#		t.connect(username = "root", password = "tsinghuamcloud")
		#sftp = paramiko.SFTPClient.from_transport(t)
		#localpath='/home/tmp/test.out'
#		remotepath='/root/TsinghuaCloudExt/README.md'
		#remotepath='/home/pangu/zookeeper.out'
		#sftp.get(remotepath, localpath)
		#t.close()
		with open('/opt/apache-storm-0.9.4/logs/supervisor.log') as f:
			c = f.read()
		
		body['log']=''
                s=c.split('\n')
                a0=s[0]
                for i in range(0,len(s)):
                        if len(s) == 1:
                                if a0[:1] != '2':
                                       #print '0' #return 0
                                        break
                        a = s[i]
                        body['log'] += a
                        body['log'] +="\r\n"
		#body['log'] = c
		f.close()
		D = '%s(%s)'%(callback, json.dumps(body))
		return HttpResponse(D, content_type="application/json")
	if storm_h_z == '2': #search hadoop log
		with open('/opt/apache-storm-0.9.4/logs/supervisor.log') as f:
			c = f.read()
		f.close()
		
		body['log']=''
		s=c.split('\n')
                a0=s[0]
                for i in range(0,len(s)):
                	if len(s) == 1:
                	       	if a0[:1] != '2':
                                       #print '0' #return 0
                  	             	break
               		a = s[i]
                	body['log'] += a
			body['log'] +="\r\n"
		#body['log'] = c
                
		D = '%s(%s)'%(callback, json.dumps(body))
                return HttpResponse(D, content_type="application/json")
	if storm_h_z == '3' :	#search keyword for storm log
		with open('/opt/apache-storm-0.9.4/logs/supervisor.log') as f:
			c=f.read()
		body['log']=''
		s=c.split('\n')
                a0=s[0]
                for i in range(0,len(s)):
                       if len(s) == 1:
                               if a0[:1] != '2':
                                       #print '0' #return 0
                                       break
                       a = s[i]
                       if a.find(want_time)!=-1:#a[:36] =='W': 
			       body['log'] += a
                	       body['log'] +="\r\n"
		f.close()
		D='%s(%s)'%(callback, json.dumps(body))
		return HttpResponse(D, content_type="application/json")
	if storm_h_z =='4' : #log2.html
		if (type_type=="storm-slave" and host_type=="2001:da8:a0:500::1:9") or (type_type=="storm-slave" and host_type=='2') or (type_type=='2' and host_type=="2001:da8:a0:500::1:9"):
			with open('/opt/apache-storm-0.9.4/logs/supervisor.log') as f:
                		c = f.read()
			body['date']=''
                	body['time']=''
                	body['masteroslave']=''
                	body['state']=''
                	body['message']=''

                	s=c.split('\n')
                	a0=s[0]
                	for i in range(0,len(s)):
                		if len(s) == 1:
                               		if a0[:1] != '2':
                                       		#print '0' #return 0
                                       		break
                		a = s[i]
				if a.find(sel_type)!=-1 and a[:1]=='2':#and a.find(type_type)!=-1 and a[:1]=='2':
					body={}
            				body['date'] = a[:10]
            				body['time'] = a[11:28]
					body['host'] = '2001:da8:a0:500::1:9'
            				body['severity'] = a.split(' ')[2]
            				body['type'] = 'storm-slave'
					pos = a.find(']')
					body['message'] = a[pos+1:]
					packet.append(body)	  
                	f.close()
		elif (type_type=="storm-slave" and host_type=="2001:da8:a0:500::1:7") or (type_type=='2' and host_type=="2001:da8:a0:500::1:7"):
                 	t = paramiko.Transport(("2001:da8:a0:500::1:7",22))
                	t.connect(username="pangu", password ="thiSiSnoTsecurE")
                	sftp = paramiko.SFTPClient.from_transport(t)
                	localpath='/home/pangu/tmp/storm_cur7.log'
                	remotepath='/opt/apache-storm-0.9.4/logs/supervisor.log'#####
                	sftp.get(remotepath, localpath)
                	t.close()

			with open('/home/pangu/tmp/storm_cur7.log') as f:
                                c = f.read()
                        body['date']=''
                        body['time']=''
                        body['masteroslave']=''
                        body['state']=''
                        body['message']=''

                        s=c.split('\n')
                        a0=s[0]
                        for i in range(0,len(s)):
                                if len(s) == 1:
                                        if a0[:1] != '2':
                                                #print '0' #return 0
                                                break
                                a = s[i]
                                if a.find(sel_type)!=-1 and a[:1]=='2':#and a.find(type_type)!=-1 and a[:1]=='2':
                                        body={}
                                        body['date'] = a[:10]
                                        body['time'] = a[11:28]
                                        body['host'] = '2001:da8:a0:500::1:7'
                                        body['severity'] = a.split(' ')[2]
                                        body['type'] = 'storm-slave'
                                        pos = a.find(']')
                                        body['message'] = a[pos+1:]
                                        packet.append(body)
                        f.close()
		elif (type_type=="storm-slave" and host_type=="2001:da8:a0:500::1:8") or (type_type=='2' and host_type=="2001:da8:a0:500::1:8"):
                        t = paramiko.Transport(("2001:da8:a0:500::1:10",22))
                        t.connect(username="pangu", password ="thiSiSnoTsecurE")
                        sftp = paramiko.SFTPClient.from_transport(t)
                        localpath='/home/pangu/tmp/storm_cur8.log'
                        remotepath='/opt/apache-storm-0.9.4/logs/supervisor.log'#####

                        sftp.get(remotepath, localpath)
                        t.close()

                        with open('/home/pangu/tmp/storm_cur8.log') as f:
                                c = f.read()
                        body['date']=''
                        body['time']=''
                        body['masteroslave']=''
                        body['state']=''
                        body['message']=''

                        s=c.split('\n')
                        a0=s[0]
                        for i in range(0,len(s)):
                                if len(s) == 1:
                                        if a0[:1] != '2':
                                                #print '0' #return 0
                                                break
                                a = s[i]
                                if a.find(sel_type)!=-1 and a[:1]=='2':#and a.find(type_type)!=-1 and a[:1]=='2':
                                        body={}
                                        body['date'] = a[:10]
                                        body['time'] = a[11:28]
                                        body['host'] = '2001:da8:a0:500::1:8'
					body['severity'] = a.split(' ')[2]
                                        body['type'] = 'storm-slave'
                                        pos = a.find(']')
                                        body['message'] = a[pos+1:]
                                        packet.append(body)
                        f.close()

		elif (type_type=="storm-slave" and host_type=="2001:da8:a0:500::1:10") or (type_type=='2' and host_type=="2001:da8:a0:500::1:10"):
                        t = paramiko.Transport(("2001:da8:a0:500::1:10",22))
                        t.connect(username="pangu", password ="thiSiSnoTsecurE")
                        sftp = paramiko.SFTPClient.from_transport(t)
                        localpath='/home/pangu/tmp/storm_cur10.log'
                        remotepath='/opt/apache-storm-0.9.4/logs/supervisor.log'#####

                        sftp.get(remotepath, localpath)
                        t.close()

                        with open('/home/pangu/tmp/storm_cur10.log') as f:
                                c = f.read()
                        body['date']=''
                        body['time']=''
                        body['masteroslave']=''
                        body['state']=''
                        body['message']=''

                        s=c.split('\n')
                        a0=s[0]
                        for i in range(0,len(s)):
                                if len(s) == 1:
                                        if a0[:1] != '2':
                                                #print '0' #return 0
                                                break
                                a = s[i]
                                if a.find(sel_type)!=-1 and a[:1]=='2':#and a.find(type_type)!=-1 and a[:1]=='2':
                                        body={}
                                        body['date'] = a[:10]
                                        body['time'] = a[11:28]
                                        body['host'] = '2001:da8:a0:500::1:10'
                                        body['severity'] = a.split(' ')[2]
					body['type'] = 'storm-slave'
                                        pos = a.find(']')
                                        body['message'] = a[pos+1:]
                                        packet.append(body)
                        f.close()

		elif type_type=='2' and host_type=='2':
			with open('/opt/apache-storm-0.9.4/logs/supervisor.log') as f:
                                c = f.read()
                        body['date']=''
                        body['time']=''
                        body['masteroslave']=''
                        body['state']=''
                        body['message']=''

                        s=c.split('\n')
                        a0=s[0]
                        for i in range(0,len(s)):
                                if len(s) == 1:
                                        if a0[:1] != '2':
                                                #print '0' #return 0
                                                break
                                a = s[i]
                                if a.find(sel_type)!=-1 and a[:1]=='2':#and a.find(type_type)!=-1 and a[:1]=='2':
                                        body={}
                                        body['date'] = a[:10]
                                        body['time'] = a[11:28]
                                        body['host'] = '2001:da8:a0:500::1:9'
                                        body['severity'] = a.split(' ')[2]
                                        body['type'] = 'storm-slave'
                                        pos = a.find(']')
                                        body['message'] = a[pos+1:]
                                        packet.append(body)
                        f.close()
		else: 
			body['date']=''
                        body['time']=''
                        body['masteroslave']=''
                        body['state']=''
                        body['message']=''
			packet.append(body)

                D='%s(%s)'%(callback, json.dumps(packet))
                return HttpResponse(D, content_type="application/json")
	if storm_h_z == '5' :#log3.html
        	with open('/opt/apache-storm-0.9.4/logs/supervisor.log') as f:
                        c=f.read()
                body['warnin']=''
		body['inf']=''
		body['erro']=''
		body['els']=''
		warnin_i=0
		inf_i=0#138
		erro_i=0
		els_i=0
                s=c.split('\n')
                a0=s[0]
                for i in range(0,len(s)):
                	if len(s) == 1:
                        	if a0[:1] != '2':
                                       #print '0' #return 0
                                	break
                	a = s[i]
			if a[:1]=='2':
                        	if a.find('WARN')!=-1:#a[:36] =='W':
                               		warnin_i=warnin_i+1
				elif a.find('INFO')!=-1:#a[:36] =='W':
                               		inf_i=inf_i+1
				elif a.find('ERROR')!=-1:#a[:36] =='W':
                               		erro_i=erro_i+1
				else:
                               		els_i=els_i+1
		body['warnin']=str(warnin_i)
		body['inf']=str(inf_i)
		body['erro']=str(erro_i)
		body['els']=str(els_i)
		#packet.append(body)
		f.close()

		t = paramiko.Transport(("2001:da8:a0:500::1:8",22))
                t.connect(username="pangu", password ="thiSiSnoTsecurE")
                sftp = paramiko.SFTPClient.from_transport(t)
                localpath='/home/pangu/tmp/zoo_no8.out'
                remotepath='/home/pangu/zookeeper.out'#####
                sftp.get(remotepath, localpath)
                t.close()
                with open('/home/pangu/tmp/storm_cur7.log') as f1:
                        c1 = f1.read()
                body['date0']=''
                body['date1']=''
                body['date2']=''
                body['date3']=''
                body['date4']=''
                body['date5']=''
                body['date6']=''
                body['date7']=''
                body['date8']=''
                body['date9']=''
                body['date10']=''
		body['date11']=''
                body['date12']=''
                body['date13']=''
                body['date14']=''
                body['date15']=''
                body['date16']=''
                body['date17']=''

                date0_i=0
                date1_i=0
                date2_i=0
                date3_i=0
                date4_i=0
                date5_i=0
                date6_i=0
                date7_i=0
                date8_i=0
                date9_i=0
                date10_i=0
		date11_i=0
                date12_i=0
                date13_i=0
                date14_i=0
                date15_i=0
                date16_i=0
                date17_i=0

                s1=c1.split('\n')
                a1=s1[0]
                for i in range(0,len(s1)):
                        if len(s1) == 1:
                                if a1[:1] != '2':
                                       #print '0' #return 0
                                        break
                        a1 = s1[i]
                        if a1[:1]=='2':
                                if a1.find('2016-05-16')!=-1:#a[:36] =='W':
                                        date0_i=date0_i+1
                                elif a1.find('2016-05-17')!=-1:#a[:36] =='W':
                                        date1_i=date1_i+1
                                elif a1.find('2016-05-18')!=-1:#a[:36] =='W':
                                        date2_i=date2_i+1
                                elif a1.find('2016-05-19')!=-1:#a[:36] =='W':
                                        date3_i=date3_i+1
                                elif a1.find('2016-05-20')!=-1:#a[:36] =='W':
                                        dat24_i=date4_i+1
                                elif a1.find('2016-05-21')!=-1:#a[:36] =='W':
                                        date5_i=date5_i+1
                                elif a1.find('2016-05-22')!=-1:#a[:36] =='W':
                                        data6_i=date6_i+1
                                elif a1.find('2016-05-23')!=-1:#a[:36] =='W':
                                        date7_i=date7_i+1
                                elif a1.find('2016-05-24')!=-1:#a[:36] =='W':
                                        date8_i=date8_i+1
                                elif a1.find('2016-05-25')!=-1:#a[:36] =='W':
                                        date9_i=date9_i+1
                                elif a1.find('2016-05-26')!=-1:#a[:36] =='W':
                                        date10_i=date10_i+1
					if a1.find('2016-05-26T09')!=-1:
                                        	date11_i=date11_i+1
                                	elif a1.find('2016-05-26T11')!=-1:
                                        	date12_i=date12_i+1
                                	elif a1.find('2016-05-26T13')!=-1:
                                       		date13_i=date13_i+1
                                	elif a1.find('2016-05-26T15')!=-1:
                                        	date14_i=date14_i+1
                               		elif a1.find('2016-05-26T17')!=-1:
                                        	date15_i=date15_i+1
                                	elif a1.find('2016-05-26T19')!=-1:
                                        	date16_i=date16_i+1
                                	elif a1.find('2016-05-26T21')!=-1:
                                        	date17_i=date17_i+1
                               		else:
                                        	date17_i=date17_i+1
      
                body['date0']=str(date0_i)
                body['date1']=str(date1_i)
                body['date2']=str(date2_i)
                body['date3']=str(date3_i)
                body['date4']=str(date4_i)
                body['date5']=str(date5_i)
                body['date6']=str(date6_i)
                body['date7']=str(date7_i)
                body['date8']=str(date8_i)
                body['date9']=str(date9_i)
                body['date10']=str(date10_i)
                body['date11']=str(date11_i)
                body['date12']=str(date12_i)
                body['date13']=str(date13_i)
                body['date14']=str(date14_i)
                body['date15']=str(date15_i)
                body['date16']=str(date16_i)
                body['date17']=str(date17_i)

		packet.append(body)
                f1.close()


                D='%s(%s)'%(callback, json.dumps(packet))
                return HttpResponse(D, content_type="application/json")
             
