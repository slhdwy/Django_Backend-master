from django.db import models

#Create your models here.
class dataset(models.Model):
       datasetid = models.IntegerField(primary_key=True, default=0)
       datasetname = models.CharField(max_length=50, default=' ')
       username = models.CharField(max_length=50, default=' ')
       status = models.CharField(max_length=20, default=' ')
       category = models.CharField(max_length=50, default=' ')
       source = models.CharField(max_length=50, default=' ')
       anonymization = models.CharField(max_length=20, default=' ')
       releasedate = models.CharField(max_length=20, default=' ')

class datacolreq(models.Model):
       username = models.CharField(max_length=50, primary_key=True)
       datasetname = models.CharField(max_length=100)
       srcport = models.CharField(max_length=10)
       dstport = models.CharField(max_length=10)
       srcip = models.CharField(max_length=100)
       dstip = models.CharField(max_length=100)
       pro = models.CharField(max_length=50)
       link = models.CharField(max_length=10)
       num = models.CharField(max_length=10)
       date = models.CharField(max_length=20)
       time = models.CharField(max_length=10)
       duration = models.CharField(max_length=10)
       period = models.CharField(max_length=10)