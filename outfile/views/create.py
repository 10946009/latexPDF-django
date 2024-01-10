import shutil
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
from outfile.forms import InputOutputFormSet, ProblemForm,InputOutputForm
import subprocess
import os
from django.shortcuts import get_object_or_404
from outfile.models import Problem,InputOutput
from .get_zerojudge import sample_file

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

FILE_NAME = ['title','statement','input_format','output_format','spec','hint']

def output_file(path,name,string):
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{name}','w',encoding='UTF-8') as f:
        string = string.replace('\r\n', '\\\\\n')
        f.write(string)

def process_formset_data(request_data,problem_data):
    # 将 QueryDict 转换为字典
    form_data = dict(request_data)
    # 获取表单集中的 DELETE 字段
    # delete old data
    for i in range(int(form_data['inputoutput_set-INITIAL_FORMS'][0])):
        delete_data = form_data.get(f'inputoutput_set-{i}-DELETE', None)
        if delete_data != ['on']:
            #create new data
            input_data = form_data.get(f'inputoutput_set-{i}-input', None)
            output_data = form_data.get(f'inputoutput_set-{i}-output', None)
            InputOutput.objects.create(problem=problem_data,input=input_data[0],output=output_data[0])
            print("add",i,input_data,output_data)
            


def create(request,cid):
    problem = Problem.objects.get(id=cid)
    # 取得現有的 Problem 對象
    problem_data = get_object_or_404(Problem, id=cid)
    if request.method == 'POST':
        form_data = dict(request.POST)
        #定義資料驗證
        problem_form = ProblemForm(form_data, instance=problem_data)
        io_form = InputOutputFormSet(form_data, instance=problem_data)
        print(problem_form.is_valid(),io_form.is_valid())

        if problem_form.is_valid() and io_form.is_valid():
            #delete old data
            InputOutput.objects.filter(problem=problem_data).delete()

            # 產生 PDF
            # 定義路徑和產生資料夾
            all_file_path = os.path.join("static", "latex", f'{problem_data.id}')
            path_dom = os.path.join(all_file_path, "dom")
            main_path = os.path.join("static","latex","main.tex")
            if not os.path.exists(all_file_path):
                os.mkdir(os.path.join(all_file_path))
                os.mkdir(os.path.join(all_file_path,"dom"))

            #寫入檔案 stament,input_format,output_format,spec,hint
            for name in FILE_NAME:
                output_file(path_dom, f'{name}.tex', getattr(problem_data, name))
            output_file(path_dom,'problem.tex','\problem{./}{'+problem_data.title+'}{1}{100}')
            output_file(path_dom,'problem.yaml',f'name: {problem_data.title}')
            output_file(path_dom,'domjudge-problem.ini',f"timelimit='{problem_data.timelimit}'")
            
            #寫入input,output
            path_dom_sample = os.path.join(path_dom,"data","sample")
            for i in range(int(form_data['inputoutput_set-INITIAL_FORMS'][0])):
                delete_data = form_data.get(f'inputoutput_set-{i}-DELETE', None)
                if delete_data != ['on']:
                    #create new data
                    input_data = form_data.get(f'inputoutput_set-{i}-input', None)
                    output_data = form_data.get(f'inputoutput_set-{i}-output', None)
                    sample_file(path_dom_sample,f'{i+1}.in',input_data)
                    sample_file(path_dom_sample,f'{i+1}.ans',output_data)
            
            # copy main.tex to path
            new_main_path = os.path.join(path_dom, "main.tex")
            shutil.copyfile(main_path,new_main_path)
            subprocess.run(['pdflatex', '-interaction=nonstopmode', 'main.tex'],cwd=path_dom)

            # if pdf產生ok
            main_pdf_path = os.path.join(path_dom, "main.pdf")
            if os.path.isfile(main_pdf_path):
                    dom_problem = os.path.join(path_dom,"problem.pdf")
                    dom_main_pdf = os.path.join(path_dom,"main.pdf")
                    print('pdf產生ok')
                    # delete old pdf
                    if os.path.isfile(f'{path_dom}problem.pdf'):
                        os.remove(dom_problem)
                    os.rename(dom_main_pdf,dom_problem)

            # # 如果要存檔，就執行 save() 方法
            # process_formset_data(request.POST,problem_data) # 資料庫create new data
            # problem_form.save()
            # io_form.save()
        
        else:
            print("ERROR!",problem_form.errors,io_form.errors)

    # 如果是 GET 請求，填充表單數據
    problem_form = ProblemForm(instance=problem)
    io_form = InputOutputFormSet(instance=problem)
    if io_form.initial_form_count() == 0:
        io_form.extra = 1

    # if input_output_form.is_valid():
    #     input_output_form.save()
    
    return render(request, 'create.html', {'cid':cid,'problem_form': problem_form, 'formset': io_form })


def your_view(request, problem_id):
    problem = Problem.objects.get(id=problem_id)

    if request.method == 'POST':
        problem_form = ProblemForm(request.POST, instance=problem)
        formset = InputOutputFormSet(request.POST, instance=problem)
        if problem_form.is_valid() and formset.is_valid():
            problem_form.save()
            formset.save()
    else:
        problem_form = ProblemForm(instance=problem)
        formset = InputOutputFormSet(instance=problem)

    return render(request, 'your_template.html', {'problem_form': problem_form, 'formset': formset})