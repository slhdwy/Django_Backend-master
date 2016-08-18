from rest_framework.views import APIView
from rest_framework.response import Response
import redis
import json
from rest_framework.parsers import JSONParser
# Create your views here.
from django.http import HttpResponse
class RealtimeApplicationThroughput(APIView):
	parser_classes = (JSONParser,)
	def OPTIONS(self):
        	web.header('Content-Type', 'application/json')
        	web.header('Access-Control-Allow-Origin', '*')
        	web.header('Access-Control-Allow-Methods', 'POST, GET')
        	web.header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
        	return web.data()

	

	def get(self, request, format=None):
		callback = request.GET.get('callback','logIt')	
		print callback
		data = []
		#r = redis.Redis(host='166.111.143.200', port=6379, db=0)
		r = redis.Redis(host='2001:da8:a0:500::1:7', port=6379, db=0)
		line1 = r.get('throuput')
		line2 = r.get('countPacket')
		#line1 = '1/2/3/4/5/6/7/8/9/0'
		#line2 = '0/9/8/7/6/5/4/3/2/1'
		array1 = line1.split('/')
		array2 = line2.split('/')

		for i in range(1,len(array1)):
			body = {}
			body['throuput'] = array1[i]
			body['countPacket'] = array2[i]
			data.append(body)
			#print data
		D = '%s(%s)'%(callback, json.dumps(data))
		#D = '%s(%s)'%(callback, '{"username":"jack","age":21,"gender":"male"}')
		#print D
		#return Response(data)
		#return HttpResponse(D, content_type="application/json;charset=utf-8")
		return HttpResponse(D, content_type="application/json")

class RealtimeApplicationThroughput_Throuput_Second(APIView):
        parser_classes = (JSONParser,)
        
	def OPTIONS(self):
                web.header('Content-Type', 'application/json')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', 'POST, GET')
                web.header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
                return web.data()

	
	def get(self, request, format=None):
                callback = request.GET.get('callback','logIt')
                print callback
		data = []
                r = redis.Redis(host='2001:da8:a0:500::1:7', port=6379, db=0)
                line = r.get('throuput_second')
                array = line.split('/')

                for i in range(1,len(array)):
                        body = {}
                        body['throuput'] = array[i]
                        data.append(body)
                        #print data
                D = '%s(%s)'%(callback, json.dumps(data))
                return HttpResponse(D, content_type="application/json")

class RealtimeApplicationThroughput_Throuput_Minute(APIView):
        parser_classes = (JSONParser,)
        
	def OPTIONS(self):
                web.header('Content-Type', 'application/json')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', 'POST, GET')
                web.header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
                return web.data()
	
	def get(self, request, format=None):
                callback = request.GET.get('callback','logIt')
                data = []
		print callback
                r = redis.Redis(host='2001:da8:a0:500::1:7', port=6379, db=0)
                line = r.get('throuput_minute')
                array = line.split('/')

                for i in range(1,len(array)):
                        body = {}
                        body['throuput'] = array[i]
                        data.append(body)
                        #print data
                D = '%s(%s)'%(callback, json.dumps(data))
                return HttpResponse(D, content_type="application/json")

class RealtimeApplicationThroughput_CountPacket_Second(APIView):
        parser_classes = (JSONParser,)
        
	def OPTIONS(self):
                web.header('Content-Type', 'application/json')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', 'POST, GET')
                web.header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
                return web.data()

	def get(self, request, format=None):
                callback = request.GET.get('callback','logIt')
                data = []
		print callback
                r = redis.Redis(host='2001:da8:a0:500::1:7', port=6379, db=0)
                line = r.get('countPacket_second')
                array = line.split('/')

                for i in range(1,len(array)):
                        body = {}
                        body['countPacket'] = array[i]
                        data.append(body)
                        #print data
                D = '%s(%s)'%(callback, json.dumps(data))
                return HttpResponse(D, content_type="application/json")

class RealtimeApplicationThroughput_CountPacket_Minute(APIView):
        parser_classes = (JSONParser,)

	def OPTIONS(self):
                web.header('Content-Type', 'application/json')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', 'POST, GET')
                web.header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
                return web.data()

        def get(self, request, format=None):
                callback = request.GET.get('callback','logIt')
                data = []
		print callback
                r = redis.Redis(host='2001:da8:a0:500::1:7', port=6379, db=0)
                line = r.get('countPacket_minute')
                array = line.split('/')

                for i in range(1,len(array)):
                        body = {}
                        body['countPacket'] = array[i]
                        data.append(body)
                        #print data
                D = '%s(%s)'%(callback, json.dumps(data))
                return HttpResponse(D, content_type="application/json")

class RealtimeApplicationThroughput_Minute(APIView):
        parser_classes = (JSONParser,)

	def OPTIONS(self):
		print 'options'
                #return HttpResponse(content_type="application/json", 'Access-Control-Allow-Origin', '*', 'Access-Control-Allow-Methods', 'POST, GET', 'Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')

        def get(self, request, format=None):
                callback = request.GET.get('callback','logIt')
                data = []
 		print '123'
                r = redis.Redis(host='2001:da8:a0:500::1:7', port=6379, db=0)
                line1 = r.get('first_countPacket_minute')
                line2 = r.get('first_throuput_minute')
		#line3 = r.get('_tcp_throuput_minute')
		#line4 = r.get('_tcp_countPacket_minute')
		#line5 = r.get('_udp_throuput_minute')
		#line6 = r.get('_udp_countPacket_minute')
		line7 = r.get('first_minute')
                array1 = line1.split('/')
                array2 = line2.split('/')
		#array3 = line3.split('/')
		#array4 = line4.split('/')
		#array5 = line5.split('/')
		#array6 = line6.split('/')
		array7 = line7.split('/')
                for i in range(1,len(array1)):
                        body = {}
                        body['countPacket_minute'] = array1[i]
                        body['throuput_minute'] = array2[i]
		#	body['tcp_throuput_minute'] = array3[i]
                 #       body['tcp_countPacket_minute'] = array4[i]
		#	body['ucp_throuput_minute'] = array5[i]
		#	body['udp_countPacket_minute'] = array6[i]
			body['TIME'] = array7[i]
                        data.append(body)
                D = '%s(%s)'%(callback, json.dumps(data))
                return HttpResponse(D, content_type="application/json")
		#return HttpResponse(D, content_type="application/json", 'Access-Control-Allow-Origin', '*', 'Access-Control-Allow-Methods', 'POST, GET', 'Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')

class RealtimeApplicationThroughput_Second(APIView):
        parser_classes = (JSONParser,)

	def options(self, request, format=None):
                print '321'
		callback = request.GET.get('callback','logIt')
		D = '%s()'%(callback)
		return HttpResponse(D, content_type="application/json")

        def get(self, request, format=None):
                callback = request.GET.get('callback','logIt')
                data = []
		print callback
                r = redis.Redis(host='2001:da8:a0:500::1:7', port=6379, db=0)
                line1 = r.get('first_countPacket_second')
                line2 = r.get('first_throuput_second')
		#line3 = r.get('_tcp_throuput_second')
		#line4 = r.get('_tcp_countPacket_second')
                #line5 = r.get('_udp_throuput_second')
		#line6 = r.get('_udp_countPacket_second')
		line7 = r.get('first_second')
                array1 = line1.split('/')
                array2 = line2.split('/')
		#array3 = line3.split('/')
                array7 = line7.split('/')
		#array6 = line6.split('/')
		#array4 = line4.split('/')
		#array5 = line5.split('/')
                for i in range(1,len(array1)):
                        body = {}
                        body['countPacket_second'] = array1[i]
                        body['throuput_second'] = array2[i]
		#	body['tcp_throuput_second'] = array3[i]
		#	body['tcp_countPacket_second'] = array4[i]
		#	body['udp_throuput_second'] = array5[i]
		#	body['udp_countPacket_second'] = array6[i]
			body['TIME'] = array7[i]
			data.append(body)
        	
	        #print data
                D = '%s(%s)'%(callback, json.dumps(data))
                return HttpResponse(D, content_type="application/json")

class RealtimeApplicationDataPacket(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeApplicationDataPacket'})

class RealtimeApplicationStream(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeApplicationStream'})

class RealtimeSourceCountryThroughput(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeSourceCountryThroughput'})

class RealtimeDestinationCountryThroughput(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeDestinationCountryThroughput'})

class RealtimeApplicationStatisticsForm(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeApplicationStatisticsForm'})

class RealtimeApplicationChart(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeApplicationChart'})

class RealtimeSourceCountryChart(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeSourceCountryChart'})

class RealtimeDestinationCountryChart(APIView):
	def get(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'RealtimeDestinationCountryChart'})
