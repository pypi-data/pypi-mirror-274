#!/usr/bin/env python
##############################################################################
#
# Usage example for the procedure PPXF, which implements the
# Penalized Pixel-Fitting (pPXF) method originally described in
# Cappellari M., & Emsellem E., 2004, PASP, 116, 138
#     http://adsabs.harvard.edu/abs/2004PASP..116..138C
# upgraded in Cappellari M., 2017, MNRAS, 466, 798
#     http://adsabs.harvard.edu/abs/2017MNRAS.466..798C
# and with photometry in Cappellari M., 2023, MNRAS, 526, 3273C
#   https://ui.adsabs.harvard.edu/abs/2023MNRAS.526.3273C
#
# This example shows how to fit multiple stellar components with different
# stellar population and kinematics.
#
# MODIFICATION HISTORY:
#   V1.0.0: Early test version. Michele Cappellari, Oxford, 20 July 2009
#   V1.1.0: Cleaned up for the paper by Johnston et al. (MNRAS, 2013).
#       MC, Oxford, 26 January 2012
#   V2.0.0: Converted to Python and adapted to the changes in the new public
#       PPXF version, Oxford 8 January 2014
#   V2.0.1: Support both Python 2.6/2.7 and Python 3.x. MC, Oxford, 25 May 2014
#   V2.0.2: Support both Pyfits and Astropy to read FITS files.
#       MC, Oxford, 22 October 2015
#   V2.0.3: Use proper noise in input. MC, Oxford, 8 March 2016
#   V2.1.0: Replaced the Vazdekis-99 SSP models with the Vazdekis+10 ones.
#       MC, Oxford, 3 May 2016
#   V2.1.1: Make files paths relative to this file, to run the example from
#       any directory. MC, Oxford, 18 January 2017
#   V2.1.2: Updated MILES file names. MC, Oxford, 29 November 2017
#   V2.1.3: Changed imports for pPXF as a package.
#       Make file paths relative to the pPXF package to be able to run the
#       example unchanged from any directory. MC, Oxford, 17 April 2018
#   V2.1.4: Dropped legacy Python 2.7 support. MC, Oxford, 10 May 2018
#   V2.1.5: Fixed clock DeprecationWarning in Python 3.7.
#       MC, Oxford, 27 September 2018
#   V2.2.0: Illustrates the usage of the `constr_kinem` keyword.
#       MC, Oxford, 5 February 2020
#   V2.3.0: Modified usage example of the `constr_kinem` keyword.
#       MC, Oxford, 21 December 2020
#   V2.4.0: Use E-Miles spectral library. MC, Oxford, 16 March 2022
#   V2.5.0: Use the new `sps_util` instead of `miles_util`. 
#       MC, Oxford, 12 November 2023
#
##############################################################################

from pathlib import Path
from time import perf_counter as clock
from urllib import request

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util
import ppxf.sps_util as lib

##############################################################################
def ppxf_example_two_components():

    ppxf_dir = Path(util.__file__).parent

    lam_range_temp = [3500, 7500]
    sps_name = 'emiles'
    velscale = 35   # km/s

    # Read SPS models file from my GitHub if not already in the ppxf package dir.
    # The SPS model files are also available here https://github.com/micappe/ppxf_data
    basename = f"spectra_{sps_name}_9.0.npz"
    filename = ppxf_dir / 'sps_models' / basename
    if not filename.is_file():
        url = "https://raw.githubusercontent.com/micappe/ppxf_data/main/" + basename
        request.urlretrieve(url, filename)

    sps = lib.sps_lib(filename, velscale, wave_range=lam_range_temp)

    model1 = sps.templates[:, -2, -2]  # age = 12.59 Gyr [M/H] = 0
    model2 = sps.templates[:, 12, -2]  # age = 1.0 Gyr [M/H] = 0
    model1 /= np.median(model1)
    model2 /= np.median(model2)

    model = np.column_stack([model1, model2])
    galaxy = np.empty_like(model)

    # These are the input values in spectral pixels
    # for the (V,sigma) of the two kinematic components
    #
    vel = np.array([0., 300.])/velscale
    sigma = np.array([200., 100.])/velscale

    # The synthetic galaxy model consists of the sum of two
    # SSP spectra with age of 1Gyr and 13Gyr respectively
    # with different velocity and dispersion
    #
    for j in range(len(vel)):
        dx = int(abs(vel[j]) + 4.*sigma[j])   # Sample the Gaussian at least to vel+4*sigma
        v = np.linspace(-dx, dx, 2*dx + 1)
        losvd = np.exp(-0.5*((v - vel[j])/sigma[j])**2) # Gaussian LOSVD
        losvd /= np.sum(losvd)      # normalize LOSVD
        galaxy[:, j] = signal.fftconvolve(model[:, j], losvd, mode="same")
        galaxy[:, j] /= np.median(model[:, j])
    galaxy = np.sum(galaxy, axis=1)
    sn = 100.
    noise = np.full_like(galaxy, np.median(galaxy)/sn)
    galaxy = np.random.normal(galaxy, noise) # add noise to galaxy

    # Adopts two templates per kinematic component
    #
    templates = np.column_stack([model1, model2, model1, model2])
    goodPixels = np.arange(20, 6000)

    t = clock()
    plt.clf()

    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          "           No constraints on the kinematics\n"
          "--------------------------------------------------------")

    # With multiple stellar kinematic components a good starting velocity is essential.
    # Starting too far from the solution pPXF may *not* converge to the global minimum.
    # One should give different starting velocities for the two stellar components.
    # In general one should explore a grid of starting velocities as illustrated
    # e.g. in Sec.3.3 of Mitzkus et al. (2017 https://ui.adsabs.harvard.edu/abs/2017MNRAS.464.4789M)
    start = [[100, 200], [200, 200]]

    plt.subplot(211)
    plt.title("Two components pPXF fit")

    pp = ppxf(templates, galaxy, noise, velscale, start, goodpixels=goodPixels,
              plot=True, degree=4, moments=[2, 2], component=[0, 0, 1, 1])

    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          "  Constraint: sigma[0]/1.5 <= sigma[1] <= sigma[0]*1.5\n"
          "--------------------------------------------------------")

    # In this example I constrain the two sigmas to be within 50%
    # of each other: 1/1.5 <= sigma[1]/sigma[0] <= 1.5.
    # The best fit is at the boundary of the feasible region.
    A_ineq = [[0, 1/1.5, 0, -1],  # sigma0/1.5 - sigma1 <= 0
              [0, -1.5, 0, 1]]    # -sigma0*1.5 + sigma1 <= 0
    b_ineq = [0, 0]
    constr_kinem = {"A_ineq": A_ineq, "b_ineq": b_ineq}

    pp = ppxf(templates, galaxy, noise, velscale, start,
              goodpixels=goodPixels, degree=4, moments=[2, 2],
              component=[0, 0, 1, 1], constr_kinem=constr_kinem)

    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          "               Single component pPXF fit\n"
          "--------------------------------------------------------")

    plt.subplot(212)
    plt.title("Single component pPXF fit")

    start = [100, 200]
    pp = ppxf(templates, galaxy, noise, velscale, start,
              goodpixels=goodPixels, plot=True, degree=4, moments=2)

    print("==============================================")
    print("Total elapsed time %.2f s" % (clock() - t))

    plt.tight_layout()
    plt.pause(5)


#------------------------------------------------------------------------------

if __name__ == '__main__':

    np.random.seed(123)  # For reproducible results
    ppxf_example_two_components()
