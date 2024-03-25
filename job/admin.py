from django.contrib import admin
from .models import CustomUser, Education, Experience, Resume, Company, Job, Application, Feedback

# Register your models here.
admin.site.register(CustomUser)

# For Job Seeker
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Resume)

# For Recruiter
admin.site.register(Company)
admin.site.register(Job)

# For Admin
admin.site.register(Application)
admin.site.register(Feedback)
