#!/usr/bin/python
from django.http import HttpResponse,JsonResponse
import subprocess
import os
import random
import requests
def generate_in_ans_file(input,code):
    p = subprocess.Popen(['python3', '-c', code],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

    output, error = p.communicate(input=input)
    
    if error:
        return error
    # 處理最後多出來的\n
    output = output.rstrip('\n')
    return output

def generator(request):
    if request.method != "POST":
        return HttpResponse("Not allow")
    
    ans = request.POST.get('ans')
    data_list = request.POST.getlist('data[]')
    output_list = []
    for data in data_list:
        print(data)
        output = generate_in_ans_file(data,ans)
        output_list.append(output)
    print(output_list)

    return JsonResponse({"output_list":output_list})