# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:38:36 2020

@author: andre
"""

import numpy as np


class BoundaryCondition():
    
    
    def __init__(self, deck,geometry,meshes):
        self.deck = deck
        self.Troom = self.deck.doc["Boundary Condition"]["Room Temperature"]
        self.geometry = geometry
        self.meshes = meshes
        self.n = meshes.n
        self.Keys = meshes.Keys
        self.set_temperatures()
        self.set_conductivity()
        self.set_density()
        self.set_specific_heat()
        self.set_diffusivity()
        self.set_dic()
        self.set_heat_input_density()
        self.set_master_properties()
        self.set_viscosity()
        
        
    def set_temperatures(self):    

        self.T_individual = {key: [None, None] for key in self.Keys}
        for i in range(self.n):
            T = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            T[:] = float(self.deck.doc["Boundary Condition"]["Initial Temperature Domain " + str(i+1)])
            self.T_individual[self.Keys[i]] = T
            
    def set_conductivity(self):
        self.Kx_individual = {key: [None, None] for key in self.Keys}
        self.Ky_individual = {key: [None, None] for key in self.Keys}
        for i in range(self.n):
            Kx = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            Ky = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            Kx[:] = float(self.deck.doc["Materials"]["Domain " + str(i+1)]["Thermal Conductivity X"])
            Ky[:] = float(self.deck.doc["Materials"]["Domain " + str(i+1)]["Thermal Conductivity Y"])

            self.Kx_individual[self.Keys[i]] = Kx
            self.Ky_individual[self.Keys[i]] = Ky
            
    def set_density(self):
        self.Rho_individual = {key: [None, None] for key in self.Keys}
        for i in range(self.n):
            Rho = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            Rho[:] = float(self.deck.doc["Materials"]["Domain " + str(i+1)]["Density"])
            self.Rho_individual[self.Keys[i]] = Rho
            
            
    def set_specific_heat(self):
        self.Cp_individual = {key: [None, None] for key in self.Keys}
        for i in range(self.n):
            Cp = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            Cp[:] = float(self.deck.doc["Materials"]["Domain " + str(i+1)]["Specific Heat Capacity"])
            self.Cp_individual[self.Keys[i]] = Cp
            
    def set_diffusivity(self):
        self.DiffX_individual = {key: [None, None] for key in self.Keys}
        self.DiffY_individual = {key: [None, None] for key in self.Keys}
        for i in range(self.n):
            DiffX = self.Kx_individual["Domain " + str(i+1)] / (self.Cp_individual["Domain " + str(i+1)] * self.Rho_individual["Domain " + str(i+1)])
            DiffY = self.Ky_individual["Domain " + str(i+1)] / (self.Cp_individual["Domain " + str(i+1)] * self.Rho_individual["Domain " + str(i+1)])
            self.DiffX_individual[self.Keys[i]] = DiffX
            self.DiffY_individual[self.Keys[i]] = DiffY
            
    def set_viscosity(self):
        Visc = np.zeros((np.shape(self.T)))
        Visc[0:, 0:] = 1.14*10**(-12)*np.exp(26300/self.T[0:, 0:])
        self.Visc=Visc.copy()

    def set_dic(self):
        self.Dic0=1./(1.+0.45)        
        self.Dic_individual = {key: [None, None] for key in self.Keys}
        
        Dic = {
            "Domain 1":np.ones((self.meshes.ny["Domain 1"], self.meshes.nx["Domain 1"])) ,
            "Domain 2":np.ones((self.meshes.ny["Domain 2"], self.meshes.nx["Domain 2"])) ,
            "Domain 3":np.ones((self.meshes.ny["Domain 3"], self.meshes.nx["Domain 3"])) 
                  }
        self.Dic_individual=Dic
        self.Dic_individual["Domain 1"][-1,:] = self.Dic0
        self.Dic_individual["Domain 2"][0:self.meshes.ny["Domain 2"],0:self.meshes.nx["Domain 2"]] = self.Dic0
        self.Dic_individual["Domain 3"][0,:] = self.Dic0
        
        
    def set_heat_input_density(self):
        self.q=float(self.deck.doc["Boundary Condition"]["Input Power Density"])
        Q =    {
        "Domain 1":np.zeros((self.meshes.ny["Domain 1"], self.meshes.nx["Domain 1"])),
        "Domain 2":np.zeros((self.meshes.ny["Domain 2"], self.meshes.nx["Domain 2"])),
        "Domain 3":np.zeros((self.meshes.ny["Domain 3"], self.meshes.nx["Domain 3"])) 
                  }
        Q["Domain 2"][0:self.meshes.ny["Domain 2"],0:self.meshes.nx["Domain 2"]] = self.q
        
        Q=np.concatenate((Q["Domain 1"], Q["Domain 2"], Q["Domain 3"]), axis=0)
        self.Q=Q.copy()
        
        
    def set_master_properties(self):
        # self.T = []
        # self.Kx = []
        # self.Ky = []
        # self.Rho = []
        # self.Cp = []
        # self.Dx = []
        # self.Dy = []
        # self.Dic = []
        auxT = self.T_individual["Domain 1"]
        auxKx = self.Kx_individual["Domain 1"]
        auxKy = self.Ky_individual["Domain 1"]
        auxRho = self.Rho_individual["Domain 1"]
        auxCp = self.Cp_individual["Domain 1"]
        auxDiffX = self.DiffX_individual["Domain 1"]
        auxDiffY = self.DiffY_individual["Domain 1"]
        auxDic = self.Dic_individual["Domain 1"]
        
        for i in range(1,self.n):
            auxT = np.concatenate((auxT,self.T_individual["Domain " + str(i+1)]))
            auxKx = np.concatenate((auxKx,self.Kx_individual["Domain " + str(i+1)]))
            auxKy = np.concatenate((auxKy,self.Ky_individual["Domain " + str(i+1)]))
            auxRho = np.concatenate((auxRho,self.Rho_individual["Domain " + str(i+1)]))
            auxCp = np.concatenate((auxCp,self.Cp_individual["Domain " + str(i+1)]))
            auxDiffX = np.concatenate((auxDiffX,self.DiffX_individual["Domain " + str(i+1)]))
            auxDiffY = np.concatenate((auxDiffY,self.DiffY_individual["Domain " + str(i+1)]))
            auxDic = np.concatenate((auxDic,self.Dic_individual["Domain " + str(i+1)]))
        self.T = auxT
        self.Kx = auxKx
        self.Ky = auxKy
        self.Rho = auxRho
        self.Cp = auxCp
        self.DiffX = auxDiffX
        self.DiffY = auxDiffY
        self.Dic = auxDic
        self.T0 = self.T.copy()        