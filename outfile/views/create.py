import time
from django.http import HttpResponse
from django.utils.timezone import now
import shutil
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
from outfile.forms import InputOutputFormSet, ProblemForm, InputOutputForm
import subprocess
import os
from django.shortcuts import get_object_or_404
from outfile.models import Problem, InputOutput
from .get_zerojudge import sample_secret_file
from .PathManager import PathManager

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

FILE_NAME = ["title", "statement", "input_format", "output_format", "hint"]


def output_file(path, name, string):
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{name}", "w", encoding="UTF-8") as f:
        f.write(string)

def output_file_tex(path, name, string):
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{name}", "w", encoding="UTF-8") as f:
        string = string.replace("\r\n", "\\\\\n")
        f.write(string)


def process_formset_data(form_data, problem_data):
    # 将 QueryDict 转换为字典
    process_data = get_form_sample_secret_data(form_data)
    # delete old data
    InputOutput.objects.filter(problem=problem_data).delete()
    for input_data, output_data in process_data["sample"]:
        is_sample = True
        InputOutput.objects.create(
            problem=problem_data,
            input=input_data,
            output=output_data,
            is_sample=is_sample,
        )

    for input_data, output_data in process_data["secret"]:
        is_sample = False
        InputOutput.objects.create(
            problem=problem_data,
            input=input_data,
            output=output_data,
            is_sample=is_sample,
        )

#把form表單資料轉成dict,並分成sample和secret
def get_form_sample_secret_data(form_data):
    sample = []
    secret = []

    for i in range(int(form_data["inputoutput_set-TOTAL_FORMS"][0])):
        is_sample_data = form_data.get(f"inputoutput_set-{i}-is_sample", None)
        input_data = form_data.get(f"inputoutput_set-{i}-input", None)
        output_data = form_data.get(f"inputoutput_set-{i}-output", None)

        print("嗨",input_data, output_data, is_sample_data)
        if is_sample_data:
            sample.append((input_data, output_data))
        else:
            secret.append((input_data, output_data))

    data_list = {"sample": sample, "secret": secret}
    return data_list

def create_tex(form_data, problem_data):
    # 取得表單資料
    process_data = get_form_sample_secret_data(form_data)
    path_manager = PathManager(problem_data.id)
    # 產生 PDF

    # 定義路徑和產生資料夾
    os.makedirs(path_manager.SAMPLE, exist_ok=True)
    os.makedirs(path_manager.SECRET, exist_ok=True)

    # 寫入檔案 stament,input_format,output_format,hint
    for name in FILE_NAME:
        output_file_tex(path_manager.DOM, f"{name}.tex", getattr(problem_data, name))
    output_file_tex(
        path_manager.DOM,
        "problem.tex",
        "\problem{./}{" + problem_data.title + "}{1}{100}",
    )
    output_file_tex(path_manager.DOM, "problem.yaml", f"name: {problem_data.title}")
    output_file_tex(
        path_manager.DOM,
        "domjudge-problem.ini",
        f"timelimit='{problem_data.timelimit}'",
    )

    # 流水號
    file_num = 1

    # 寫入input,output
    # clear old sample
    save_path = {"sample":path_manager.SAMPLE,"secret":path_manager.SECRET}
    for save_type , path in save_path.items():
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path, exist_ok=True)

        for input_data, output_data in process_data[save_type]:
            sample_secret_file(path, f"{file_num}.in", input_data)
            sample_secret_file(path, f"{file_num}.ans", output_data)
            file_num += 1
        
    




def create(request, cid):
    html_show_filed = ["輸出", "輸入"]
    problem = Problem.objects.get(id=cid)
    path_manager = PathManager(cid)
    show_pdf = path_manager.exist_problem_pdf()
    create_pdf = True
    timestamp = int(time.time())
    # 取得現有的 Problem 對象
    problem_data = get_object_or_404(Problem, id=cid)
    if request.method == "POST":
        print(request.POST)
        form_data = request.POST
        save_value = request.POST.get("saveValue", None)
        # 定義資料驗證
        problem_form = ProblemForm(form_data, instance=problem_data)
        io_form = InputOutputFormSet(form_data, instance=problem_data)
        print(problem_form.is_valid(), io_form.is_valid())

        if problem_form.is_valid() and io_form.is_valid():
            create_tex(form_data, problem_data)

            # 複製模板 main.tex 到指定的path
            for file in path_manager.INIT_FILE:
                if not os.path.exists(os.path.join(path_manager.DOM, os.path.basename(file))):
                    shutil.copy(file, path_manager.DOM)

            # 產生PDF
            if create_pdf:
                subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "main.tex"],
                    cwd=path_manager.DOM,
                )

            # if pdf產生ok
            main_pdf_path = os.path.join(path_manager.DOM, "main.pdf")
            if os.path.isfile(main_pdf_path):
                dom_problem = os.path.join(path_manager.DOM, "problem.pdf")
                dom_main_pdf = os.path.join(path_manager.DOM, "main.pdf")
                print("pdf產生ok")
                # delete old pdf
                if os.path.isfile(f"{path_manager.DOM}problem.pdf"):
                    os.remove(dom_problem)
                os.rename(dom_main_pdf, dom_problem)
                
            if save_value == "1":
                # 如果要存檔，就執行 save() 方法
                process_formset_data(
                    request.POST, problem_data
                )  # 資料庫create new data
                problem_form.save()
                output_file(path_manager.DOM, "ans.py", problem_data.ans_program)
                # 生成ans.py
                

            return render(
                request, "create_form_PDF.html", {"cid": cid, "show_pdf": show_pdf}
            )
        else:
            print("ERROR!", problem_form.errors, io_form.errors)

    # 如果是 GET 請求，填充表單數據
    problem_form = ProblemForm(instance=problem)
    io_form = InputOutputFormSet(instance=problem)
    if io_form.initial_form_count() == 0:
        io_form.extra = 1

    # if input_output_form.is_valid():
    #     input_output_form.save()
    content = {
        "cid": cid,
        "problem_form": problem_form,
        "formset": io_form,
        "show_pdf": show_pdf,
        "html_show_filed": html_show_filed,
        'timestamp': timestamp,
    }

    return render(request, "create.html", content)


def download_zip(request, cid):
    path_manager = PathManager(cid)
    source_folder = path_manager.DOM

    # 打包
    shutil.make_archive(source_folder, "zip", source_folder)

    archive_name = f"{source_folder}.zip"

    # 打开打包后的文件
    with open(archive_name, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/zip")

        # 设置头信息，防止缓存
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Expires"] = now().strftime("%a, %d %b %Y %H:%M:%S GMT")

    # 不再手动删除原始的 .zip 文件，因为 make_archive 已经完成了这个操作

    return response
