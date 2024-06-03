from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from jobapp.models import SignUp,AboutCompany,PostJobs,ApplyJobs
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
# Create your views here.

def index(request):
    return render(request,'jobapp/index.html')

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '')
        gender = request.POST.get('gender', '')
        role = request.POST.get('role', '')

        user = SignUp(username=username,email=email,password=password,phone=phone,gender=gender,role=role)
        user.save()
        return redirect('../login.html')
    return render(request,'jobapp/signup.html')

# def user_login(request):
#     registrations = SignUp.objects.all()
#     email = ""
#     password=""
#     if request.method == "POST":
#         email = request.POST.get('email','')
#         password = request.POST.get('password','')
#     for registration in registrations:
#         d_email = registration.email
#         role = registration.role
#         d_password = registration.password
#         if d_email == email and d_password == password:
#             if role == 'recruiter':
#               return redirect('../../recruiter.html')
#             else:
#                 return redirect('../../applicant.html')
#     return render(request, 'jobapp/login.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        try:
            user = SignUp.objects.get(email=email, password=password)
        except SignUp.DoesNotExist:
            print('Invalid email or password.')
            return redirect('login')  # Redirect back to login page with error message
        
        # Store the user's ID in the session
        request.session['user_id'] = user.id
        
        if user.role == 'recruiter':
            return redirect('../recruiters/recruiter.html')
        else:
            return redirect('../applicants/applicant.html')
    
    return render(request, 'jobapp/login.html')

def recruiter(request):
    # Get the current user's ID from the session
    user_id = request.session.get('user_id')
    
    if user_id:
        # Retrieve the current user's posted jobs
        jobs = PostJobs.objects.filter(user_id=user_id)
        return render(request, 'jobapp/recruiters/recruiter.html', {'jobs': jobs})
    else:
        # Handle the case where the user is not logged in
        # Redirect them to the login page or display an error message
        return redirect('login')
# def aboutcomp(request):
#     if request.method =='POST':
#         company_name = request.POST.get('company_name', '')
#         about_company = request.POST.get('about_company', '')
#         founder_name = request.POST.get('founder_name', '')
#         headquarters_location = request.POST.get('headquarters_location', '')
       
#         company = AboutCompany(company_name=company_name, about_company=about_company, founder_name=founder_name, headquarters_location=headquarters_location)
#         company.save()
#         msg = "Company Information Saved Successfully."
#         return render(request, 'jobapp/recruiters/aboutcomp.html', {'msg': msg})
#     return render(request, 'jobapp/recruiters/aboutcomp.html')


# def postjob(request):
#     if request.method =='POST':
#         job_title = request.POST.get('job_title', '')
#         address = request.POST.get('address', '')
#         salary_low = request.POST.get('salary_low', '')
#         salary_high = request.POST.get('salary_high', '')
#         last_date = request.POST.get('last_date', '')

#         job = PostJobs(job_title=job_title, address=address, salary_low=salary_low, salary_high=salary_high, last_date=last_date)
#         job.save()
#         msg = "Job Posted Successfully."
#         return render(request, 'jobapp/recruiters/postjob.html', {'msg': msg})
#     return render(request, 'jobapp/recruiters/postjob.html')
def aboutcomp(request):
    if request.method =='POST':
        # Get the current user's ID from the session
        user_id = request.session.get('user_id')
        
        if user_id:
            # Retrieve the current user from the database
            current_user = SignUp.objects.get(id=user_id)
            
            company_name = request.POST.get('company_name', '')
            about_company = request.POST.get('about_company', '')
            founder_name = request.POST.get('founder_name', '')
            headquarters_location = request.POST.get('headquarters_location', '')
           
            # Create the AboutCompany instance associated with the current user
            company = AboutCompany(user=current_user, company_name=company_name, about_company=about_company, founder_name=founder_name, headquarters_location=headquarters_location)
            company.save()
            msg = "Company Information Saved Successfully."
            return render(request, 'jobapp/recruiters/aboutcomp.html', {'msg': msg})
        else:
            # Handle the case where the user is not logged in
            # Redirect them to the login page or display an error message
            return redirect('login')  # or return HttpResponse("Please log in first")
    
    return render(request, 'jobapp/recruiters/aboutcomp.html')

def postjob(request):
    if request.method =='POST':
        # Get the current user's ID from the session
        user_id = request.session.get('user_id')
        
        if user_id:
            # Retrieve the current user from the database
            current_user = SignUp.objects.get(id=user_id)
            
            job_title = request.POST.get('job_title', '')
            address = request.POST.get('address', '')
            salary_low = request.POST.get('salary_low', '')
            salary_high = request.POST.get('salary_high', '')
            last_date = request.POST.get('last_date', '')

            # Create the PostJobs instance associated with the current user
            job = PostJobs(user=current_user, job_title=job_title, address=address, salary_low=salary_low, salary_high=salary_high, last_date=last_date)
            job.save()
            msg = "Job Posted Successfully."
            return render(request, 'jobapp/recruiters/postjob.html', {'msg': msg})
        else:
            # Handle the case where the user is not logged in
            # Redirect them to the login page or display an error message
            return redirect('login')  # or return HttpResponse("Please log in first")
    
    return render(request, 'jobapp/recruiters/postjob.html')

def applicant(request):
    jobs = PostJobs.objects.all()
    return render(request,'jobapp/applicants/applicant.html',{'jobs': jobs})

def job_details(request, job_id):
    # Retrieve the job details
    job = get_object_or_404(PostJobs, pk=job_id)
    
    # Retrieve the company information associated with the job
    company = AboutCompany.objects.get(user=job.user)
    
    return render(request, 'jobapp/applicants/job_details.html', {'job': job, 'company': company})


def apply_job(request, job_id):
    # Retrieve the job object
    job = get_object_or_404(PostJobs, pk=job_id)
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        current_user = SignUp.objects.get(id=user_id)
        # Extract form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        passout_year = request.POST.get('passout_year')
        experience = request.POST.get('experience')
        resume = request.FILES.get('resume')
        resume_folder = 'resumes'
        # Create the folder if it doesn't exist
        if not os.path.exists(resume_folder):
            os.makedirs(resume_folder)

        # Save the resume file to the folder
        resume_path = os.path.join(resume_folder, resume.name)
        with open(resume_path, 'wb') as f:
            for chunk in resume.chunks():
                f.write(chunk)
        # Save the data to the ApplyJob model
        application = ApplyJobs(
            username=username,
            email=email,
            passout_year=passout_year,
            experience=experience,
            resume=resume_path,
            job=job,
            user = current_user
        )
        application.save()

        # Optionally, you can add a success message or redirect to a success page
        return redirect('applicant')  # You can redirect to a success page here

    else:
        # Render the form for applying to the job
        return render(request, 'jobapp/applicants/apply_job.html', {'job': job})
    
def job_applicants(request, job_id):
    # Fetch all applicants for the selected job
    applicants = ApplyJobs.objects.filter(job_id=job_id)
    return render(request, 'jobapp/recruiters/job_applicants.html', {'applicants': applicants})    

def accept_applicant(request):
    if request.method == 'POST':
        applicant_id = request.POST.get('applicant_id')
        status = request.POST.get('status')
        
        # Update applicant status in the database
        applicant = ApplyJobs.objects.get(pk=applicant_id)
        applicant.status = status  # Set status to "accept"
        applicant.save()
        
        # Render the same template
        return render(request, 'jobapp/recruiters/job_applicants.html')  # Adjust the template path if needed

def reject_applicant(request):
    if request.method == 'POST':
        applicant_id = request.POST.get('applicant_id')
        status = request.POST.get('status')
        
        # Update applicant status in the database
        applicant = ApplyJobs.objects.get(pk=applicant_id)
        applicant.status = status  # Set status to "reject"
        applicant.save()
        
        # Render the same template
        return render(request, 'jobapp/recruiters/job_applicants.html')



def job_status_view(request):
    # Fetch job titles and their status for the current user
    jobs_with_status = []
    user_id = request.session.get('user_id')  # Get the current logged-in user
    
    # Filter jobs applied by the current user
    applied_jobs = ApplyJobs.objects.filter(user=user_id)
    
    for applied_job in applied_jobs:
        jobs_with_status.append((applied_job.job.job_title, applied_job.status))
    
    return render(request, 'jobapp/applicants/job_status.html', {'jobs_with_status': jobs_with_status})