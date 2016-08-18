<<<<<<< HEAD
<<<<<<< HEAD
# Django_Backend
bigdata platform's backend based django rest_framework
=======
django_backend
===================

This is platform's backend based on django rest_framework.

------------
Installation
------------
    
1. To install Django:
    
    https://www.djangoproject.com/
    
2. To install Django rest_framework:
    
    http://www.django-rest-framework.org/
    
--------------
文件结构：
--------------
    
    目录结构：
    Server
      
      server              #项目配置文件目录
        url.py            #所有url配置文件
        setting.py        #项目设置文件
        ...
      
      users               #用户部分目录，对应于API文档中的一级目录（1 用户部分）
        models.py         #定义与数据库（mysql）对应的模型，如不需要数据库则不用修改
        views_XXX.py      #定义视图，里面包含获取数据的类和方法，XXX代表API文档中的二级目录（1.1  用户操作）。文件中定义的类的名称代表的是API文档中的三级目录（1.1.1 运行人员登录）。
        serializers.py    #将数据库中获取的数据进行序列化
      
      TrafficMonitor
        models.py 
        ...
      ...
    
--------------
Note：
--------------
    
    其他地方的设置好了，要修改的地方就只每个应用中的views_XXX.py文件。
    views_XXX.py 中定义了与接口对于的类，继承APIView。
    通过重写该类的get，post等方法实现类的获取数据功能。
    具体可以可以参考users.views_user_operation.OperatorLogin中的实现方法。
    
>>>>>>> Update README.md
=======
# Django_Backend
bigdata platform's backend based django rest_framework
>>>>>>> df42a9685f2820b7f7c8abab8a52fe9c1e590fbe
