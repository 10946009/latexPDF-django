from django.db import models

# Create your models here

class Problem(models.Model):
    # main_tex = models.ForeignKey('MainTex', on_delete=models.SET_DEFAULT)
    title = models.TextField(max_length=255, blank=True, null=False, default='')
    timelimit = models.IntegerField(blank=False, null=False, default=1)
    statement = models.TextField(max_length=255, blank=True, null=False, default='')
    hint = models.TextField(max_length=255, blank=True, null=False, default='')
    spec = models.TextField(max_length=255, blank=True, null=False, default='')

    def __str__(self):
        return self.title

class InputOutput(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_sample = models.BooleanField(default=False)
    input = models.TextField(max_length=255, blank=True, null=False, default='')
    output = models.TextField(max_length=255, blank=True, null=False, default='')

# class MainTex(models.Model):
#     name = models.TextField(max_length=255, blank=True, null=False, default='')
#     content = models.TextField(max_length=255, blank=True, null=False, default='')
