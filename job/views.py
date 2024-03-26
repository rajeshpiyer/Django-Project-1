from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMessage

def index(request):
    if 'search' in request.GET:
        search_query = request.GET.get('search')
        jobs = Job.objects.filter(title__icontains=search_query)
    else:
        jobs = Job.objects.all()
    return render(request, 'index.html', {'jobs': jobs})
#Login
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
                
            if user.user_type == 'recruiter':
                return redirect('recruiter_index')
            elif user.user_type == 'job_seeker':
                return redirect('job_seeker_index')
            else:
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

#Landing Pages------------------

@login_required
def admin_dashboard(request):
    user_count = CustomUser.objects.count()
    job_count = Job.objects.count()
    application_count = Application.objects.count()
    feedback_count = Feedback.objects.count()

    context = {
        'user_count': user_count,
        'job_count': job_count,
        'application_count': application_count,
        'feedback_count': feedback_count,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def recruiter_index(request):
    # Your recruiter index view logic here
    return render(request, 'recruiter_index.html')

@login_required
def job_seeker_index(request):
    if 'search' in request.GET:
        search_query = request.GET.get('search')
        jobs = Job.objects.filter(title__icontains=search_query)
    else:
        jobs = Job.objects.all()

    applications = Application.objects.filter(user=request.user)
    applied_job_ids = applications.values_list('job_id', flat=True)
    applied_jobs = Job.objects.filter(id__in=applied_job_ids)

    return render(request, 'job_seeker_index.html', {'jobs': jobs, 'applied_job_ids':applied_job_ids})



@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            cover_letter = form.cleaned_data['cover_letter']  # Corrected field name
            user = request.user
            application = Application.objects.create(user=user, job=job, cover_letter=cover_letter)
            #SENDING MAIL
            role = application.job.title
            applicant = application.user
            name = ""+applicant.first_name + "" + applicant.last_name
            email = applicant.email        
            sender = application.job.user.email
            recipient = [email]
            resume = Resume.objects.filter(user=request.user).order_by('-id').first()
            file_path = resume.resume
            qualifications = Education.objects.filter(user=request.user)

            # TO APPLICANT
            subject_to_applicant = "APPLICATION SUBMITTED FOR : " + role
            message_to_applicant = "Congratulations!!\nYour Application is Sumbitted for "+ role +"\n Good Luck!"
            send_mail(subject_to_applicant, message_to_applicant, sender, recipient)

            #TO RECRUITER
            subject_to_recruiter = "NEW APPLICATION RECIEVED FOR : " + role
            message_to_recruiter = "New Application recieved for : "+role
            message_to_recruiter += "\nApplicant Name : "+name
            message_to_recruiter += "\nCovering Letter : \n"+application.cover_letter
            message_to_recruiter += "\nEducational Qualifications : \n"
            for q in qualifications:
                message_to_recruiter += ""+q.level+" : "+q.institution+" : "+str(q.percentage)+"%\n"
            message_to_recruiter += "\n\n Detailed Resume is Attached"

            email_to_recruiter = EmailMessage(subject_to_recruiter, message_to_recruiter, sender, [sender])
            email_to_recruiter.attach_file(str(file_path))
            email_to_recruiter.send()
            
            return redirect('user_applications') 
    else:
        form = ApplicationForm()
    
    return render(request, 'job_detail.html', {'job': job, 'form': form})

#Registration---------------------------

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Please login.')

            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration.html', {'form': form})

def update_personal_details(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('job_seeker_index')  # Redirect to home page after successful update
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'update_personal_details.html', {'form': form,'user':user})
#----------------------------------------------
#----EDUCATIONAL QUALIFICATIONS---------------

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user  # Assuming you have authentication in place
            education.save()
            messages.success(request, 'Added Successfully')
            return redirect('user_educations')  # Redirect to a success URL
        messages.success(request, 'Form is not valid')
    else:
        form = EducationForm()
    
    return render(request, 'education_form.html', {'form': form})

@login_required
def user_educations(request):
    educations = Education.objects.filter(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    last_resume = Resume.objects.filter(user=request.user).order_by('-id').first()  # Retrieve the last uploaded resume
    return render(request, 'user_educations.html', {'educations': educations, 'experiences': experiences, 'resume': last_resume})


@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('user_educations')  # Redirect to a page showing uploaded resumes
    else:
        form = ResumeForm()
    
    return render(request, 'upload_resume.html', {'form': form})

def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user  # Assuming user is authenticated
            experience.save()
            return redirect('user_educations')  # Redirect to a list view of experiences
    else:
        form = ExperienceForm()
    return render(request, 'add_experience.html', {'form': form})

#----------Recruiter------------------------------


def update_recruiter_details(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('recruiter_index')  # Redirect to home page after successful update
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'update_recruiter_details.html', {'form': form,'user':user})

@login_required
def add_company(request):
    # Get companies associated with the current user
    user_companies = Company.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            return redirect('recruiter_index')  # Redirect to a page showing company list
    else:
        form = CompanyForm()
    
    return render(request, 'company_form.html', {'form': form, 'user_companies': user_companies})

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('job_list')  # Redirect to a page showing job list
    else:
        form = JobForm()
    
    return render(request, 'job_form.html', {'form': form})

@login_required
def feedback_page(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_page')
    else:
        form = FeedbackForm()

    feedbacks = Feedback.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'feedbacks': feedbacks,
    }
    return render(request, 'feedback_page.html', context)

@login_required
def user_applications(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'user_applications.html', {'applications': applications})

@login_required
def job_list(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.user == request.user:
        job.delete()
    return redirect('job_list')

@login_required
def application_list(request):
    applications = Application.objects.filter(job__user=request.user)
    return render(request, 'application_list.html', {'applications': applications})

@login_required
def recruiter_index(request):
    applications = Application.objects.filter(job__user=request.user)
    return render(request, 'recruiter_index.html', {'applications': applications})




@login_required
def update_status(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()

        #SENDING MAIL
        role = application.job.title
        applicant = application.user
        name = ""+applicant.first_name + applicant.last_name
        email = applicant.email        

        sender = application.job.user.email
        recipient = [email]
        # TO APPLICANT
        subject_to_applicant = "RE: STATUS UPDATED IN YOUR JOB APPLICATION : " + role
        if new_status == "shortlisted":
            message_to_applicant = "Congratulations!!\nHappy to inform that you are Shortlisted for thi role.\n Our HR team will contact you for further procedures."
        else:
            message_to_applicant = "Sorry, You're not shortlisted.\nBetter luck next time"
        send_mail(subject_to_applicant, message_to_applicant, sender, recipient)

        #TO RECRUITER
        subject_to_recruiter = "RE: STATUS UPDATED IN JOB APPLICATION : " + role
        message_to_recruiter = "Status Updated for :"+name+" in recruitment for : "+role+" as "+new_status
        send_mail(subject_to_recruiter, message_to_recruiter, sender, [sender])

    return redirect('application_list')

@login_required
def recruiter_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_page')
    else:
        form = FeedbackForm()

    feedbacks = Feedback.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'feedbacks': feedbacks,
    }
    return render(request, 'recruiter_feedback.html', context)

@login_required
def user_list(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user_list.html', context)
@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'success': True})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def admin_job_list(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
    return render(request, 'admin_job_list.html', context)

@login_required
def delete_job(request, job_id):
    if request.method == 'POST':
        try:
            job = Job.objects.get(pk=job_id)
            job.delete()
            return JsonResponse({'success': True})
        except Job.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
@login_required
def delete_application(request, application_id):
    if request.method == 'POST':
        try:
            application = Application.objects.get(pk=application_id)
            application.delete()
            return JsonResponse({'success': True})
        except Application.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Application not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
@login_required
def admin_application_list(request):
    applications = Application.objects.all()
    context = {
        'applications': applications
    }
    return render(request, 'admin_application_list.html', context)

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all()  # Fetch feedbacks in descending order of creation
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'feedback_list.html', context)

@login_required
def update_reply(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    if request.method == 'POST':
        reply = request.POST.get('reply')
        feedback.reply = reply
        feedback.save()
        return redirect('admin_feedback')  # Redirect back to the feedback list page
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

