from django.db import models

# Create your models here

class Problem(models.Model):
    # main_tex = models.ForeignKey('MainTex', on_delete=models.SET_DEFAULT)
    title = models.TextField(blank=True, null=False, default='')
    problem_number = models.TextField(blank=True, null=False, default='')
    timelimit = models.IntegerField(blank=False, null=False, default=1)
    statement = models.TextField(blank=True, null=False, default='')
    input_format = models.TextField(blank=True, null=False, default='')
    output_format = models.TextField(blank=True, null=False, default='')
    hint = models.TextField(blank=True, null=False, default='')
    created_time = models.DateTimeField(auto_now_add=True ,blank=True, null=True)
    edited_time = models.DateTimeField(auto_now=True ,blank=True, null=True)
    ans_program = models.TextField(blank=True, null=False, default='')

    problem_tag = models.ManyToManyField('Tag', blank=True)
    problem_hard = models.ManyToManyField('Hard', blank=True)
    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.TextField(blank=True, null=False, default='')
    def __str__(self):
        return self.name

class Hard(models.Model):
    name = models.TextField(blank=True, null=False, default='')
    def __str__(self):
        return self.name
class InputOutput(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_sample = models.BooleanField(default=False)
    input = models.TextField(blank=True, null=False, default='')
    output = models.TextField(blank=True, null=False, default='')

    def __str__(self):
        return self.problem
# class MainTex(models.Model):
#     name = models.TextField(blank=True, null=False, default='')
#     content = models.TextField(blank=True, null=False, default='')
