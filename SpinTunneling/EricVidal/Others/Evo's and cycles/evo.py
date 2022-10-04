#%% 1. Initial parameters
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 18:14:16 2022

@author: Eric Vidal Marcos
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp

#Arbitrary spin to study
s=3     #total spin
dim=round(2*s+1)    #in order to work when s is half-integer with int dim
Nterm1=s*(s+1)      #1st term of N+-

#Hamiltonian Parameters
D=5
hz=2.5
B=0.7

#Time span
At=[-5,30]

#IC
a_m0=[]
a_m0.append(1+0j)
for i in range(dim-1):
    a_m0.append(0+0j)




#Transition times
#Because of Hamiltonian symetry transitions can only occur s times
#which correspond to each level from the metastable state opposite to the true
#ground state, and then goes up or down dependig which is the true ground state
#m=s or m=-s, and changes from steps of 2
time_n=[]
for i in range(s):
    time_n.append((D/hz)*(2*i))

#States energies if H_0
energies=[]
for i in range(dim):
    energies.append([])
for i in range(dim):
    for j in range(2):
        energies[i].append(-D*(i-s)**2-hz*At[j]*(i-s))
#%% 2. Coupled differential equations
#WE HAVE TO TAKE INTO ACCOUNT THAT M DOESNT GO FROM -S TO S
#IT GOES FROM 0 TO DIM-1=2s

#N+ and N- definition
def Np(m):
    m=m-s   #cuz m goes from 0 to 2s
    Nplus=np.sqrt(Nterm1-m*(m+1))
    return Nplus
def Nm(m):
    m=m-s   #cuz m goes from 0 to 2s
    Nminus=np.sqrt(Nterm1-m*(m-1))
    return Nminus

#PER TESTEJAR SI EL METODE ES CORRECTE, COMPARAREM AMB RESULTATS LAURA
#definition of ODE's
def dak1(s, k, t, am):
    '''Inputs: s (int) total spin, k (int) quantum magnetic number,
    t (int or float) time, am (array (dim,1)) coefficients of each state.
    Outputs: dak (complex) time derivative of a_k.
    This function returns each differential equation for coefficients time
    evolution.'''
    #First we define k to the scale we work in QM
    kreal=k-s
    if (kreal>s):
        print('It makes no sense that k>s or k<s, sth went wrong.')
        exit()
        
    #eigenvalues term
    eigenterm=am[k]*(-D*kreal**2-hz*t*kreal)
    
    #summatory term
    sumterm=0
    for m in range(dim):
        #first we apply Kronicker deltas
        if (k==(m+2)):
            sumtermpos=Np(m)*Np(m+1)
        else:
            sumtermpos=0
            
        if (k==(m-2)):
            sumtermneg=Nm(m)*Nm(m-1)
        else:
            sumtermneg=0
            
        #and obtain summatory term along the for
        sumterm += am[m]*(B/2)*(sumtermpos+sumtermneg)
    
    #finally obtaining the result of one differential equation
    dak=-1j*(eigenterm+sumterm)
    return dak

def odes(t, a_m):
    '''Input: t (int or float) time and a_m (1D list) coefficients. D, h, B
    (int or floats) are Hamiltonian parameters that could be omitted because
    they are global variables as s (spin).
    Ouput: system (1D list), this is the coupled differential equation
    system.'''
    system=[]
    for i in range(dim):
        system.append(dak1(s, i, t, a_m))
    
    return system

#test the defined function odes
print(odes(0, a_m0))

#%% 3. Resolution and plotting

#solve
a_m=solve_ivp(odes, At, a_m0)

#Plotting parameters
t=a_m.t[:]  #time

aplot=[]
for i in range(dim):
    aplot.append(np.abs(a_m.y[i,:])**2)     #Probabilities coeff^2

norm = np.sum(aplot, axis=0)    #Norm (sum of probs)

#Plot
plt.figure()
plt.subplot(221)
plt.title('General spin method, solve_ivp')
plt.xlabel('t')
plt.ylabel('$|a|^2$')
plt.axhline(y=1.0,linestyle='--',color='grey')
for i in range(s):
    plt.axvline(x=time_n[i],linestyle='--',color='grey')
for i in range(dim):
    plt.plot(t, aplot[i],'-',label='m='+str(i-s))
plt.plot(t, norm,'-',label='norma')
plt.legend()
plt.subplot(222)
plt.title('States energies if $\mathcal{H}_0$')
plt.xlabel('t')
plt.ylabel('$E$')
for i in range(s):
    plt.axvline(x=time_n[i],linestyle='--',color='grey')
for i in range(dim):
    plt.plot(At, energies[i],'-',label='$E_{'+str(i-s)+'}$')
plt.legend()


#Magnetization
magne=np.zeros(np.size(aplot[0]))
for i in range(dim):
    magne=magne+aplot[i]*(i-s)
    
    
plt.subplot(223)
plt.title('Principi Cicle')
plt.xlabel('t')
plt.ylabel('M')
for i in range(s):
    plt.axvline(x=time_n[i],linestyle='--',color='grey')
plt.plot(t, magne,'-')
plt.show()
plt.tight_layout()