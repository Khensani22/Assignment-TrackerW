from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['module_name', 'assignment_name', 'description', 'due_date', 'status']
