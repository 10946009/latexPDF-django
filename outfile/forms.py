from django import forms
from django.forms import ModelForm ,inlineformset_factory
from outfile.models import Problem, InputOutput
from django.forms import formset_factory
class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'
        labels = {
            'title': '題目名稱',
            'timelimit': '時間限制',
            'statement': '題目敘述',
            'input_format': '範例輸入',
            'output_format': '範例輸出',
            'hint': 'hint',
            'spec': 'spec',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'timelimit': forms.NumberInput(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control'}),
            'input_format': forms.Textarea(attrs={'class': 'form-control'}),
            'output_format': forms.Textarea(attrs={'class': 'form-control'}),
            'hint': forms.Textarea(attrs={'class': 'form-control'}),
            'spec': forms.Textarea(attrs={'class': 'form-control'}),
        }

class InputOutputForm(ModelForm):
    class Meta:
        model = InputOutput
        fields ="input","output"
        labels = {
            'input': '輸入',
            'output': '輸出',
        }
        widgets = {
            'input': forms.Textarea(attrs={'class': 'form-control'}),
            'output': forms.Textarea(attrs={'class': 'form-control'}),
        }

InputOutputFormSet = inlineformset_factory(Problem, InputOutput, form=InputOutputForm, extra=1, can_delete=True)