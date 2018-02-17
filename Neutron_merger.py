# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:38:17 2018

@author: Matt
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import math

from astropy import units as u
from astropy import constants as const
import astropy as asp



MilkyWayVol = 4/3*math.pi*(15000*u.pc)**3 #radius of MW=15000 pc; Vol in pc^3
N_MWstars = 250*10^(9) # Average number of stars in MW (+/- 150 billion error)
N_MWgiants = 75300000
LAMOSTstars = 454180

Ejecta = 1.989*10**(30)*10**(-4.5)*u.kg #Typical Eu Neutron Star Ejecta in kg from Ji's Paper

#Upper limit Merger rate from LIGO paper {Upper limits on the rates of binary neutron star
#and neutron-star--black-hole mergers from Advanced LIGO's
#first observing run}

#Lower limit merger rate from 1991 paper; author: Phinney E.S. {The rate of neutron star binary mergers in the universe
# - Minimal predictions for gravity wave detectors}

Rate = (10**(-6))*(u.Mpc**(-3))/(u.yr) #Lower limit
#Rate = 12600*(u.Gpc**(-3))/(u.yr) #Upper limit NS merger rate per parsec cubed per year

Densityintime = Ejecta*Rate #kg*parsec^(-3)*yr^(-1)

LAMOST_MW_Frac = float(LAMOSTstars)/N_MWgiants #percentage of Milky Way stars observed by Anna Ho

ObsMW = LAMOST_MW_Frac*MilkyWayVol #The observed volume of the Milky Way in parsec^3

AveStarMass = 1.989*10**(30)*0.8*u.kg#Average star mass in kg

Eu_Fe = 0.7

Hatom_mass = 1.6737236*10**(-27)*u.kg #kg

H_mass = AveStarMass*0.75 #Hydrogen mass in the star (kg)

N_Hatoms = H_mass/Hatom_mass

Fe_H = 0.0134 # Using Solar metallicity as average

Eu_H = Eu_Fe + Fe_H

N_Euatoms = 10**(Eu_H - 12)*N_Hatoms

Euatom_mass = 2.5234214*10**(-25)*u.kg
Eu_mass = Euatom_mass*N_Euatoms #Total mass of Eu in each enhanced star (assuming average of [Eu/Fe]=0.7)

Eu60 = Eu_mass*61 #Total (average) mass of Eu in the 60 stars

Eu_density = Eu60/ObsMW #kg*parsec^(-3)

Years_required = Eu_density/Densityintime

print(Years_required)

Age_universe = 13.8*10**9*u.yr

Density = Densityintime*Age_universe

N_starsinvol = Density/Eu_mass

N_stars = N_starsinvol*MilkyWayVol


# How many should there be in LAMOST?
N_stars_in_LAMOST = N_stars * (float(LAMOSTstars)/N_MWgiants)

print("Number of r-process stars within 15 kpc sphere of Milky  Way: {:.0f}".format(
    N_stars.to(1)))

print("Number of r-process giants expected in LAMOST from NSM: {:.0f}".format(
    N_stars_in_LAMOST.to(1)))

# ((N_stars.to(1))/(250*10**9))*2200000 Relevant code for below
# ((N_stars.to(1))/(75300000))*450000
# ((N_stars.to(1))/(250*10**9))*450000

# Use the rate of neutron star merger we have to find how many r-processed stars we should find as compared to what we do find
# How many r-processed stars we would have to find in order to make the rates inconsistent = 125589.03
# Number of stars we expect to find from the sample is 1.1051835 assumptions probably wrong


#From the lower limit we find that this could occur in 8.511*10**11 yrs, so definitely couldn't happen.
