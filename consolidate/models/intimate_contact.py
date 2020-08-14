# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:07:28 2020

@author: andre
"""

import numpy as np

class IntimateContact():
    
    def __init__(self, meshes, deck):
        self.meshes = meshes
        self.deck = deck
        self.P = (float(self.deck.doc["Boundary Condition"]["Consolidation Pressure"]))
        self.init_parameter()
        # self.calculate_average_dic()
        
        
    def viscosity_timestep(self,v,u):
        v[0:, 0:]=1.14*10**(-12)*np.exp(26300/u[0:,0:])
        return v
    
    
    def init_parameter(self):
        self.aux1 = 0
        self.aux2 = 0
        self.aux3 = 0
        
        
    def dic_timestep(self, dic, dic0, v, t):
        
        C1=5*(1+0.45)*(0.85)**2
        
        dic[self.meshes.ny["Domain 1"]-1, 0:] = dic[self.meshes.ny["Domain 1"]-1, 0:] * (1 + C1 * (self.aux1 + self.P*10**6/v[(self.meshes.ny["Domain 1"]-1), 0:]*t))**(1/5)
        dic[self.meshes.ny["Domain 1"], 0:] = dic[self.meshes.ny["Domain 1"], 0:] * (1 + C1*(self.aux2 + self.P*10**6/v[(self.meshes.ny["Domain 1"]), 0:]*t))**(1/5)
        dic[self.meshes.ny["Domain 1"] + self.meshes.ny["Domain 2"], 0:]=dic[self.meshes.ny["Domain 1"] + self.meshes.ny["Domain 2"], 0:]*(1+C1*(self.aux3 + self.P*10**6/v[(self.meshes.ny["Domain 1"] + self.meshes.ny["Domain 2"]), 0:]*t))**(1/5)
        np.clip(dic, 0, 1)
        
        self.aux1=self.aux1+self.P*10**6/v[(self.meshes.ny["Domain 1"]-1), 0:]*t
        self.aux2=self.aux2+self.P*10**6/v[(self.meshes.ny["Domain 1"]), 0:]*t
        self.aux3=self.aux3+self.P*10**6/v[(self.meshes.ny["Domain 1"] + self.meshes.ny["Domain 2"]), 0:]*t
        return dic



    # def calculate_average_dic(self):
    #     self.DicAverage=np.sum(self.meshes.Dic[int(self.meshes.ny/2-1):int(self.meshes.ny/2+1),1:-1])/((self.meshes.nx-2)*2)
    #     return self.DicAverage