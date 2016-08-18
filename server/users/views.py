#coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from users.models import Operator
from users.models import Administrator
from users.models import Researcher
from users.models import UserProfile
from django import forms
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import MySQLdb
import json

# Create your views here.

class regist(APIView):
    def get(self, req, format=None):
      #  print "121212121"
        data = {}
        data['username'] = None
        data['password'] = None
        data['password2'] = None
        data['message'] = None
        data['email'] = None
        data['role'] = None
        data['privilege'] = None
        username = None
        password = None
        password2 = None
        email = None
        role = None
        callback = req.GET.get('callback')
      #  print "888888"
        role = req.GET.get('optionsRadiosInline')
        print("role:%s" %(role))

        if not req.GET.get('optionsRadiosInline'):
            data['message'] = 'Please Choose a Role'
            D = '%s(%s)'%(callback, json.dumps(data))
            print("Please choose a role")
            return HttpResponse(D, content_type="application/json")
        else:
            role = req.GET.get('optionsRadiosInline')
            print("role:%s" %(role))
            if not req.GET.get('username'):
                data['message'] = 'Please Enter Username'
                D = '%s(%s)'%(callback, json.dumps(data))
                print("Please enter username")
                return HttpResponse(D, content_type="application/json")
            else:
                username = req.GET.get('username')
                #把获取表单的用户名传递给session对象
                req.session['username'] = username
                print("username:%s" %(username))
                if not req.GET.get('email'):
                    data['message'] = 'Please Enter Emailaddress'
                    D = '%s(%s)'%(callback, json.dumps(data))
                    print("Please enter email")
                    return HttpResponse(D, content_type="application/json")
                else:
                    email = req.GET.get('email')
                    print("email:%s" %(email))
                    if not req.GET.get('password'):
                        data['message'] = 'Please Enter Password'
                        D = '%s(%s)'%(callback, json.dumps(data))
                        print("Please enter password")
                        return HttpResponse(D, content_type="application/json")
                    else:
                        password = req.GET.get('password')
                        print("password:%s" %(password))
                        if not req.GET.get('password2'):
                            data['message'] = 'Please Enter Password again'
                            D = '%s(%s)'%(callback, json.dumps(data))
                            print("Please enter password again")
                            return HttpResponse(D, content_type="application/json")
                        else:
                            password2 = req.GET.get('password2')
                            print("password2:%s" %(password2))
                                 #test if passwords match
                            if not (password and password2):
                                 data['message'] = 'password2 is diff from password'
                                 D = '%s(%s)'%(callback, json.dumps(data))
                                 print("password2 is diff from password")
                                 return HttpResponse(D, content_type="application/json")
                            else:
                                same_user = User.objects.filter(username=username)
                                if not len(same_user) == 0:
                                    data['message'] = 'Username exists'
                                    D = '%s(%s)'%(callback, json.dumps(data))
                                    print("Username exists")
                                    return HttpResponse(D, content_type="application/json")
                                else:
                                    user = User()
                                    user.username = username
                                    user.set_password(password)
                                    user.email = email
                                    #user.create_profile().address = 'home/' + username
                                    user.save()

                                    print("user.id:%s" %(user.id))
                                    profile = UserProfile()
                                    profile.user_id = user.id
                                    profile.address = 'home/' + username
                                    profile.major = role
                                    profile.save()
                                    print("puser.id:%s" %(profile.user_id))
                                    if role == "option1":
                                        print("choose option1")
                                        operator = Operator()
                                        operator.uesr_id = user.id
                                        operator.privilege = 1
                                        operator.save()
                                        data['username'] = username
                                        data['password'] = password
                                        data['email'] = email
                                        data['privilege'] = 1
                                        data['role'] = 'operator'
                                        data['message'] = 'Create user successfully!'
                                        D = '%s(%s)'%(callback, json.dumps(data))
                                        return HttpResponse(D, content_type="application/json")

                                    else:
                                        if role == "option2":
                                            print("choose option2")
                                            administrator = Administrator()
                                            administrator.uesr_id = user.id
                                            administrator.privilege = 1
                                            print("administrator.uesr_id:%s" %(administrator.uesr_id))
                                            print("OK!!!")
                                            administrator.save()
                                            print("choose option2")
                                            data['username'] = username
                                            data['password'] = password
                                            data['email'] = email
                                            data['privilege'] = 1
                                            data['role'] = 'administrator'
                                            data['message'] = 'Create user successfully!'
                                            D = '%s(%s)'%(callback, json.dumps(data))
                                            return HttpResponse(D, content_type="application/json")

                                        else:
                                            if role == "option3":
                                                print("choose option3")
                                                researcher = Researcher()
                                                researcher.uesr_id = user.id
                                                researcher.privilege = 1
                                                researcher.save()
                                                data['username'] = username
                                                data['password'] = password
                                                data['email'] = email
                                                data['privilege'] = 1
                                                data['role'] = 'researcher'
                                                data['message'] = 'Create user successfully!'
                                                D = '%s(%s)'%(callback, json.dumps(data))
                                                return HttpResponse(D, content_type="application/json")
                                            else:
                                                data['message'] = 'Error!'
                                                D = '%s(%s)'%(callback, json.dumps(data))
                                                print("Error!")
                                                return HttpResponse(D, content_type="application/json")

#登陆
class login(APIView):
    def get(self, req, format=None):
        print "liwei0"
        data = {}
        data['username'] = None
        data['password'] = None
        data['role'] = None
        data['message'] = None
        username = None
        password = None
        role = None
        callback = req.GET.get('callback')
        print "liwei"
        role = req.GET.get('optionsRadiosInline')
        print("role:%s" %(role))
        if not req.GET.get('optionsRadiosInline'):
           data['message'] = 'Please choose a role'
           D = '%s(%s)'%(callback, json.dumps(data))
           print("Please choose a role")
           return HttpResponse(D, content_type="application/json")
        else:
           role = req.GET.get('optionsRadiosInline')
           if not req.GET.get('username'):
                data['message'] = 'Please enter username'
                D = '%s(%s)'%(callback, json.dumps(data))
                print("Please enter username")
                return HttpResponse(D, content_type="application/json")
           else:
                username = req.GET.get('username')
                #把获取表单的用户名传递给session对象
                req.session['username'] = username
                print("username:%s" %(username))
                if not req.GET.get('password'):
                    data['message'] = 'Please enter password'
                    D = '%s(%s)'%(callback, json.dumps(data))
                    print("Please enter password")
                    return HttpResponse(D, content_type="application/json")
                else:
                    password = req.GET.get('password')
                    print("password:%s" %(password))
                    UserObj = User.objects.filter(username=username)
                    if len(UserObj) == 0:
                        data['message'] = 'invalid user'
                        D = '%s(%s)'%(callback, json.dumps(data))
                        print("invalid user")
                        return HttpResponse(D, content_type="application/json")
                    else:
                        is_staff = UserObj[0].is_staff
                        if is_staff == 0:
                            data['message'] = "Check not pass!"
                            D = '%s(%s)'%(callback, json.dumps(data))
                            print("message:%s" %(data['message']))
                            return HttpResponse(D, content_type="application/json")
                        else:
                            if role == "option1":
                                 print("option1!!!")
                                 OperatorObj = User.objects.filter(username=username)
                                 if len(OperatorObj) == 0:
                                     data['message'] = 'invalid user'
                                     D = '%s(%s)'%(callback, json.dumps(data))
                                     print("invalid user")
                                     return HttpResponse(D, content_type="application/json")
                                 else:
                                     OperatorNum = Operator.objects.filter(uesr_id=OperatorObj[0].id)
                                     if len(OperatorNum) ==0:
                                         data['message'] = 'This user is not an operator!'
                                         D = '%s(%s)'%(callback, json.dumps(data))
                                         print("This user is not an operator!")
                                         return HttpResponse(D, content_type="application/json")
                                     else:
                                         if OperatorObj[0].check_password(password):
                                             data['username'] = OperatorObj[0].username
                                             data['password'] = OperatorObj[0].password
                                             data['email'] = OperatorObj[0].email
                                             data['role'] = 'operator'
                                             data['message'] = "Login success!"
                                             req.session['username'] = username
                                             D = '%s(%s)'%(callback, json.dumps(data))
                                             return HttpResponse(D, content_type="application/json")
                                         else:
                                             data['message'] = 'wrong password'
                                             D = '%s(%s)'%(callback, json.dumps(data))
                                             print("wrong password!")
                                             return HttpResponse(D, content_type="application/json")
                            else:
                                if role == "option2":
                                    print("option2!!!")
                                    AdministratorObj = User.objects.filter(username=username)
                                    if len(AdministratorObj) == 0:
                                        data['message'] = 'invalid user'
                                        D = '%s(%s)'%(callback, json.dumps(data))
                                        print("invalid user")
                                        return HttpResponse(D, content_type="application/json")
                                    else:
                                        AdministratorNum = Administrator.objects.filter(uesr_id=AdministratorObj[0].id)
                                        if len(AdministratorNum) ==0:
                                            data['message'] = 'This user is not an administrator!'
                                            D = '%s(%s)'%(callback, json.dumps(data))
                                            print("This user is not an administrator!")
                                            return HttpResponse(D, content_type="application/json")
                                        else:
                                            if AdministratorObj[0].check_password(password):
                                                data['username'] = AdministratorObj[0].username
                                                data['password'] = AdministratorObj[0].password
                                                data['email'] = AdministratorObj[0].email
                                                data['role'] = 'Administrator'
                                                data['message'] = "Login success!"
                                                D = '%s(%s)'%(callback, json.dumps(data))
                                                return HttpResponse(D, content_type="application/json")
                                            else:
                                                data['message'] = 'wrong password'
                                                D = '%s(%s)'%(callback, json.dumps(data))
                                                print("wrong password!")
                                                return HttpResponse(D, content_type="application/json")
                                else:
                                    print("option3!!!")
                                    ResearcherObj = User.objects.filter(username=username)
                                    if len(ResearcherObj) == 0:
                                        data['message'] = 'invalid user'
                                        D = '%s(%s)'%(callback, json.dumps(data))
                                        print("invalid user")
                                        return HttpResponse(D, content_type="application/json")
                                    else:
                                        ResearcherNum =Researcher.objects.filter(uesr_id=ResearcherObj[0].id)
                                        if len(ResearcherNum) ==0:
                                            data['message'] = 'This user is not a researcher!'
                                            D = '%s(%s)'%(callback, json.dumps(data))
                                            print("This user is not a researcher!")
                                            return HttpResponse(D, content_type="application/json")
                                        else:
                                             if ResearcherObj[0].check_password(password):
                                                 data['username'] = ResearcherObj[0].username
                                                 data['password'] = ResearcherObj[0].password
                                                 data['email'] = ResearcherObj[0].email
                                                 data['role'] = 'Researcher'
                                                 data['message'] = "Login success!"
                                                 D = '%s(%s)'%(callback, json.dumps(data))
                                                 return HttpResponse(D, content_type="application/json")
                                             else:
                                                 data['message'] = 'wrong password'
                                                 D = '%s(%s)'%(callback, json.dumps(data))
                                                 print("wrong password!")
                                                 return HttpResponse(D, content_type="application/json")


   #用户数据集目录+用户信息
class index2(APIView):
    def get(self, req, format=None):
        print("lcj")
        data = {}
        data['username'] = None
        data['message'] = None
        data['address'] = None
        data['role'] = None
        username = None
        message = None
        address = None
        role = None
        callback = req.GET.get('callback')
        message = req.GET.get('message')
        print("message:%s" %(message))
        if not req.GET.get('message'):
            data['message'] = 'no message received!'
            D = '%s(%s)'%(callback, json.dumps(data))
            print("have no message!")
            return HttpResponse(D, content_type="application/json")
        else:
            if not req.session.get('username', None):
                data['message'] = 'jump index fail!'
                print("jump index fail!")
                D = '%s(%s)'%(callback, json.dumps(data))
                print("session callback already!")
                return HttpResponse(D, content_type="application/json")
            else:
                username = req.session.get('username', None)
                print("jump index success!")
                print("username_index:%s" %(username))
                user = User.objects.filter(username=username)
                userr = UserProfile.objects.filter(user_id=user[0].id)
                address = userr[0].address
                role = userr[0].major
                data['username'] = username
                data['address'] = address
                data['message'] = 'jump index success!'
                data['role'] = role
                D = '%s(%s)'%(callback, json.dumps(data))
                print("session callback already!")
                return HttpResponse(D, content_type="application/json")

 #待审核用户信息
class usermanage(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        print("lcj")
        count = 0
        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='bigdata')
        cursor=Con.cursor()
        aa=cursor.execute("select auth_user.username,users_userprofile.major,auth_user.email from auth_user inner join users_userprofile on auth_user.id = users_userprofile.user_id where auth_user.is_staff = 0")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        print(aa)

        for ii in info:
            data = {}
            data['username'] = ii[0]
            data['role'] = ii[1]
            data['email'] = ii[2]
            data['num'] = aa
            count = count + 1
            packet.append(data)
        if count == 0:
            data = {}
            data['num'] = count
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

#用户审核通过
class userpass(APIView):
    parser_classes = (JSONParser,)
    def get(self, req, format=None):
        print("lcj_userpass")
        data = {}
        data['username'] = None
        username1 = None
        callback = req.GET.get('callback')
        username1 = req.GET.get('username')
        print("username:%s" %(username1))
        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='bigdata')
        cursor=Con.cursor()
        cursor.execute("update auth_user set is_staff = 1 where username = %s", username1)
        data['message'] = 'user update success!'
        D = '%s(%s)'%(callback, json.dumps(data))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

#用户审核不通过
class usernopass(APIView):
    parser_classes = (JSONParser,)
    def get(self, req, format=None):
        print("lcj_usernopass")
        data = {}
        data['username'] = None
        username1 = None
        callback = req.GET.get('callback')
        username1 = req.GET.get('username')
        print("username:%s" %(username1))
        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='bigdata')
        cursor=Con.cursor()
        UserObj = User.objects.filter(username=username1)
        userid = UserObj[0].id
        cursor.execute("delete from users_researcher where uesr_id = %s", userid)
        cursor.execute("delete from users_operator where uesr_id = %s", userid)
        cursor.execute("delete from users_administrator where uesr_id = %s", userid)
        cursor.execute("delete from users_userprofile where user_id = %s", userid)
        cursor.execute("delete from auth_user where id = %s", userid)
        data['message'] = 'user delete success!'
        D = '%s(%s)'%(callback, json.dumps(data))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")

#通过审核的用户
class userpassed(APIView):
    parser_classes = (JSONParser,)
    def get(self, request, format=None):
        print("hhh")
        count = 0
        Con=MySQLdb.connect(host='localhost',user='root',passwd='root',db='bigdata')
        cursor=Con.cursor()
        aa=cursor.execute("select auth_user.username,users_userprofile.major,auth_user.email from auth_user inner join users_userprofile on auth_user.id = users_userprofile.user_id where auth_user.is_staff = 1")
        packet=[]
        callback = request.GET.get('callback')
        info = cursor.fetchmany(aa)
        print(aa)

        for ii in info:
            data = {}
            data['username'] = ii[0]
            data['role'] = ii[1]
            data['email'] = ii[2]
            data['num'] = aa
            count = count + 1
            packet.append(data)
        if count == 0:
            data = {}
            data['num'] = count
            packet.append(data)
        D = '%s(%s)'%(callback, json.dumps(packet))
        cursor.close()
        Con.commit()
        Con.close()
        return HttpResponse(D, content_type="application/json")