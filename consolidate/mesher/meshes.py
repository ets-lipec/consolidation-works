# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 11:20:57 2020

@author: andre
"""

# Adherent 1 = Bottom Adherent


import numpy as np

class MeshTwoPlates():

    def __init__(self, deck, geometry):
        self.deck = deck
        self.n = int(self.deck.doc["Problem Type"]["Number of Domains"])
        self.geometry = geometry
        self.set_Keys()
        self.set_mesh_grid()
        self.set_element_size()
        


    def set_Keys(self):
        self.Keys = []
        for i in range(self.n):
            self.Keys.append("Domain " + str(i + 1))
            
    def set_mesh_grid(self):
        self.nx = {key: None for key in self.Keys}
        self.ny = {key: None for key in self.Keys}
        for i in range(self.n):
            nx = (int(self.deck.doc["Mesh"]["Number of Elements in X"]["Domain " + str(i+1)]))
            ny = (int(self.deck.doc["Mesh"]["Number of Elements in Y"]["Domain " + str(i+1)]))
            self.nx[self.Keys[i]] = nx
            self.ny[self.Keys[i]] = ny



    def set_element_size(self):
        self.element = {key: [None,None] for key in self.Keys}
        for i in range(self.n):
            dx = self.geometry.Lx.get("Domain " + str(i+1))/self.nx.get("Domain " + str(i+1))  
            dy = self.geometry.Ly.get("Domain " + str(i+1))/self.ny.get("Domain " + str(i+1))  
            self.element[self.Keys[i]] = [dx,dy]




            