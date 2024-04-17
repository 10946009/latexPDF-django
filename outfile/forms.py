from django import forms
from django.forms import ModelForm, inlineformset_factory
from outfile.models import Problem, InputOutput
from django.forms import formset_factory


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = "__all__"
        labels = {
            "title": "題目名稱",
            "timelimit": "時間限制",
            "statement": "題目敘述",
            "input_format": "範例輸入",
            "output_format": "範例輸出",
            "hint": "hint",
            "ans_program": "答案程式碼",
            'problem_tag': '標籤(未完成)',
            'problem_hard': '難度(未完成)',

        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "timelimit": forms.NumberInput(attrs={"class": "form-control"}),
            "statement": forms.Textarea(attrs={"class": "form-control"}),
            "input_format": forms.Textarea(attrs={"class": "form-control"}),
            "output_format": forms.Textarea(attrs={"class": "form-control"}),
            "hint": forms.Textarea(attrs={"class": "form-control"}),
            "ans_program": forms.Textarea(attrs={"class": "form-control",'hidden': 'true'}),
            'problem_tag': forms.SelectMultiple(attrs={"class": "form-control"}),
            'problem_hard': forms.Select(attrs={"class": "form-control"})
        }

class InputOutputForm(ModelForm):

    class Meta:
        model = InputOutput
        fields = ["input", "output" , "is_sample"]
        exclude = ["id"]  # 排除掉 id 字段
        labels = {
            "input": "輸入",
            "output": "輸出",
            "is_sample": "範例測資",
        }
        widgets = {
            "input": forms.Textarea(attrs={"class": "form-control inputoutput-input "}),
            "output": forms.Textarea(attrs={"class": "form-control inputoutput-output"}),
            "is_sample": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


InputOutputFormSet = inlineformset_factory(
    Problem, InputOutput, form=InputOutputForm, extra=0, can_delete=True
)
