from django import forms 
from .models import Login,Projects


class signupForm(forms.ModelForm): 
	class Meta: 
		model = Login 
		fields="__all__"
		widgets = {
        'password': forms.PasswordInput(),
		}
		


class loginForm(forms.ModelForm): 
	class Meta: 
		model = Login 
		fields=("name","password","ptype")
		widgets = {
        'password': forms.PasswordInput(),
		}

class post_project_form(forms.ModelForm):
	class Meta:
		model = Projects
		fields =("name","desc","skills","max_payment","days")
		widgets={
			'name':forms.TextInput(attrs={'class': "input-lg"}),
			'desc':forms.Textarea(attrs={'class': "input-lg"}),
			'skills':forms.TextInput(attrs={'class': "input-lg"}),
			'max_payment':forms.NumberInput(attrs={'class': "input-lg"}),
			'days':forms.NumberInput(attrs={'class': "input-lg"}),

		}
		
		