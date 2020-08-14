# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:38:36 2020

@author: andre
"""


class Geometry():
    def __init__(self, deck):
        self.deck = deck
        self.n = int(self.deck.doc["Problem Type"]["Number of Domains"])
        self.geometry()
        
        
        
    def geometry(self):
        self.Keys = []
        for i in range(self.n):
            self.Keys.append("Domain " + str(i + 1))
            
            
        self.Lx = {key: None for key in self.Keys}
        self.Ly = {key: None for key in self.Keys}
        for i in range(self.n):
            Lx = float(self.deck.doc["Geometry"]["Length X"]["Domain " + str(i+1)])
            Ly = float(self.deck.doc["Geometry"]["Length Y"]["Domain " + str(i+1)])
            self.Lx[self.Keys[i]] = Lx
            self.Ly[self.Keys[i]] = Ly
        
        
