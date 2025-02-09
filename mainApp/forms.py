from django import forms
from mainApp.models import *

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements']

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description']


class FreelanceProjectForm(forms.ModelForm):
    
    class Meta:
        model = FreelanceProject
        fields = ['title', 'description', 'budget']
        # posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Description'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Budget'}),
        }

        labels = {
            'title': 'Project Title',
            'description': 'Project Description',
            'budget': 'Budget (₹)',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type']  # Add more fields as needed
        widgets = {
            'user_type': forms.Select(choices=User.USER_TYPE_CHOICES),
        }
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email',  'user_type']  # Add more fields if necessary
        widgets = {
            'user_type': forms.Select(choices=User.USER_TYPE_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 

class FeedPostForm(forms.ModelForm):
    class Meta:
        model = FeedPost
        fields = ['content']


# PROJECT

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'price_offer']