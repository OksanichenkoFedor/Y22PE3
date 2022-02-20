import config

class AC_contur():
    def __init__(self):
        pass

    def z1(self, w):
        return complex(config.glob_E_R1, 0)

    def z2(self, w):
        return complex(0, w*config.glob_E_L1)

    def z3(self, w):
        return complex(config.glob_E_r, (w*config.glob_E_L2 - 1.0/(w*config.glob_E_C2))  )

    def z4(self, w):
        return complex(0, (-1.0)/(w*config.glob_E_C1) )

    def z5(self, w):
        return complex(config.glob_E_R2, 0)

    def i(self, w):
        z1 = self.z1(w)
        z2 = self.z2(w)
        z3 = self.z3(w)
        z4 = self.z4(w)
        z5 = self.z5(w)
        up = z3*(z4+z5) + z1*(z3+z4+z5) + z2*(z3+z4+z5)
        down = z1*z2*(z3+z4) + z3*z4*z5 + z1*z5*(z2+z3+z4) + z2*z4*(z3+z5)
        return abs(up/down)

    def u(self, w):
        z1 = self.z1(w)
        z2 = self.z2(w)
        z3 = self.z3(w)
        z4 = self.z4(w)
        z5 = self.z5(w)
        up = z3*(z2*z4-z1*z5)
        down = z1*z2*(z3+z4) + z3*z4*z5 + z1*z5*(z2+z3+z4) + z2*z4*(z3+z5)
        return abs(up / down)

