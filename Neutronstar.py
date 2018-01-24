import numpy as np 
import os
import matplotlib.pyplot as plt

from astropy import constants as const
import astropy as asp 



MilkyWayVol = 4/3*math.pi*15000 #radius of MW=15000 pc; Vol in pc^3
N_MWstars = 250*10^(9) # Average number of stars in MW (+/- 150 billion error)
N_MWgiants = 75300000
LAMOSTstars = 454180

Ejecta = const.M_sun*10^(-4.5)*u.kg #Typical Eu Neutron Star Ejecta in kg

#Merger rate from LIGO paper {Upper limits on the rates of binary neutron star 
#and neutron-star--black-hole mergers from Advanced LIGO's 
#first observing run}
Rate = 12600*(1000000129.6312)^(-3) #Upper limit NS merger rate per parsec cubed per year

Densityintime = Ejecta*Rate #kg*parsec^(-3)*yr^(-1)

LAMOST_MW_Frac = LAMOSTstars/N_MWgiants #percentage of Milky Way stars observed by Anna Ho

ObsMW = LAMOST_MW_Frac*MilkyWayVol #The observed volume of the Milky Way in parsec^3

AveStarMass = const.M_sun*0.8*u.kg #Average star mass

Eu_Fe = 0.7

Hatom_mass = 1.6737236*10^(-27) #kg

H_mass = AveStarMass*0.75 #Hydrogen mass in the star (kg)

N_Hatoms = H_mass/Hatom_mass

Fe_H = 0.0134 # Using Solar metallicity as average

Eu_H = Eu_Fe + Fe_H

N_Euatoms = 10^(Eu_H - 12)*N_Hatoms

Euatom_mass = 2.5234214*10^(-25)
Eu_mass = Euatom_mass*N_Euatoms #Total mass of Eu in each enhanced star (assuming average of [Eu/Fe]=0.7)

Eu47 = Eu_mass*47 #Total (average) mass of Eu in the 47 stars

Eu_density = Eu47*ObsMW #kg*parsec^(-3)

Years_required = Eu_density/Densityintime

print(Years_required)


