# -*- coding: utf-8 -*-
import numpy as np


class SolvesTwoPlates:
    
    def __init__(self, deck,meshes,BC,model_HT,model_IC,plots):
        self.deck = deck
        self.meshes = meshes
        self.BC = BC
        self.model_HT=model_HT
        self.model_IC=model_IC
        self.plots = plots
        self.do_solver()
        
    def do_solver(self):
        for m in range(int(self.deck.doc["Simulation"]["Number Time Steps"])):
# -------------- CALCULATE TEMPERATURE FOR EACH STEP INCREMENT----------
            self.BC.T0, self.BC.T = self.model_HT.do_convection(self.BC.T0, self.BC.T, self.BC.DiffX, self.BC.DiffY)
            self.BC.T0, self.BC.T = self.model_HT.do_timestep(self.BC.T0, self.BC.T, self.BC.DiffX, self.BC.DiffY, self.BC.Q)
# -------------- FORCE TEMPERATURE AT THE INTERFACE: ISOTHERMAL CONDITION----------
            # self.BC.T[50, 1:-1] = self.deck.doc["Boundary Condition"]["Ideal Temperature"]
# -------------- CALCULATE VISCOSITY FOR EACH STEP INCREMENT----------
            self.BC.Visc=self.model_IC.viscosity_timestep(self.BC.Visc, self.BC.T)
# # -------------- CALCULATE Dic FOR EACH STEP INCREMENT----------
            self.BC.Dic=self.model_IC.dic_timestep(self.BC.Dic, self.BC.Dic0, self.BC.Visc, float(self.deck.doc["Simulation"]["Time Step"]))
            self.BC.Dic=np.clip(self.BC.Dic, 0, 1)
# -------------- DO PLOT ACCORDING TO THE SELECTED INTERVAL----------             
            if m in self.plots.mfig:
                self.plots.update_Dic(self.BC.Dic)
                self.plots.update_T(self.BC.T)
                self.plots.do_plots(m)    
        self.plots.do_animation()
        # self.model_IC.calculate_average_dic()