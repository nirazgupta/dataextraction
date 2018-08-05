from django import forms

class NewBusinessForm(forms.Form):
    business_name = forms.CharField(label='Business Name', max_length=100)
    business_phone = forms.CharField(label='Phone Number', max_length=100)
    business_email = forms.EmailField(label='Email Address', max_length=100)
    business_website = forms.CharField(label='Web Site', max_length=100)