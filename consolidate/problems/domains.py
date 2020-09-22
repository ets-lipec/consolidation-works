import numpy as np
class RectangularDomain:

    def __init__(self, name, corner0, corner1, ex0, ex1, ey0, ey1, position, material, initialcondition, extboundarycond, mesh ):
        self.corners={"X" : [float(corner0[0]), float(corner1[0])], "Y" : [float(corner0[1]),float(corner1[1])]}
        self.dimensions = {"Lx" : float(corner1[0]) - float(corner0[0]), "Ly" : float(corner1[1])-float(corner0[1])}
        self.elements = {"Elements in X":[ex0, ex1], "Elements in Y": [ey0,ey1]}
        self.name = name
        self.material = material.copy()
        self.mesh = mesh.copy()
        self.initial_fields = initialcondition.copy()
        self.external_boundary_fields= extboundarycond.copy()
        self.position = position

    # def test(self, point):
    #     if point[0] >= self.x0 and point[0] <= self.x1 and point[1] >= self.y0 and point[1] <= self.y1:
    #         return True
    #     else:
    #         return False

    def test_mesh(self, mesh):
        if mesh[0] >= self.elements["Elements in Y"][0] and mesh[0] <= self.elements["Elements in Y"][1] and mesh[1] >= self.elements["Elements in X"][0] and mesh[1]<= self.elements["Elements in X"][1]:
        # if mesh[0] >= self.ey0 and mesh[0] <= self.ey1 and mesh[1] >= self.ex0 and mesh[1]<= self.ex1:
            # import pdb; pdb.set_trace()
            return True
        else:
            return False

    def set_field_init_value(self, field_dict):
        for key, value in field_dict.items():
            self.initial_fields[key] = float(value)

    def generate_mask(self, totalNy, totalNx):
        m=np.zeros((totalNy, totalNx))
        maux=np.zeros((totalNy+2, totalNx+2))
        self.mask = m.copy()
        self.mask_external_boundary={}
        self.mask_contact_interface={}
        mask_left= maux.copy()
        mask_right= maux.copy()
        mask_top= maux.copy()
        mask_bottom= maux.copy()
        contact_mask=m.copy()
        contact_mask_middle_top = m.copy()
        contact_mask_middle_bottom = m.copy()
        for x_i in range (0,np.shape(m)[0]):
            for y_i in range (0,np.shape(m)[1]):
                if self.test_mesh( (x_i, y_i) ):
                    self.mask[x_i][y_i] = 1
                    mask_left[x_i+1][0]=1
                    mask_right[x_i+1][-1]=1
                    self.mask_external_boundary.update({"Left Edge":mask_left})
                    self.mask_external_boundary.update({"Right Edge":mask_right})
                    
                    if self.position ==1:
                        # import pdb; pdb.set_trace()
                        mask_bottom[self.elements["Elements in Y"][0]][y_i+1]=1
                        contact_mask[self.elements["Elements in Y"][1]][y_i] = 1
                        self.mask_external_boundary.update({"Bottom Edge": mask_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask})
                    if self.position ==3:
                        mask_top[-1][y_i+1]=1
                        self.mask_external_boundary.update({"Top Edge": mask_top})
                        contact_mask[self.elements["Elements in Y"][0]][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask})
                    if self.position ==2:
                        contact_mask_middle_bottom[self.elements["Elements in Y"][0]][y_i] = 1
                        contact_mask_middle_top[self.elements["Elements in Y"][1]][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask_middle_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask_middle_top})
                        
