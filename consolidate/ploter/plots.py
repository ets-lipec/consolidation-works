# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:00:34 2020

@author: andre
"""

import matplotlib.pyplot as plt
from PIL import Image
import glob
import numpy as np


class PlotsTwoPlates():
    
    def __init__(self, deck,meshes, assembles, BC):
        self.deck = deck
        self.assembles=assembles
        self.nsteps =  int(self.deck.doc["Simulation"]["Number Time Steps"])
        self.nsetepinterval =int(self.deck.doc["Plot"]["plot interval"])
        self.meshes=meshes
        self.T = BC.T
        self.Dic=BC.Dic
        self.Dic0=BC.Dic0
        self.Keys=meshes.Keys
        self.n = meshes.n
        self.set_plot_limites()
        self.set_plots()
        
        
        
    def set_plot_limites(self):
        self.T = {key: [None, None] for key in self.Keys}
        for i in range(self.n):
            T = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            T = float(self.deck.doc["Boundary Condition"]["Initial Temperature Domain " + str(i+1)])
            self.T[self.Keys[i]] = T
        
        tmin=self.T["Domain 1"]
        for i in range(1,self.n):
            self.tmin=min(tmin, self.T["Domain " + str(i+1)])
            
            
    def set_plots(self):
        self.mfig=[]
        for i in range (0,self.nsteps,self.nsetepinterval):
            self.mfig.append(i)
        self.fignum = 0
        self.fig = plt.figure()
        
    def update_T(self,T):
        self.T = T
        
    def update_Dic(self,Dic):
        self.Dic = Dic
        
        
    def do_plots(self,m):
        plt.clf()
        self.fignum += 1
        print(m, self.fignum)
        # plt.figure( figsize=(8, 6), dpi=280)
        plt.gcf().set_size_inches(16, 8)
        plt.gcf().set_dpi(80)
        plt.pcolormesh(self.assembles.Xposition, self.assembles.Yposition, self.T, vmin=self.tmin, vmax=float(self.deck.doc["Boundary Condition"]["Ideal Temperature"]),cmap=self.deck.doc["Plot"]["Color Map"])
        plt.colorbar()
        self.fig.suptitle('time: {:.2f}'.format( m*float(self.deck.doc["Simulation"]["Time Step"])), fontsize=16)
        plt.savefig(self.deck.plot_dirTemp+self.deck.doc["Plot"]["figure temperature name"]+ str("%03d" %self.fignum) + '.jpg')
        
        plt.clf()
        print(m, self.fignum)
        # plt.figure( figsize=(8, 6), dpi=280)
        plt.gcf().set_size_inches(16, 8)
        plt.gcf().set_dpi(80)
        plt.pcolormesh(self.assembles.Xposition, self.assembles.Yposition, self.Dic, vmin=self.Dic0, vmax=1,cmap=self.deck.doc["Plot"]["Color Map"])
        plt.colorbar()
        self.fig.suptitle('time: {:.2f}'.format( m*float(self.deck.doc["Simulation"]["Time Step"])), fontsize=16)
        plt.savefig(self.deck.plot_dirDic+self.deck.doc["Plot"]["figure dic name"]+ str("%03d" %self.fignum) + '.jpg')


    def do_animation(self):   
        frames = []
        # imgs = glob.glob("./output/*.jpg")
        imgs = glob.glob(self.deck.plot_dirTemp + '*.jpg')
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)
            print(i)
    
        direction=(self.deck.plot_dirTemp+self.deck.doc["Animation"]["Temperature name"]+'.gif')
        frames[0].save(direction, format='GIF', append_images=frames[1:], save_all=True, duration=400, loop=0)
        
        frames = []
        # imgs = glob.glob("./output/*.jpg")
        imgs = glob.glob(self.deck.plot_dirDic + '*.jpg')
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)
            print(i)
            
        direction=(self.deck.plot_dirDic+self.deck.doc["Animation"]["Dic name"]+'.gif')
        frames[0].save(direction, format='GIF', append_images=frames[1:], save_all=True, duration=400, loop=0)  
        
        