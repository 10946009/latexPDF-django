from django import forms
from django.forms import ModelForm
from outfile.models import Problem, InputOutput

class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'
        labels = {
            'title': '題目名稱',
            'statement': '題目敘述',
            'sample_input': '範例輸入',
            'sample_output': '範例輸出',
            'hint': '提示',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control'}),
            'sample_input': forms.Textarea(attrs={'class': 'form-control'}),
            'sample_output': forms.Textarea(attrs={'class': 'form-control'}),
            'hint': forms.Textarea(attrs={'class': 'form-control'}),
        }