import numpy as np
import os
import matplotlib.pyplot as plt
from astropy.table import Table

import lamost
import utils
import pandas as pd

plt.ioff()
catalog = lamost.load_catalog()
wavelengths = lamost.common_wavelengths
N, P = (len(catalog), wavelengths.size)

# Open the data arrays
all_observed_flux = np.memmap(
    os.path.join(lamost.LAMOST_PATH, "observed_flux.memmap"),
    mode="r", dtype='float32', shape=(N, P))

all_observed_ivar = np.memmap(
    os.path.join(lamost.LAMOST_PATH, "observed_ivar.memmap"),
    mode="r", dtype='float32', shape=(N, P))

all_model_flux = np.memmap(
    os.path.join(lamost.LAMOST_PATH, "model_flux.memmap"),
    mode="r", dtype="float32", shape=(N, P))

t = Table.read("Na_new_catalog.csv")

snrg = t["snrg"]
chi = t["cannon_red_chisq"]
starID=t["id"]

teff= t["cannon_teff"]
surfg= t["cannon_logg"]
met= t["cannon_m_h"]

Na5889_wavelength = t["Na_5890_wavelength"] 
Na5889_amp = t["Na_5890_amplitude"]
Na5889_amperr = t["Na_5890_amplitude_err"]
Na5896_wavelength = t["Na_5896_wavelength"] 
Na5896_amp = t["Na_5896_amplitude"]
Na5896_amperr = t["Na_5896_amplitude_err"]

N_Na5889 = (np.abs(Na5889_amp/(Na5889_amperr.astype(float) + 1e-10)) > 3) \
       * (chi < 3) \
       * (Na5889_amp < -0.05) \
       * (np.abs(Na5889_wavelength - 5889) < 2) \
       * (Na5889_amperr.astype(float) > 0)\
       * (snrg > 30)

N_Na5896 = (np.abs(Na5896_amp/(Na5896_amperr.astype(float) + 1e-10)) > 3) \
       * (chi < 3) \
       * (Na5896_amp < -0.05) \
       * (np.abs(Na5896_wavelength - 5896) < 2) \
       * (Na5896_amperr.astype(float) > 0)\
       * (snrg > 30)


N_Sodiumstars = N_Na5889*N_Na5889

print("Sodium matches: {}".format(sum(N_Sodiumstars)))

for index, star in enumerate(t):
    if not N_Sodiumstars[index]: continue

    observed_flux = all_observed_flux[index]
    observed_ivar = all_observed_ivar[index]
    model_flux = all_model_flux[index]

    fig = utils.plot_spectrum(wavelengths, observed_flux, observed_ivar, model_flux)   
    fig.axes[0].set_xlim(5869, 5909)
    fig.axes[1].set_xlim(5869, 5909)
    fig.axes[1].set_ylim(0.7, 1.2)
    fig.axes[1].axvline(5889.95, c="#666666", zorder=-1)
    fig.axes[1].axvline(5895.92, c="#666666", zorder=-1)
    string="Na Matches"+starID[index] + "Index: " + str(index)+" Teff: "+str(teff[index])+" SurfG: "+str(surfg[index])+" M: "+str(met[index])
    fig.suptitle(string)
    fig.savefig('Na_matchesamp0.05/' +str(index) +'.png')
    """
    fig = utils.plot_spectrum(wavelengths, observed_flux, observed_ivar, model_flux)   
    fig.axes[0].set_xlim(4000, 4600)
    fig.axes[1].set_ylim(0.7, 1.2)
    fig.axes[1].axvline(4077, c="#666666", zorder=-1)
    fig.axes[1].axvline(4554, c="#666666", zorder=-1)
    string="Ba4554 and St4077"+starID[index] + "Index: " + str(index)+" Teff: "+str(teff[index])+" SurfG: "+str(surfg[index])+" M: "+str(met[index])
    fig.suptitle(string)
    fig.savefig('Na5890+Na5896pics/' +str(index) +'Na' +'.png')
    """
    fig = utils.plot_spectrum(wavelengths, observed_flux, observed_ivar, model_flux)
    fig.axes[1].axvline(5889.95, c="#666666", zorder=-1)
    fig.axes[1].axvline(5895.92, c="#666666", zorder=-1)
    #fig.axes[1].axvline(5889, c="#666666", zorder=-1)
    string="Na full"+starID[index] + "Index: " + str(index)
    fig.suptitle(string)
    fig.savefig('Na_matchesamp0.05/'+str(index)+'full'+'.png')
    plt.close("all")

    del fig
    print(index)








