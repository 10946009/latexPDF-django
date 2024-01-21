from django.shortcuts import render
from outfile.models import Problem
def index(request):
    problem_list = Problem.objects.all()
    return render(request, 'index.html', {'problem_list': problem_list})