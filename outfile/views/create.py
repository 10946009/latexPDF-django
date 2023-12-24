import shutil
from django.shortcuts import render
from outfile.forms import ProblemForm
import subprocess
import os
from django.shortcuts import get_object_or_404
from outfile.models import Problem

FILE_NAME = ['title','statement','sample_input','sample_output','hint']

def output_file(path,name,string):
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{name}','w',encoding='UTF-8') as f:
        f.write(string)

def create(request,cid):

    # 取得現有的 Problem 對象
    unit = get_object_or_404(Problem, id=cid)
    
    if request.method == 'POST':
        # 如果是 POST 請求，處理表單提交
        form = ProblemForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            # 產生 PDF
            all_file_path = os.path.join("static", "latex", f'{unit.id}')
            dom_path = os.path.join(all_file_path, "dom")
            main_path = os.path.join("static","latex","main.tex")
            if not os.path.exists(all_file_path):
                os.mkdir(os.path.join(all_file_path))
                os.mkdir(os.path.join(all_file_path,"dom"))

            #寫入檔案
            for name in FILE_NAME:
                output_file(all_file_path, f'{name}.tex', getattr(unit, name))
            output_file(all_file_path,'problem.tex','\problem{./}{'+unit.title+'}{1}{100}')
            output_file(dom_path,'problem.yaml',f'name: {unit.title}')
            output_file(dom_path,'domjudge-problem.ini',f"timelimit='{unit.timelimit}'")
            
            
            # copy main.tex to path
            f2 = os.path.join(all_file_path, "main.tex")
            shutil.copyfile(main_path,f2)

            subprocess.run(['pdflatex', '-interaction=nonstopmode', 'main.tex'],cwd=all_file_path)
    else:
        # 如果是 GET 請求，填充表單數據
        form = ProblemForm(instance=unit)

    return render(request, 'create.html', {'form': form,'cid':cid})