# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 10:00:53 2020

@author: andre
"""
import numpy as np

class Assembly():
    def __init__(self, deck, geometry,meshes):
        self.deck = deck
        self.geometry = geometry
        self.meshes = meshes
        self.Keys = meshes.Keys
        self.n = meshes.n
        self.set_Element_Position()
        self.set_element_in_matrix()
        self.set_elements_master_matrix()


    def set_Element_Position(self):
        self.ElementPosition = {key: [None, None] for key in self.Keys}
        for i in range(self.n):
            ElementXPosition = np.arange(self.meshes.nx.get("Domain " + str(i + 1))) * self.meshes.element.get("Domain " + str(i+1))[0] + np.ones(self.meshes.nx.get("Domain " + str(i+1))) * float(self.deck.doc["Assembly"]["Domain " + str(i+1)]["Offset X"])
            ElementYPosition = np.arange(self.meshes.ny.get("Domain " + str(i + 1))) * self.meshes.element.get("Domain " + str(i+1))[1] + np.ones(self.meshes.ny.get("Domain " + str(i+1))) * float(self.deck.doc["Assembly"]["Domain " + str(i+1)]["Offset Y"])
            self.ElementPosition[self.Keys[i]] = [ElementXPosition, ElementYPosition]
            
    def set_element_in_matrix(self):
        self.Mdx_individual = {key: None for key in self.Keys}
        self.Mdy_individual = {key: None for key in self.Keys}
        for i in range(self.n):
            Mdx_individual = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            Mdx_individual[:] = self.geometry.Lx.get("Domain " + str(i+1))/self.meshes.nx.get("Domain " + str(i+1))
            Mdy_individual = np.zeros((self.meshes.ny.get("Domain " + str(i + 1)), self.meshes.nx.get("Domain " + str(i + 1))))
            Mdy_individual[:] = self.geometry.Ly.get("Domain " + str(i+1))/self.meshes.ny.get("Domain " + str(i+1))
            self.Mdx_individual[self.Keys[i]] = Mdx_individual
            self.Mdy_individual[self.Keys[i]] = Mdy_individual
            
    def set_elements_master_matrix(self):
        Mdy = self.Mdy_individual["Domain 1"]
        Mdx = self.Mdx_individual["Domain 1"]
        ElementYPositon=self.ElementPosition["Domain 1"][1]
        for i in range(1, self.n):
            Mdy = np.concatenate((Mdy, self.Mdy_individual["Domain " + str(i+1)]))
            Mdx = np.concatenate((Mdx, self.Mdx_individual["Domain " + str(i+1)]))
            ElementYPositon=np.concatenate((ElementYPositon, self.ElementPosition["Domain " + str(i+1)][1]))
            self.Mdy = Mdy
            self.Mdx = Mdx
            self.Yposition = ElementYPositon
            self.Xposition = self.ElementPosition["Domain 1"][0]


        # aux=np.arange(1,4)        
        # if (self.ElementXPosition["Domain " +str(aux[0])].all() == self.ElementXPosition["Domain " + str(aux[1])].all()==self.ElementXPosition["Domain " +str(aux[2])].all())
        
    #     if all(self.ElementXPosition["Top Adherent"] == self.ElementXPosition["Bottom Adherent"]) and all(self.ElementXPosition["Top Adherent"] == self.ElementXPosition["HE"] ):
    #         self.Xposition=self.ElementXPosition.get("Top Adherent")
    #     else:
    #         print("Error")
            
    #     self.Yposition = np.concatenate((ElementYPosition["Bottom Adherent"], ElementYPosition["HE"]+ElementYPosition.get("Bottom Adherent")[-1],ElementYPosition["Top Adherent"]+ElementYPosition.get("HE")[-1]+ElementYPosition.get("Bottom Adherent")[-1]))
    