from django.db import models

# Create your models here

class Problem(models.Model):
    title = models.TextField(max_length=255, blank=True, null=False, default='')
    statement = models.TextField(max_length=255, blank=True, null=False, default='')
    sample_input = models.TextField(max_length=255, blank=True, null=False, default='')
    sample_output = models.TextField(max_length=255, blank=True, null=False, default='')
    hint = models.TextField(max_length=255, blank=True, null=False, default='')

    def __str__(self):
        return self.title

class InputOutput(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField(max_length=255, blank=True, null=False, default='')
    output = models.TextField(max_length=255, blank=True, null=False, default='')
