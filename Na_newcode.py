import numpy as np
import os
import matplotlib.pyplot as plt

import lamost
import utils


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

star_index = 10

observed_flux = all_observed_flux[star_index]
observed_ivar = all_observed_ivar[star_index]
model_flux = all_model_flux[star_index]

x, y, y_err, indices = lamost.get_data_to_fit(wavelengths, observed_flux,
    observed_ivar, model_flux, 4120, 4140)

p0 = np.array([-0.1,  4129, 2])

p_opt, p_cov = lamost.fit_gaussian(x, y, y_err, p0)




L = len(p_opt)
Na_p_opts_5890 = np.zeros((N,L))
Na_p_covs_5890 = np.zeros((N,L,L))
Na_p_opts_5896 = np.zeros((N,L))
Na_p_covs_5896 = np.zeros((N,L,L))

for index, star in enumerate(catalog):

    
    observed_flux = all_observed_flux[index]
    observed_ivar = all_observed_ivar[index]
    model_flux = all_model_flux[index]

    #Sodium doublet (Enhanced)
    x, y, y_err, indices = lamost.get_data_to_fit(wavelengths, observed_flux,
        observed_ivar, model_flux, 5879, 5899)
    try:
        p0 = np.array([-0.1, 5889.95, 2]) 
        p_optNa_5890, p_covNa_5890 = lamost.fit_gaussian(x, y, y_err, p0)
        p_opt_errorNa_5890 = np.sqrt(np.diag(p_covNa_5890))
    except ValueError:
        print('error encountered, moving on to next star')

    x, y, y_err, indices = lamost.get_data_to_fit(wavelengths, observed_flux,
        observed_ivar, model_flux, 5885, 5905)
    try:
        p0 = np.array([-0.1, 5895.92, 2]) 
        p_optNa_5896, p_covNa_5896 = lamost.fit_gaussian(x, y, y_err, p0)
        p_opt_errorNa_5896 = np.sqrt(np.diag(p_covNa_5896))
    except ValueError:
        print('error encountered, moving on to next star')


    Na_p_opts_5890[index] = p_optNa_5890
    Na_p_covs_5890[index] = p_covNa_5890
    Na_p_opts_5896[index] = p_optNa_5896
    Na_p_covs_5896[index] = p_covNa_5896

    print(index)


Na_p_opt_err_5890 = np.array([np.sqrt(np.diag(each)) for each in Na_p_covs_5890])
Na_p_opt_err_5896 = np.array([np.sqrt(np.diag(each)) for each in Na_p_covs_5896])


for index, label_name in enumerate(("amplitude", "wavelength", "sigma")):
    
    catalog["Na_5890_{}".format(label_name)] = Na_p_opts_5890[:, index]
    catalog["Na_5890_{}_err".format(label_name)] = Na_p_opt_err_5890[:, index]
    catalog["Na_5896_{}".format(label_name)] = Na_p_opts_5896[:, index]
    catalog["Na_5896_{}_err".format(label_name)] = Na_p_opt_err_5896[:, index]  




catalog.write("Na_new_catalog.csv")







