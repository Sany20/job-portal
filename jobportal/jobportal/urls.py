"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jobapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login.html/',views.user_login,name='login'),
    path('signup.html/',views.signup,name='signup'),
    path('recruiters/recruiter.html/',views.recruiter,name='recruiter'),
    path('aboutcomp.html/',views.aboutcomp,name='aboutcomp'),
    path('postjob.html/',views.postjob,name='postjob'),
    path('applicants/applicant.html',views.applicant,name='applicant'),
    path('job/<int:job_id>/', views.job_details, name='job_details'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('job_applicants/<int:job_id>/', views.job_applicants, name='job_applicants'),
    path('accept/', views.accept_applicant, name='accept_applicant'),
    path('reject/', views.reject_applicant, name='reject_applicant'),
    path('job_status/', views.job_status_view, name='job_status'),
]
