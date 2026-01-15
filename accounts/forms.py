
from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))

    class Meta:
        model = Account
        fields =['first_name','last_name','username','email']
        widgets = {
            'first_name':forms.TextInput(attrs={
                'placeholder':'Enter First Name',
                'class':'form-control'
            }),
            'last_name':forms.TextInput(attrs={
                'placeholder':'Enter Last Name',
                'class':'form-control'
            }),
            'username':forms.TextInput(attrs={
                'placeholder':'Enter Username',
                'class':'form-control'
            }),
            'email':forms.EmailInput(attrs={
                'placeholder':'Enter Email',
                'class':'form-control'
            })
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password must be same")
        if len(password)<8:
            raise forms.ValidationError("Password length must be atleast 8")
        return cleaned_data
        

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    
class ForgotPageForm(forms.Form):
    email = forms.EmailField()
    
    
class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        
        if password!=confirm_password:
            raise forms.ValidationError('Password and Confirm Password must be same')
        
        return cleaned_data