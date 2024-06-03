from django.db import models

# Create your models here.

from django.conf import settings

# Create your models here.
class SignUp(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, default='+919822331994')
    gender = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class AboutCompany(models.Model):
    user = models.ForeignKey(SignUp, on_delete=models.CASCADE, default=None, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    about_company = models.TextField()
    founder_name = models.CharField(max_length=255)
    headquarters_location = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name

class PostJobs(models.Model):
    user = models.ForeignKey(SignUp, on_delete=models.CASCADE, default=None, blank=True, null=True)
    job_title = models.CharField(max_length=255)
    address = models.TextField()
    salary_low = models.IntegerField()
    salary_high = models.IntegerField()
    last_date = models.DateField()

    def __str__(self):
        return self.job_title
    
class ApplyJobs(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    passout_year = models.CharField(max_length=255)
    experience = models.IntegerField()
    resume = models.FileField()
    status = models.CharField(max_length=255,default="Pending")
    job = models.ForeignKey(PostJobs, on_delete=models.CASCADE, default=None, blank=True, null=True)   
    user = models.ForeignKey(SignUp, on_delete=models.CASCADE, default=None, blank=True, null=True)