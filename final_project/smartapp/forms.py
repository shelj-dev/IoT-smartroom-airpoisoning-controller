from django import forms
from smartapp.models import Limit
 

class limitForm(forms.ModelForm):
    class Meta:
        model = Limit
        fields =['threshold']