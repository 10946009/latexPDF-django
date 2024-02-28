import shutil
import time
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
from outfile.forms import ProblemForm, InputOutputFormSet
import subprocess
import os
from outfile.models import InputOutput, Problem
from .PathManager import PathManager
from django.http import HttpResponse
from requests.exceptions import RequestException

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

FILE_NAME = ["title", "statement", "input_format", "output_format", "hint"]


def output_file(path, name, string):
    os.makedirs(path, exist_ok=True)
    print([string])
    with open(f"{path}/{name}", "w", encoding="UTF-8") as f:
        string = string.replace("\r\n", "\\\\")
        f.write(string)


# 取代常用的特殊字元轉為latex格式
def replace_special_characters(st):
    latex_n = "\\\\"
    st = st.replace("\xa0", latex_n)
    st = st.replace("\n", latex_n)
    while 1:
        if "\\\\\\\\" in st:
            st = st.replace("\\\\\\\\", latex_n)
        else:
            break
    st = st.replace(latex_n, "\n")
    st = st.replace("\t", "")

    # 特殊符號
    st = st.replace("≤", "$\leq$")
    st = st.replace("<=", "$\leq$")
    st = st.replace("≥", "$\geq$")
    st = st.replace(">=", "$\geq$")
    st = st.replace("!=", "$\neq$")
    st = st.replace("<", "$<$")
    st = st.replace(">", "$>$")
    st = st.replace("%", "\%")
    return st


def get_crowd(url):
    html = requests.get(url, headers=headers)
    html.encoding = "UTF-8"
    htmltext = BeautifulSoup(html.text, "html.parser")
    return htmltext


# 針對sample的in,ans檔轉LF
def sample_secret_file(path, name, lststring):
    print(lststring)
    lststring = lststring.replace("\r\n", "\n")
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{name}", "wb") as f:
        f.write((str(lststring) + "\n").encode())

def get_zerojudge_problem(number):
    problem_from = (f"% 題目來源:https://zerojudge.tw/ShowProblem?problemid={number} \n")
    try:
        htmltext = get_crowd("https://zerojudge.tw/ShowProblem?problemid=" + number)
    except RequestException as err:
        print(err)
        print("網路連接失敗")
        return {"error": "網路連接失敗", "status": 503}  # 503 Service Unavailable
    except Exception as err:
        print(err)
        print(number, "無此題目")
        return {"error": "無此題目", "status": 404}

    title = htmltext.find("span", id="problem_title").text
    problem = htmltext.find_all("div", class_="panel-body")
    lst = []
    for i in problem:
        if "記憶體限制" in i.text:
            break
        st = i.text.strip()
        # 取代常用特殊字元
        # st = HanziConv.toTraditional(replace_special_characters(st))
        st = replace_special_characters(st)
        lst.append(st)
    input_output = lst[3:]
    #處理input output
    all_io = list()
    io_dict = {"input": "", "output": "", "is_sample": True}
    for index, io in enumerate(input_output):
        print("io", [io])
        io = io.replace("\r\n", "\n")
        if index % 2 == 0:
            io_dict["input"] = io
        else:
            io_dict["output"] = io
            all_io.append(io_dict)
            io_dict = {"input": "", "output": "", "is_sample": True}

    return {
        "title": title,
        "statement": problem_from + lst[0],
        "input_format": lst[1],
        "output_format": lst[2],
        "hint": "",
        "input_output": all_io,
    }


def get_zerojudge(request, cid):
    timelimit = 1
    all_file_path = os.path.join("static", "latex", f"{cid}")
    path_dom = os.path.join(all_file_path, "dom")
    main_path = os.path.join("static", "latex", "main.tex")
    show_pdf = PathManager(cid).exist_problem_pdf()
    number = request.POST["ZeroJudgeNumber"]
    timestamp = int(time.time())

    # 爬取題目
    zerojudge_data = get_zerojudge_problem(number)
    
    # 題目來源變數



    problem_dict = {
        "title": zerojudge_data['title'],
        "timelimit": timelimit,
        "statement": zerojudge_data['statement'],
        "input_format": zerojudge_data['input_format'],
        "output_format": zerojudge_data['output_format'],
        "hint": '',
    }
    
    problem_form = ProblemForm(initial=problem_dict)
    io_form = InputOutputFormSet(initial=zerojudge_data['input_output'])
    io_form.extra = len(zerojudge_data['input_output'])
    print(zerojudge_data['input_output'])

    content = {
        "cid": cid,
        "problem_form": problem_form,
        "formset": io_form,
        "number": number,
        "show_pdf": show_pdf,
    }
    return render(request, "create_form_form.html", content)
