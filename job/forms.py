from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

#--------SIGN UP--------------
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'user_type', 'email', 'username', 'password1', 'password2', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['user_type'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['profile_picture'].widget.attrs['class'] = 'form-control-file'

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture']

#---------Educational Qualification------------
class EducationForm(forms.ModelForm):
    LEVEL_CHOICES = [
        ('Tenth', 'Tenth'),
        ('Twelth', 'Twelth'),
        ('Graduation', 'Graduation'),
        ('Post Graduation', 'Post Graduation'),
        ('Doctoral', 'Doctoral'),
        ('Post Doctoral', 'Post Doctoral'),
    ]
    
    level = forms.ChoiceField(choices=LEVEL_CHOICES)

    class Meta:
        model = Education
        fields = ['level', 'institution', 'from_year', 'to_year', 'percentage']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['role', 'company', 'from_year', 'to_year']

#----------Recruiter-------------------------

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['user']  # Exclude user field as it will be set automatically in the view
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'})
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']