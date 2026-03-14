"""
create forms
create super user
add new models into admin.py
in admin page create a threshold (Limit)
"""


from django import forms
from smartapp.models import Limit

# SAFE_LIMIT = 300   

class limitForm(forms.ModelForm):
    class Meta:
        model = Limit
        fields =['threshold']