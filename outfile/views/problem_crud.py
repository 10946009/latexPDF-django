from django.shortcuts import render, redirect,HttpResponse
from outfile.models import Problem

def delete_problem(request,cid = None):
    if request.method == 'POST':
        print(request.POST)
        cid = request.POST.get('cid', None)
        if cid:
            problem = Problem.objects.get(id=cid)
            problem.delete()
            return HttpResponse('刪除成功')
        else:
            return HttpResponse('刪除失敗')
    return HttpResponse('請求失敗')

def create(request):
    new_problem = Problem.objects.create()
    return redirect(f'/create/{new_problem.id}')
