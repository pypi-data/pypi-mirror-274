import tkinter as tk
import os
from scipy.signal import savgol_filter
import numpy as np
from tkinter import *
from tkinter import filedialog, Menu
from tkinter import ttk
import datetime
from SACMES_PYTHON_PACKAGE.GUI import MainWindow
from SACMES_PYTHON_PACKAGE.GUI_CA import Controller

handle_variable = ''
electrodes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
method=""
InputFrequencies = [30,80,240]

class Model:
    def __init__(self,method):
        self.method = method

    def animate(self):
        if self.method == "SWV":
            root = tk.Tk()
            app = MainWindow(root)
            root.mainloop()
        else:
            root = tk.Tk()
            app = Controller(master=root)
            root.mainloop()

    
















"""
def readData(self,filepath):
        print(filepath)
        with open(filepath,'r',encoding='utf-8') as file:
         for line in file:
            values = line.split()
            self.currents.append(values[0])
        print(self.currents)
    
    def data_analysis(self):
        self.currents = Savitzky_smoothing(self.currents,self.sg_degree)
        Polynomial_fit(self.potential,self.currents,self.polyfit_deg)
        return
        
        

def Savitzky_smoothing(currents,sg_degree):
    smooth_currents = savgol_filter(currents, 15, sg_degree)
    return smooth_currents

def Polynomial_fit(adjusted_potentials,adjusted_currents,polyfit_deg):
    polynomial_coeffs = np.polyfit(adjusted_potentials,adjusted_currents,polyfit_deg) # returns the coefficients of the polynomial regression line
    eval_regress = np.polyval(polynomial_coeffs,adjusted_potentials).tolist() # At each adjusted_potential, what is the y value indicated by the regression line
    regression_dict = dict(zip(eval_regress, adjusted_potentials))      # dictionary with current: potential (after regression)
    fit_half = round(len(eval_regress)/2)
    min1 = min(eval_regress[:-fit_half])
    min2 = min(eval_regress[fit_half:])
    max1 = max(eval_regress[:-fit_half])
    max2 = max(eval_regress[fit_half:])
    linear_fit = np.polyfit([regression_dict[min1],regression_dict[min2]],[min1,min2],1)
    linear_regression = np.polyval(linear_fit,[regression_dict[min1],regression_dict[min2]]).tolist()
"""

    
    




    



        
            