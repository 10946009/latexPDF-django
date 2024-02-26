from django.shortcuts import render
from outfile.models import Problem
from .PathManager import PathManager
import time

def get(request,cid):
    path_manager = PathManager(cid)
    show_pdf = path_manager.exist_problem_pdf()
    timestamp = int(time.time())
    return render(request, 'create_form_PDF.html', {'cid':cid, 'show_pdf':show_pdf, 'timestamp': timestamp})