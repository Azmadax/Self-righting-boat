#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 14:44:14 2025

@author: nicolasfihey
"""
import numpy as np
import matplotlib.pyplot as plt


L=2 # Width of rectangle
l=1 # height of rectangle
N=100 # Number of points
OG_dimensionless= np.array([0, 0])# dimensionless horizontal and vertical offset from center of rectangle
GZ=[] # List containing the righting arm for different angle

"""rectangle sitting on water"""

alpha_deg = np.linspace(0, 90, N) # We stop at 90 degrees because afterward the point of contact is changing.
GZ.append(0) # No torque when rectangle is at horizontal
for i in range(N-1):
    OG = OG_dimensionless*np.array([L, l])
    CG = L/2+OG[0] + (l/2 +OG[1])*1j # Define vector from corner to center of gravity using complex
    CG_rotated = CG*np.exp(1j*np.radians(alpha_deg[i+1]))
    GZ.append(CG_rotated.real) # Take real part to project on horizontal axis

plt.plot(alpha_deg,GZ)
plt.title("GZ rectangle on water")
plt.xlabel('Heel angle alpha (°)')
plt.ylabel('Righting arm GZ (m)')
plt.grid(True)
plt.show()
