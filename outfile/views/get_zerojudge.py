import shutil
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
from outfile.forms import ProblemForm
import subprocess
import os
from django.shortcuts import get_object_or_404
from outfile.models import Problem

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

FILE_NAME = ['title','statement','sample_input','sample_output','hint']

def output_file(path,name,string):
    os.makedirs(path, exist_ok=True)
    print([string])
    with open(f'{path}/{name}','w',encoding='UTF-8') as f:
        string = string.replace('\r\n', '\\\\')
        f.write(string)

# 取代常用的特殊字元轉為latex格式
def replace_special_characters(st):
    st = st.replace('\xa0', '\\\\')
    st = st.replace('\n', '\\\\')
    st = st.replace('。', '。\\\\')
    while 1:
        if '\\\\\\\\' in st:
            st = st.replace('\\\\\\\\', '\\\\')
        else:
            break
    st = st.replace('\\\\', '\\\\\n')
    st = st.replace('\t', '')

    #特殊符號
    st = st.replace('≤', '$\leq$')
    st = st.replace('<=', '$\leq$')
    st = st.replace('≥', '$\geq$')
    st = st.replace('>=', '$\geq$')
    st = st.replace('!=', '$\neq$')
    st = st.replace('<', '$<$')
    st = st.replace('>', '$>$')
    st = st.replace('%', '\%')
    return st


def get_crowd(url):
    html = requests.get(url,headers=headers)
    html.encoding = 'UTF-8'
    htmltext = BeautifulSoup(html.text, 'html.parser')
    return htmltext

#針對sample的in,ans檔轉LF
def sample_file(path,name,lststring):
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{name}','wb') as f:
        f.write((str(lststring)+'\n').encode())


def get_zerojudge(request,cid):
    timelimit = 1
    all_file_path = os.path.join("static", "latex", f'{cid}')
    path_dom = os.path.join(all_file_path, "dom")
    main_path = os.path.join("static","latex","main.tex")

    number = request.POST['ZeroJudgeNumber']
    print("正在爬取題目",number)
    try:
        htmltext = get_crowd('https://zerojudge.tw/ShowProblem?problemid='+number)
        problem_all_text = []
        title = htmltext.find('span', id='problem_title').text
        problem = htmltext.find_all('div', class_='panel-body')
        lst = []

        for i in problem:
            if "記憶體限制" in i.text:
                break
            st = i.text.strip()
            problem_all_text.append(st)
            # 取代常用特殊字元
            # st = HanziConv.toTraditional(replace_special_characters(st))
            st = replace_special_characters(st)
            lst.append(st)
        input_output = lst[3:]
        
        for index,io in enumerate(input_output):
            io = io.replace('\r', '\n')
            io = io.replace('\\\\\n', '')
            if index % 2 == 0:
                sample_file(f'{all_file_path}/dom/data/sample',f'{(index+2)//2}.in',io)
            else:
                sample_file(f'{all_file_path}/dom/data/sample',f'{(index+2)//2}.ans',io)
        
        #題目來源變數
        problem_from = f'% 題目來源:https://zerojudge.tw/ShowProblem?problemid={number} \n'

        #建立檔案&傳放入的文字
        output_file(all_file_path,'statement.tex',problem_from+lst[0])
        output_file(all_file_path,'sample_input.tex',lst[1])
        output_file(all_file_path,'sample_output.tex',lst[2])
        output_file(all_file_path,'problem.tex','\problem{./}{'+title+'}{1}{100}')
        output_file(all_file_path,'spec.tex','')
        output_file(all_file_path,'hint.tex','')
        output_file(path_dom,'problem.yaml',f'name: {title}')
        output_file(path_dom,'domjudge-problem.ini',f"timelimit='{timelimit}'")
        initial_data = {"statement":lst[0],"input":lst[1],"output":lst[2],"title":title,"timelimit":timelimit}
        form = ProblemForm(initial=initial_data)
        #複製generator.py到資料夾
        # f1 = f'{os.getcwd()}/generator.py'
        # f2 = f'{path}/dom/generator.py'
        # if not os.path.isfile(f'{path}/dom/generator.py'):
        #     shutil.copyfile(f1,f2)
        
        # 執行main.tex
        if os.path.isfile(main_path):
            # with open(main_path, 'r') as f:
            #     with open(os.getcwd()+f'/main_{number}.tex', 'a') as f_temp:
            #         for line in f.readlines():
            #             if 'problem.tex' in line:
            #                 f_temp.write(re.sub('\{.*?\}','{'+f'zj-{number}/problem.tex'+'}',line))
            #                 continue
            #             f_temp.write(line)
            # if run_pdf:
            subprocess.run(['pdflatex', '-interaction=nonstopmode', 'main.tex'],cwd=all_file_path)
            
            #刪除暫存
            remove_tamp=['main.aux','main.log','main.out','main.toc']
            for r in remove_tamp:  
                if os.path.isfile(os.path.join(all_file_path,r)):
                    os.remove(os.path.join(all_file_path,r))
            
            #如果成功產出來了就放進dom並改檔名
            
            new_pdf = os.path.join(all_file_path,'main.pdf')
            path_dom = os.path.join(all_file_path,'dom')
            if os.path.isfile(new_pdf):
                print('pdf產生ok')
                shutil.move(new_pdf,path_dom)
                os.rename(os.path.join(path_dom,'main.pdf'),os.path.join(path_dom,'problem.pdf'))
            
        

        else:
            print('pdf產生失敗')

    except Exception as err:
        print(err)
        print(number,"無此題目")
    
    return render(request, 'create_form.html', {'form': form,'cid':cid})