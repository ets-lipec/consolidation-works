
import numpy as np
class HeatTransfer:

    def __init__(self, deck,meshes,assembles,BC):
        self.dt = float(deck.doc["Simulation"]["Time Step"])
        self.BC=BC
        self.Mdy = assembles.Mdy
        self.Mdx = assembles.Mdx
        self.dx2 = self.Mdx*self.Mdx
        self.dy2 = self.Mdy*self.Mdy        
        self.meshes = meshes
        self.h= float(deck.doc["Boundary Condition"]["Convective Coefficient"])
        
        

    def do_convection(self, u0, u, Diffx, Diffy):
        
        Q=np.zeros(np.shape(self.BC.T))
        Q[0,:]   =  self.h*(float(self.BC.Troom) - u[0,:])
        Q[-1,:]  =  self.h*(float(self.BC.Troom) - u[-1,:])
        Q[:,-1]  =  self.h*(float(self.BC.Troom) - u[:,-1])
        Q[:,0]   =  self.h*(float(self.BC.Troom) - u[:,-1])
        
        Q[0,0]   =  self.h*(float(self.BC.Troom)  - u[0,0])
        Q[-1,0]  =  self.h*(float(self.BC.Troom) - u[-1,0])
        Q[0,-1]  =  self.h*(float(self.BC.Troom) - u[0,-1])
        Q[-1,-1] =  self.h*(float(self.BC.Troom) - u[-1,-1])
        self.Q=Q
        
        
        valueX=np.zeros(np.shape(self.BC.T))
        valueX[:,0 ]  = -Q[:,0]/ self.BC.Kx[:,0]
        valueX[:,-1]  = -Q[:,-1]/self.BC.Kx[:,-1]
    
        valueX[0,0]   = -Q[0,0]/self.BC.Kx[0,0]
        valueX[-1,0]  = -Q[-1,0]/self.BC.Kx[-1,0]
        valueX[0,-1]  = -Q[0,-1]/self.BC.Kx[0,-1]
        valueX[-1,-1] = -Q[-1,-1]/self.BC.Kx[-1,-1]
        self.valueX = valueX
        
        
        valueY = np.zeros(np.shape(self.BC.T))
        valueY[0,:]   = -Q[0,:]/ self.BC.Ky[0,:]
        valueY[-1,:]  = -Q[-1,:]/self.BC.Ky[-1,:]
        
        valueY[0,0]   = -Q[0,0]/self.BC.Ky[0,0]
        valueY[-1,0]  = -Q[-1,0]/self.BC.Ky[-1,0]
        valueY[0,-1]  = -Q[0,-1]/self.BC.Ky[0,-1]
        valueY[-1,-1] = -Q[-1,-1]/self.BC.Ky[-1,-1]
        self.valueY = valueY
        
        
        UoutX = np.zeros(np.shape(self.BC.T))     
        UoutX[:,-1]   = u[:,-1]  -2*self.Mdx[:,-1]*valueX[:,-1]
        UoutX[:,0]    = u[:,0]   -2*self.Mdx[:,0] *valueX[:,0]
        
        UoutX[0,0]    = u[0,0]   -2*self.Mdx[0,0]*valueX[0,0] 
        UoutX[0,-1]   = u[0,-1]  -2*self.Mdx[0,-1]*valueX[0,-1] 
        UoutX[-1,0]   = u[-1,0]  -2*self.Mdx[-1,0]*valueX[-1,0] 
        UoutX[-1,-1]  = u[-1,-1] -2*self.Mdx[-1,-1]*valueX[-1,-1]    
        self.UoutX = UoutX
        
        
        UoutY=np.zeros(np.shape(self.BC.T))
        UoutY[0,:]    = u[0,:]   -2*self.Mdy[0,:] *valueY[0,:]        
        UoutY[-1,:]   = u[-1,:]  -2*self.Mdy[-1,:]*valueY[-1,:]
        
        UoutY[0,0]    = u[0,0]   -2*self.Mdy[0,0]*valueY[0,0]
        UoutY[0,-1]   = u[0,-1]  -2*self.Mdy[0,-1]*valueY[0,-1]
        UoutY[-1,0]   = u[-1,0]  -2*self.Mdy[-1,0]*valueY[-1,0]
        UoutY[-1,-1]  = u[-1,-1] -2*self.Mdy[-1,-1]*valueY[-1,-1]    
        self.UoutY = UoutY
        
        
        
        
        
        u[0,1:-1]     = u0[0,1:-1]     + Diffy[0,1:-1] *self.dt*      ((u0[1,1:-1]    -2*u[0,1:-1]      + UoutY[0,1:-1]) /self.dy2[0,1:-1])      + Diffx[0,1:-1] *self.dt*       ((u0[0, 2:]    -2*u0[0,1:-1]     +u0[0,:-2])/self.dx2[0,1:-1]) 
        u[-1,1:-1]    = u0[-1,1:-1]    + Diffy[-1,1:-1]*self.dt*      ((u0[-2,1:-1]   -2*u[-1,1:-1]     + UoutY[-1,1:-1])/self.dy2[-1,1:-1])     + Diffx[-1,1:-1]*self.dt*       ((u0[-1, 2:]   -2*u0[-1,1:-1]    +u0[-1,:-2])/self.dx2[-1,1:-1]) 
        
        u[1:-1,0]     = u0[1:-1,0]     + Diffy[1:-1,0] *self.dt*      ((u0[2:,0 ]     -2*u[1:-1,0]      + u0[0:-2,0]) /self.dy2[1:-1,0])       + Diffx[1:-1, 0]*self.dt*       ((u0[1:-1, 1 ] -2*u0[1:-1,0]     +UoutX[1:-1,0])/self.dx2[1:-1,0])        
        u[1:-1,-1]    = u0[1:-1,-1]    + Diffy[1:-1,-1]*self.dt*      ((u0[2:,-1]     -2*u[1:-1,-1]     + u0[0:-2,-1])/self.dy2[1:-1,-1])      + Diffx[1:-1,-1]*self.dt*       ((u0[1:-1, -2 ]-2*u0[1:-1,-1]    +UoutX[1:-1,-1])/self.dx2[1:-1,-1]) 

        u[0,0]   = u0[0,0]      +Diffy[0,0]      *self.dt*((u0[1,0]   -2*u[0,0]    + UoutX[0,0])/self.dy2[0,0])         +Diffx[0,0]     *self.dt*((u0[0, 1]     -2*u0[0,0]    +UoutY[0,0])/self.dx2[0,0])
        u[-1,0]  = u0[-1,0]     +Diffy[-1,0]     *self.dt*((u0[-2,0]  -2*u[-1,0]   + UoutX[-1,0])/self.dy2[-1,0])       +Diffx[-1,0]    *self.dt*((u0[-1, 1]    -2*u0[-1,0]   +UoutY[-1,0])/self.dx2[-1,0])  
        u[0,-1]  = u0[0,-1]     +Diffy[0,-1]     *self.dt*((u0[1,-1]  -2*u[0,-1]   + UoutX[0,-1])/self.dy2[0,-1])       +Diffx[0,-1]    *self.dt*((u0[0, -2]    -2*u0[0,-1]   +UoutY[0,-1])/self.dx2[0,-1])
        u[-1,-1] = u0[-1,-1]    +Diffy[-1,-1]    *self.dt*((u0[-2,-1] -2*u[-1,-1]  + UoutX[-1,-1])/self.dy2[-1,-1])     +Diffx[-1,-1]   *self.dt*((u0[-1,-2]    -2*u0[-1,-1]  +UoutY[-1,-1])/self.dx2[-1,-1])


        # u[self.meshes.ny.get("Bottom Adherent"),0]   = u0[self.meshes.ny.get("Bottom Adherent"),0]      +self.dt*(self.BC.q)/(self.BC.Rho[self.meshes.ny.get("Bottom Adherent"),0] *self.BC.Cp[self.meshes.ny.get("Bottom Adherent"),0])
        # u[self.meshes.ny.get("Bottom Adherent"),:]  = u0[self.meshes.ny.get("Bottom Adherent"),-:]     +self.dt*(self.BC.q)/(self.BC.Rho[self.meshes.ny.get("Bottom Adherent"),-1]*self.BC.Cp[self.meshes.ny.get("Bottom Adherent"),:])
        
        u0 = u.copy()
        
        return u0,u 
    def do_timestep(self, u0, u, Diffx, Diffy,Q):
        # Propagate with forward-difference in time, central-difference in space
        u[1:-1, 1:-1] = u0[1:-1, 1:-1] + Diffy[1:-1, 1:-1]* self.dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/self.dy2[1:-1, 1:-1] ) + Diffx[1:-1, 1:-1]* self.dt * ( (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/self.dx2[1:-1, 1:-1] ) + self.dt*Q[1:-1,1:-1]/(self.BC.Cp[1:-1,1:-1]*self.BC.Rho[1:-1,1:-1])

        u0 = u.copy()
        
        return u0, u