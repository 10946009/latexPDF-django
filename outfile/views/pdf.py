from django.shortcuts import render
from outfile.models import Problem
from .PathManager import PathManager

def get(request,cid):
    path_manager = PathManager(cid)
    show_pdf = path_manager.exist_problem_pdf()
    return render(request, 'create_form_PDF.html',{'cid':cid,'show_pdf':show_pdf})