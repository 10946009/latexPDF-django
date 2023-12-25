from django import forms
from django.forms import ModelForm ,inlineformset_factory
from outfile.models import Problem, InputOutput
from django.forms import modelformset_factory
class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'
        labels = {
            'title': '題目名稱',
            'timelimit': '時間限制',
            'statement': '題目敘述',
            'hint': 'hint',
            'spec': 'spec',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'timelimit': forms.NumberInput(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control'}),
            'hint': forms.Textarea(attrs={'class': 'form-control'}),
            'spec': forms.Textarea(attrs={'class': 'form-control'}),
        }

class InputOutputForm(ModelForm):
    class Meta:
        model = InputOutput
        fields = "problem","input","output"
        labels = {
            'problem': '題目',
            'input': '輸入',
            'output': '輸出',
        }
        widgets = {
            'problem': forms.Select(attrs={'class': 'form-control'}),
            'input': forms.Textarea(attrs={'class': 'form-control'}),
            'output': forms.Textarea(attrs={'class': 'form-control'}),
        }