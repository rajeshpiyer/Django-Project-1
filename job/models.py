from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

#--------------------------------------------------------
#-------------ALL USERS----------------------------------

class CustomUser(AbstractUser):
     # Define choices for user_type field
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('recruiter', 'Recruiter'),
        ('job_seeker', 'Job Seeker'),
    ]

    # Add your custom fields here
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')
    profile_picture = models.ImageField(upload_to='static/profile_pictures/', null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unique related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Unique related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

#--------------------------------------------------------
#-------------FOR JOB SEEKER-----------------------------


class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    from_year = models.IntegerField()
    to_year = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.level} at {self.institution} ({self.from_year} - {self.to_year})"

class Experience(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    from_year = models.IntegerField()
    to_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.role} at {self.company} ({self.from_year} - {self.to_year})"

class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"Resume of {self.user.username}"

#--------------------------------------------------------
#-------------FOR RECRUITER------------------------------

class Company(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='static/company_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_qualifications = models.TextField()
    desired_qualifications = models.TextField()
    responsibilities = models.TextField()
    application_deadline = models.DateField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    company_benefits = models.TextField()
    how_to_apply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#--------------------------------------------------------
#-------------FOR JOB SEEKER-----------------------------

class Application(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    

    def __str__(self):
        return f"Application by {self.user.username} for job {self.job.title}"

#--------------------------------------------------------
#-------------FOR ADMIN----------------------------------

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField(default="No Reply")

    def __str__(self):
        return f"Feedback from {self.user.username}"





