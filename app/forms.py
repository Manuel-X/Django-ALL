from django import forms     # built in forms provided by django

from .models import Store,Item   # import Store and Item models

from django.contrib.auth.models import User    # import user model

from django.contrib.auth.forms import UserCreationForm



class StoreForm(forms.ModelForm):   # method to link form with model
	class Meta:					    # StoreForm contents is same as model object content
		model = Store
		#fields = '__all__'
		#fields = ['name','location']
		exclude = ['owner','slug']

#class StoreForm(forms.Form)  ##form not linked with model, attributes should be initialized manually
	#name = models.CharField(max_length = 30)
	#location = models.CharField(max_length = 30)
	#description = models.TextField()


class ItemForm(forms.ModelForm):   
	class Meta:					    
		model = Item
		exclude = ['store','slug']




class SignupForm(forms.ModelForm): 
	email = forms.EmailField(required=True) # overwrite email field should be written before class Meta:
	class Meta:
		model = User 
		fields = ['username', 'password', 'first_name', 'email']  #username and password are compulsary
		widgets = {                          # widgets for all desired fields
		'password': forms.PasswordInput()
		}

class SigninForm(forms.Form):
		username = forms.CharField(required=True)  
		password = forms.CharField(widget=forms.PasswordInput(),required=True) #widget for password only
		fields = ['username','password']

