from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#from django.db.models.signals import post_save


# Create your models here.
class Operator(models.Model):
    uesr=models.OneToOneField(User)
    privilege = models.IntegerField()

class Administrator(models.Model):
    uesr=models.OneToOneField(User)
    privilege = models.IntegerField()

class Researcher(models.Model):
    uesr=models.OneToOneField(User)
    privilege = models.IntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    major = models.TextField(default='', blank=True)
    address = models.CharField(max_length=200,default='',blank=True)

    def __unicode__(self):
        return self.user.username

#def create_user_profile(sender, instance, created, **kwargs):
  #  """Create the UserProfile when a new User is saved"""
 #   if created:
   #     profile = UserProfile()
  #      profile.user = instance
   #     profile.save()
#post_save.connect(create_user_profile, sender=User)
