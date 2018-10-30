import numpy as np
from numpy import sqrt, log, pi
from scipy.interpolate import interp1d
from SystemOfUnits import *
import pdb

class Trajectory():
    """
    Calculate the trajectory from a set of given parameters(E, B, L_M, etc)
    Draw Trajectory on the image
    """

    def __init__(self, q=1, m=2.014, B=0.44, E=20, L_M=10, L_ME=8, L_E=40, L_ES=8, scale=40):
        self.q = q * e        # charge of the ion
        self.m = m * u        # AUM mass of the ion
        self.B = B * T        # magnetic field in unit of Tesla
        self.E = E * kV/cm    # electric field in unit of V/m
        self.L_M = L_M * cm   # length of the magnet
        self.L_ME = L_ME * cm # length between the magnet and electrodes
        self.L_E = L_E * cm   # length of the electrode
        self.L_ES = L_ES * cm # length between the electrode and screen
        self.scale = scale    # image scale
        self.calculate()

    def calculate(self, energy_min=None, energy_max=None):
        """
        Calculate the trajectory
        Return the corespponding energy and x, y positon
        """

        if energy_min == None:
            #Minimum energy is 1MeV per charge
            energy_min = self.q*1e6
        if energy_max == None:
            #maximum energy is 100MeV per charge
            energy_max = self.q*80e6

        self.E_k = np.geomspace(energy_min, energy_max, 200) # kinetic energy of the ions
        E_m = self.m*c**2                                    # mass energy
        E_t = self.E_k + E_m                                 # total relativistic energy of the ions
        p = sqrt(E_t**2-E_m**2)/c                            # relativistic momentum
        gamma = self.E_k/E_m + 1                             # relativistic gamma factor
        r = p/(self.q*self.B)                                # cyclotron radius
        self.x0 = ((r-sqrt(r**2-self.L_M**2)) +
                self.L_M*(self.L_E+self.L_ME+self.L_ES)/sqrt(r**2-self.L_M**2))
        self.y0 = (self.q*self.E*(self.L_ES+self.L_E)*self.L_E
                / (p**2*(1-(self.L_M/r)**2)) * gamma * self.m)

    def transform(self, dx=0, dy=0, rotate=0):
        """
        dx, dy are the position of zero point of image
        rotate is the rotation of the image in degrees, if there is any
        """
        self.dx = dx
        self.dy = dy
        rotate = rotate * deg
        self.x = (np.cos(rotate)*self.x0 - np.sin(rotate)*self.y0)*self.scale*100 + dx
        self.y = (np.sin(rotate)*self.x0 + np.cos(rotate)*self.y0)*self.scale*100 + dy

    def getTrace(self):
        """return the trace"""
        return self.x, self.y

    def extracSpectrum(self, img):
        """"extract Spectrum from a given image"""
        fxE = interp1d(self.x, self.E_k)
        fxy = interp1d(self.x, self.y)
        (h, w) = img.shape
        width = 5 # the intergration width of the trace
        #find the index from where the trace is within the broundary of the image
        for i in range(len(self.x)):
            if round(self.x[i]) < w and round(self.y[i]) + width < h:
                break
        x = np.arange(np.floor(self.x[i]), np.ceil(self.x[-1]), -1, dtype=int)
        dN = np.zeros(len(x))

        for i in range(len(x)):
            #lower and upper intergration boundary on the y axis
            lower = int(fxy(x[i])) - width
            upper = int(fxy(x[i])) + width
            #sum up the signal within the width of the trace
            dN[i] = np.sum(img[lower:upper, x[i]])
        #calculate signal per energy interval
        dNdE = -dN/(fxE(x+0.5) - fxE(x-0.5))*MeV
        energy_range = fxE(x)/MeV
        # converte the spectrum to even energy space sampling
        # in order to reduce noise that are introduced by high sample rate at low energy
        fspec = interp1d(energy_range, dNdE)
        # rearrange the energy_range so that it evenly distributed
        n_sample = 200
        energy_range = np.linspace(energy_range[0], energy_range[-1], n_sample)
        self.dNdE = np.zeros(n_sample-1)
        # integrate between the new energy sample point E(i-1) and E(i)
        for i in range(1, n_sample):
            inte_x = np.linspace(energy_range[i-1], energy_range[i], 100)
            self.dNdE[i-1] = np.trapz(fspec(inte_x), inte_x)
        # set the middle value of the energy_range as the new energy value()
        self.energy = (energy_range[:-1] + energy_range[1:])/2
        return self.energy, self.dNdE

    def saveSpectrum(self, filename):
        """save the sepctrum to a file"""
        with open(filename, 'w') as f:
            f.write('Energy(MeV), dN/dE(PSL/MeV)\n')
            for e, n in zip(self.energy, self.dNdE):
                f.write('{}, {}\n'.format(e, n))
