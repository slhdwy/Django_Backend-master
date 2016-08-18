from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import json
# Create your views here.

class OperatorLogin(APIView):

	def post(self, request, format=None):
		data = {}
		data['code'] = False
		data['message'] = None
		data['privilege'] = None
		data['content'] = None
		data['pageaddress'] = None

		if not request.POST.get('UserID'):
			data['message'] = 'Please enter UserID'
			return Response(data)
		else:
			userid = request.POST.get('UserID')

		if not request.POST.get('Password'):
			data['message'] = 'Please enter Password'
			return Response(data)
		else:
			password = request.POST.get('Password')

		user = User.objects.filter(UserID=userid, Password=password)

		if len(user) == 0:
			data['message'] = 'not a valid user'
			return Response(data)
		else:
			data['code'] = False
			data['message'] = 'this is message'
			data['privilege'] = user[0].UserID
			data['content'] = user[0].Email
			data['pageaddress'] = user[0].Url
			return Response(data)

	def get(self, request, format=None):
		data = {}
		data['code'] = False
		data['message'] = 'test get'
		data['privilege'] = 'high'
		data['content'] = 'this is content'
		data['pageaddress'] = 'here should include a url'
		#return Response(data)
		return HttpResponse(json.dumps(data), content_type="application/json")

class OperatorChgPsw(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'OperatorChgPsw'})

class OperatorReg(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'OperatorReg'})

class AdminLogin(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'AdminLogin'})

class AdminChgPsw(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'AdminChgPsw'})

class AdminReg(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'AdminReg'})

class ResearcherLogin(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'ResearcherLogin'})

class ResearcherChgPsw(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'ResearcherChgPsw'})

class ResearcherReg(APIView):
	def post(self, request, format=None):
		#
		#include method here
		#
		return Response({'Response':'ResearcherReg'})