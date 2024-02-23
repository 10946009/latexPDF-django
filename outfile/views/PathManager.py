import os
from enum import Enum

class PathManager:
    def __init__(self, dir_name):
        self.PATH = os.path.join("static", "latex",str(dir_name))
        self.SAMPLE_DIR = os.path.join("static", "sample")
        self.INIT_FILE = [ os.path.join(self.SAMPLE_DIR, file) for file in os.listdir(self.SAMPLE_DIR)]
        self.DOM = os.path.join(self.PATH, "dom")
        self.DOM_ZIP = os.path.join(self.PATH, "dom.zip")
        self.MAIN_TEX = os.path.join(self.DOM, "main.tex")
        self.MAIN_PDF = os.path.join(self.DOM, "main.pdf")
        self.DATA = os.path.join(self.DOM, "data")
        self.SAMPLE = os.path.join(self.DATA, "sample","")
        self.SECRET = os.path.join(self.DATA, "secret","")

        self.PROBLEM_PDF = os.path.join(self.DOM, "problem.pdf")

    def print_all_path(self):
        return [self.PATH, self.SAMPLE_TEX, self.DOM, self.SAMPLE, self.MAIN_TEX, self.MAIN_PDF, self.PROBLEM_PDF]
    
    def exist_problem_pdf(self):
        return os.path.isfile(self.PROBLEM_PDF)
    # def __init__(self, problem_object):
    #     self.path = os.path.join("static", "latex", f'{problem_object.id}')

    # def get_path(self):
    #     return self.path
    
    # def get_dom_path(self):
    #     return os.path.join(self.path, "dom")
    
    # def get_sample_path(self):
    #     return os.path.join(self.get_dom_path(),"data","sample")