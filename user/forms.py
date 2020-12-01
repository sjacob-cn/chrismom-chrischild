from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
  
