# -*- coding: utf-8 -*-
import yaml, sys
import os.path

class Deck():

    def __init__(self, inputhpath):
        if not os.path.exists(inputhpath):
            print("File " + inputhpath)
            sys.exit(1)
        else:
            with open(inputhpath,'r') as f:
                ## Container of the tags parsed from the yaml file
                self.doc = yaml.load(f, Loader=yaml.BaseLoader)
        self.create_folder_structure()
        self.type=self.doc["Problem Type"]["Type"]
        
        
    def create_folder_structure(self):        
        self.plot_dir = self.doc["Plot"]["folder"]
        check_folder = os.path.isdir(self.plot_dir)
        if not check_folder:
              os.makedirs(self.plot_dir)
