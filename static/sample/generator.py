#!/usr/bin/python
import subprocess
import os
import random
import glob
############################################################################
def generate_random_one(m_min,m_max):
    global inputlist
    r = random.randrange(m_min,m_max+1)
    inputlist.append(f'{r}\n')
    return r

def generate_random_many(many,m_min,m_max,repeat,sort):
    global inputlist
    random_lst = []
    if repeat:
        for i in range(int(many)):
            random_lst.append(random.randrange(m_min,m_max))
    else:
        random_lst=random.sample(range(m_min,m_max),many)
    if sort:
        random_lst.sort()

    inputlist.append(' '.join(list(map(str,random_lst)))+'\n')
    return random_lst

def generate_random_first_many(f_min,f_max,m_min,m_max,repeat,sort):
    global inputlist
    random_lst = []
    r = random.randrange(f_min,f_max)
    if repeat:
        for i in range(int(r)):
            random_lst.append(random.randrange(m_min,m_max))
    else:
        random_lst=random.sample(range(m_min,m_max),r)
    if sort:
        random_lst.sort()

    inputlist.append(f'{r} '+' '.join(list(map(str,random_lst)))+'\n')
    return random_lst
#############################################################################

# 1. 請先把解答程式放在ans.py
# 2. 確定terminal開在generator.py同一層的資料夾 ex: C:/xxx/xxx/a001
# 3. 設定測資範本
    
###############################################################################


# 在這邊定義secret測資數量!!!
secret_count = 5

secret = []
for i in range(secret_count):
    sample_input = ''
    inputlist = []

    # 在這裡定義隱藏測資邏輯!!!!!!!!!!!!
    # sample_input = 一行文字
    # inputlist.append(sample_input+"\n") 用來存入每一行的測資，結尾\n用來換行

    # 此為zj-a001的範例，直接定義secret即可
    # secret=['python','c++','hello','a123','abcdefg']

    # 此為zj-a002的範例，自定義兩個數的亂數
    # a = random.randrange(0,10000)
    # b = random.randrange(0,10000)
    # inputlist.append(f'{a} {b}\n')
    
    # 此為zj-d074的範例，自定義亂數
    # M = random.randrange(1, 10)
    # sample_input = f"{M}"
    # inputlist.append(sample_input+"\n")
    # mlst=[]
    # for r in range(0,M):
    #     m =random.randrange(10,100)
    #     mlst.append(str(m))

    # inputlist.append(' '.join(mlst))
    

    #此為zj-d074的呼叫方法範例
    # generate_random_one(最小值,最大值)，會回傳一個亂數且自動塞入inputlist
    # generate_random_many(亂數數量,最小值,最大值,是否可重複,是否排序)，會回傳一個亂數list且自動塞入inputlist
    # generate_random_first_many(第一個數字最小值,第一個數字最大值,亂數list的最小值,亂數list的最大值,是否可重複,是否排序)
    # 根據第一個的數字決定後面要產多少數字，會回傳一個亂數list且自動塞入inputlist
    for j in range(5,10):
        generate_random_one(2,1000000) # 1~10的亂數
    inputlist.append('0\n')
    print(inputlist)
    
    
    #測資邏輯結束
    #輸出secret
    if len(secret) == secret_count:
        break 
    secret.append(''.join(inputlist))


#----------------------------------------------------
# 把測資跟secret放進ans.py並取出output
def generate_in_ans_file(input, path, number):
    p = subprocess.Popen(os.getcwd() + "/ans.py",
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8', shell=True)

    output, error = p.communicate(input=input)
    print(input, output, path, number)
    with open(f"{path}/{number}.in",'w', encoding = 'utf-8') as f:
        f.write(input)
    with open(f"{path}/{number}.ans",'w', encoding = 'utf-8') as f:
        f.write(output)

# 定義路徑
secret_path = os.getcwd() + "/data/secret"
path = [
    os.getcwd() + "/data",
    secret_path
]

# 建立secret資料夾
for p in path:
    if not os.path.isdir(p):
        os.mkdir(p)

# 產生input跟ans
# 判斷sample中有幾筆測資
number = len(os.listdir(os.getcwd()+'/data/sample'))//2 
for i, d in enumerate(secret):
    number += 1
    generate_in_ans_file(d, secret_path, number)


# main.pdf更名為problem.pdf
if 'main.pdf' in os.listdir(os.getcwd()):
    os.rename('main.pdf','problem.pdf')