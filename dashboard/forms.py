from django import forms
from dashboard.models import AiUser
from django.core.validators import RegexValidator

class SignUpForm(forms.ModelForm):

    class Meta:
        model = AiUser
        fields = ('name','email', 'password', 'department', 'age')
        exclude = ['role']
        extra_kwargs = {'password': {'write_only': True}}
        
        error_css_class = 'error_msg'
        required_css_class = "required"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'register_form_content'}),
            'email': forms.TextInput(attrs={'class': 'register_form_content'}),
            'department': forms.TextInput(attrs={'class': 'register_form_content'}),
            'age': forms.TextInput(attrs={'class': 'register_form_content'}),
            'password': forms.PasswordInput(attrs={'class': 'register_form_content'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-content'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-content'}))
    error_css_class = 'error_msg'