import math as m
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Reaction mechanism GRI-Mech 3.0
gas = ct.Solution('gri30.xml')
# Energy which has to be provided in order to ignite the rocket fuel of A2 rocket motor
ignition_energy = 1.2*1550 # [kcal]
ign_energy = ignition_energy*4186.8 # [J]
# Outer combustion chamber (reactor) for ignition mixture will be used
d = 40.0 # mm diameter of the reactor
l = 100.0 # mm length of the reactor
Vr = m.pi*d*d*0.25*l/1000000000 # [m^3] volume of the reactor
mdot = 0.025 # [kg/s] mass flow in the reactor
mt = []
Tt = []
Qet = []
Eqt = []
tsim = 0.005 # [s] time spended in the reactor by flowing gases

eq_ratio = 0.6 # initial equivalence ratio
while eq_ratio < 1.6:
    print(eq_ratio)
    
    # gas definition, initial conditions and inlet
    gas.TP = 300.0, ct.one_atm*10
    gas.set_equivalence_ratio(eq_ratio, 'CH4:1.0', 'O2:1.0, N2:3.76')
    inlet = ct.Reservoir(gas)
    
    # filling combustor with a gas
    gas.equilibrate('HP')
    combustor = ct.IdealGasReactor(gas)
    combustor.volume = Vr
    
    # exhaust definition
    exhaust = ct.Reservoir(gas)
    
    # mass flow
    inlet_mfc = ct.MassFlowController(inlet, combustor, mdot=mdot)
    
    # simulation definition
    sim = ct.ReactorNet([combustor])
    
    # Reactor's states array
    states = ct.SolutionArray(gas)

    #Simulation
    sim.set_initial_time(0.0)  # reset the integrator
    sim.advance(tsim)
    states.append(combustor.thermo.state)
    V = mdot/combustor.density
    Q = -np.sum(states.net_production_rates * states.partial_molar_enthalpies)
    Qe = Q*V
    t = ign_energy/Qe
    mpal = mdot*t
    print('masa = {:.2f}; T = {:.1f};'.format(mpal, combustor.T))     
        
    # writing results to arrays
    mt.append(mpal)
    Tt.append(t)
    Qet.append(Qe)
    Eqt.append(eq_ratio)
    eq_ratio += 0.01
    print('Qe = {:.2f}; mpal = {:.2f}; t = {:.2f}'.format(Qe, mpal, t))
    Q=0.0
    mpal=0.0
    
#plots
f, ax1 = plt.subplots(1,1)
ax1.plot(Eqt, mt, '.-', color='C0')
ax2 = ax1.twinx()
ax1.set_xlabel('equivalence ratio [-]')
ax1.set_ylabel('mixture mass [kg]', color='C0')
ax2.plot(Eqt,Tt, '.-', color='C0')
ax2.set_ylabel('t [s]', color='C0')
f.tight_layout()
plt.show()