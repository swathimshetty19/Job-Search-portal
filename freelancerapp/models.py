from django.db import models
# Create your models here.
from django.utils import timezone

class Login(models.Model): # The Category table name that inherits models.Model
    name = models.CharField(max_length=100,primary_key=True) #Like a varchar
    password = models.CharField(max_length=100)
    ptype = models.CharField(max_length=100,default='search')
    def __str__(self):
        return self.name #name to be shown when called

class Users(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    firstname= models.CharField(max_length=100,null=True)
    lastname= models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=254,null=True)
    phone = models.IntegerField(default=0)
    experience= models.CharField(max_length=254,null=True)
    skills=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Skills(models.Model):
    skill=models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.skill

class Projects(models.Model):
	project_id = models.CharField(max_length=100,primary_key=True)
	name = models.CharField(max_length=100)
	desc = models.TextField()
	skills = models.TextField()
	status = models.CharField(max_length=100,default='') #either fresh or taken
	leader = models.CharField(max_length=100)
	members = models.TextField()
	mem_needed = models.IntegerField(default=0)
	applied = models.TextField()
	min_payment = models.CharField(max_length=50,default='')
	max_payment = models.CharField(max_length=50)
	days = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name

