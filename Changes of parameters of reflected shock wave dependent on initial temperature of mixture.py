import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from sdtoolbox.postshock import CJspeed, PostShock_eq
from sdtoolbox.reflections import reflected_eq

# Initial state specification:
# P1 = Initial Pressure  
# T1 = Initial Temperature 
# U = Shock Speed 
# q = Initial Composition 
# mech = Cantera mechanism File name
# Tmax = maximal temperature

P1 = 100000
T1 = 300
Tmax = 1400
tab_T=[]
tab_P=[]
tab_D=[]
tab_U=[]

i=1
for T1 in range(300,Tmax,10):
    q = 'H2:2 O2:1 N2:3.56'    
    mech = 'Mevel2017.cti'         
    gas1 = ct.Solution(mech)
    gas1.TPX = T1, P1, q

    # create gas objects for other states
    gas2 = ct.Solution(mech)
    gas3 = ct.Solution(mech)
    
    # compute minimum incident wave speed
    cj_speed = CJspeed(P1, T1, q, mech)  
    
    # incident wave must be greater than or equal to cj_speed for
    # equilibrium computations
    UI = 1.2*cj_speed
        
    # compute postshock gas state object gas2
    gas2 = PostShock_eq(UI, P1, T1, q, mech);
    
    # compute reflected shock post-shock state gas3
    [p3,UR,gas3]= reflected_eq(gas1,gas2,gas3,UI);
    
    # Outputs:
    # p3 - pressure behind reflected wave
    # UR = Reflected shock speed relative to reflecting surface
    # gas3 = gas object with properties of postshock state
    

    # gas3 states stored in tables
    tab_T.append(gas3.T)
    tab_P.append(gas3.P/ct.one_atm)
    tab_D.append(gas3.density)
    tab_U.append(UR)

#generating plots
x = np.arange(300,Tmax,10)

fig, ax_T = plt.subplots()
ax_T.plot(x,tab_T)
ax_T.set(xlabel='T0 [K]', ylabel='Tr [K]', title='Temperature of reflected Shockwave')
ax_T.grid()
fig.savefig('C:/Users/user/Desktop/Temperature1.png', bbox_inches='tight', pad_inches=0.3)

fig, ax_P = plt.subplots()
ax_P.plot(x,tab_P)
ax_P.set(xlabel='T0 [K]', ylabel='Pr [atm]', title='Pressure of reflected Shockwave')
ax_P.grid()
fig.savefig('C:/Users/user/Desktop/Pressure1.png', bbox_inches='tight', pad_inches=0.3)

fig, ax_D = plt.subplots()
ax_D.plot(x,tab_D)
ax_D.set(xlabel='T0 [K]', ylabel='Dr [kg/m^3]', title='Density of reflected Shockwave')
ax_D.grid()
fig.savefig('C:/Users/user/Desktop/Density1.png', bbox_inches='tight', pad_inches=0.3)

fig, ax_U = plt.subplots()
ax_U.plot(x,tab_U)
ax_U.set(xlabel='T0 [K]', ylabel='Vr [m/s]', title='Velocity of reflected Shockwave')
ax_U.grid()
fig.savefig('C:/Users/user/Desktop/Velocity1.png', bbox_inches='tight', pad_inches=0.3)