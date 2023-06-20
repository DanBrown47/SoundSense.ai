from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Preference

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
    def clean_file_field(self):
        uploaded_file = self.cleaned_data['file']
        filename = uploaded_file.name
        self.cleaned_data['original_filename'] = str(filename)  # Save filename into another field
        return uploaded_file

class SongForm(forms.Form):
    file = MultipleFileField()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class':"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':"form-control"}))

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['metadata','engagement','instrument','danceability','acoustics','aggressive','happy','party','relaxed','sad','tonality','reverb','gender','voice','year']
        widgets = {
            'metadata': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 0.6, 'step': 0.01, 'class':"form-control-range"}),
            'engagement': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'instrument': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 3, 'step': 0.01, 'class':"form-control-range"}),
            'danceability': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'acoustics': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'aggressive': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'happy': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'party': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'relaxed': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'sad': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'tonality': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'reverb': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'gender': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'voice': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"}),
            'year': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 1, 'step': 0.01, 'class':"form-control-range"})
        }
        labels = {
            'metadata': 'Artists and Album',
            'engagement': 'Level of Engagement',
            'aggressive': 'Aggressiveness',
            'instrument': 'Instruments used',
            'happy': 'Happiness',
            'party': 'Party Mood',
            'relaxed': 'Relaxation',
            'sad': 'Sadness',
            'reverb': 'Reverberation',
            'gender': 'Singer gender',
            'voice': 'Overall vocals percentage',
            'year': 'Time of Release'
        }

class SongUploadForm(forms.Form):
    file = forms.FileField(required=False, label='Select a file', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept':'.m4a, .mp3, .wav'}))