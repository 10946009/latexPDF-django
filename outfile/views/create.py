from django.shortcuts import render
from outfile.forms import ProblemForm
import subprocess



def create(request):
    form = ProblemForm()
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()


    subprocess.run(['pdflatex', '-interaction=nonstopmode', 'example.tex'])

    return render(request, 'create.html', {'form': form})