from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('login/', custom_login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('recruiter_index/', recruiter_index, name='recruiter_index'),
    path('job_seeker_index/', job_seeker_index, name='job_seeker_index'),
    path('job_detail/<int:job_id>/', job_detail, name='job_detail'),
    path('register/', register_view, name='register'),
    path('update_personal_details/', update_personal_details, name='update_personal_details'),
    path('update_recruiter_details/', update_recruiter_details, name='update_recruiter_details'),
    path('add_education/', add_education, name='add_education'),
    path('upload_resume/', upload_resume, name='upload_resume'),
    path('add_experience/', add_experience, name='add_experience'),
    path('user_educations/', user_educations, name='user_educations'),
    path('add_company/', add_company, name='add_company'),
    path('create_job/', create_job, name='create_job'),
    path('feedback_page/', feedback_page, name='feedback_page'),
    path('user_applications/', user_applications, name='user_applications'),

    path('jobs/', job_list, name='job_list'),
    path('jobs/delete/<int:job_id>/', delete_job, name='delete_job'),
     path('application_list/', application_list, name='list_applications'),
    path('application_list/update_status/<int:application_id>/', update_status, name='update_status'),
    path('recruiter_feedback/', recruiter_feedback, name='recruiter_feedback'),

    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user_list/', user_list, name='user_list'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('job_list/', job_list, name='job_list'),
    path('delete_job/<int:job_id>/', delete_job, name='delete_job'),
    path('admin_application_list/', admin_application_list, name='admin_application_list'),
    path('delete_application/<int:application_id>/', delete_application, name='delete_application'),
    path('feedback_list/', feedback_list, name='admin_feedback'),
    path('update_reply/<int:feedback_id>/', update_reply, name='update_reply'),
]