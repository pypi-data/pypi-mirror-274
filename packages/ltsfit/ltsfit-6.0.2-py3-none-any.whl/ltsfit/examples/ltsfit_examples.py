#!/usr/bin/env python
# V1.0.0: Michele Cappellari, Oxford, 5 November 2014
# V1.0.1: Fixed deprecation warning. MC, Oxford, 1 October 2015
# V1.0.2: Changed imports for ltsfit as package. MC, Oxford, 17 April 2018
# V2.0.0: Adapted to use the new general ltsfit.ltsfit. MC, Oxford, 7 July 2023

import numpy as np
import matplotlib.pyplot as plt

from ltsfit.ltsfit import ltsfit

#------------------------------------------------------------------------------

def lts_linefit_example():
    """
    Usage example for ltsfit() fitting a line in 2-dim.
    In this example I assume that 10% of the values are strong outliers.

    """
    print('-'*70 + "\nExample fitting a line in 2-dim\n" + '-'*70 + '\n')

    ntot = 300  # Total number of values
    frac = 0.1  # fraction of outliers

    # Coefficients of the test line
    a = 10.
    b = 1.

    n = int(ntot*(1 - frac))  # (1 - frac) good values
    rng = np.random.default_rng(913)
    x = rng.uniform(18, 21, n)
    y = a + b*x

    sig_int = 0.3 # Intrinsic scatter in y
    y += rng.normal(0, sig_int, n)

    sigx = 0.1 # Observational error in x
    sigy = 0.2 # Observational error in y
    x += rng.normal(0, sigx, n)
    y += rng.normal(0, sigy, n)

    # Outliers produce a background of spurious values
    # intersecting with the true distribution
    #
    nout = int(ntot*frac)   # frac outliers
    x1 = rng.uniform(np.mean(x), max(x), nout)
    y1 = rng.uniform(20, 26, nout)
    y1 = np.mean(y) + rng.uniform(0, np.ptp(y), nout)

    # Combines the good values and the outliers in one vector
    #
    x = np.append(x, x1)
    y = np.append(y, y1)

    sigx = np.full_like(x, sigx)  # Adopted error in x
    sigy = np.full_like(x, sigy)  # Adopted error in y

    plt.clf()
    pivot = np.round(np.median(x))
    p = ltsfit(x, y, sigx, sigy, pivot=pivot)
    plt.pause(1)

    # Illustrates how to obtain the best-fitting values from the class
    print(f"The best fitting parameters are: {p.coef}\n")

#------------------------------------------------------------------------------

def lts_planefit_example():
    """
    Usage example for ltsfit() fitting a plane in 3-dim.
    In this example I assume that 10% of the values are strong outliers.

    """
    print('-'*70 + "\nExample fitting a plane in 3-dim\n" + '-'*70 + '\n')

    ntot = 300  # Total number of values
    frac = 0.1  # fraction of outliers

    # Coefficients of the test plane
    a = 10.
    b = 2.
    c = 1.

    n = int(ntot*(1 - frac))  # (1 - frac) good values
    rng = np.random.default_rng(913)
    x = rng.uniform(17.5, 22.5, n)
    y = rng.uniform(7.5, 12.5, n)
    z = a + b*x + c*y

    sig_int = 1  # Intrinsic scatter in z
    z = rng.normal(z, sig_int, n)

    sigx = 0.2  # Observational error in x
    sigy = 0.4  # Observational error in y
    sigz = 0.4  # Observational error in z
    x = rng.normal(x, sigx, n)
    y = rng.normal(y, sigy, n)
    z = rng.normal(z, sigz, n)

    # Outliers produce a background of spurious values
    # intersecting with the true distribution
    #
    nout = int(ntot*frac)  # frac outliers
    xbad = rng.uniform(min(x), max(x), nout)
    ybad = rng.uniform(min(y), max(y), nout)
    zbad = np.mean(z) + rng.uniform(0, np.ptp(z), nout)

    # Combines the good values and the outliers in one vector
    #
    x = np.append(x, xbad)
    y = np.append(y, ybad)
    z = np.append(z, zbad)

    sigx = np.full_like(x, sigx)  # Adopted error in x
    sigy = np.full_like(x, sigy)  # Adopted error in y
    sigz = np.full_like(x, sigz)  # Adopted error in z

    plt.clf()
    data = np.column_stack([x, y])
    sigdata = np.column_stack([sigx, sigy])
    pivot = np.round(np.median(data, 0))
    p = ltsfit(data, z, sigdata, sigz, pivot=pivot)
    plt.pause(1)

    # Illustrates how to obtain the best-fitting values from the class
    print(f"The best fitting parameters are: {p.coef}\n")

#------------------------------------------------------------------------------

def lts_hyperfit_example():
    """
    Usage example for ltsfit() fitting a hyperplane in 4-dim.
    In this example I assume that 10% of the values are strong outliers.

    """
    print('-'*70 + "\nExample fitting a hyperplane in 4-dim\n" + '-'*70 + '\n')

    ntot = 300  # Total number of values
    frac = 0.1  # fraction of outliers

    # Coefficients of the test hyperplane
    a = 10.
    b = 1.
    c = 2.
    d = 3.

    n = int(ntot*(1 - frac))  # (1 - frac) good values
    rng = np.random.default_rng(235)
    x1 = rng.uniform(17.5, 22.5, n)
    x2 = rng.uniform(7.5, 12.5, n)
    x3 = rng.uniform(5, 9, n)
    z = a + b*x1 + c*x2 + d*x3

    sig_int = 1  # Intrinsic scatter in z
    z = rng.normal(z, sig_int, n)

    sigx1 = 0.2     # Observational error in x1
    sigx2 = 0.4     # Observational error in x2
    sigx3 = 0.4     # Observational error in x3
    sigz = 0.25     # Observational error in z
    x1 = rng.normal(x1, sigx1, n)
    x2 = rng.normal(x2, sigx2, n)
    x3 = rng.normal(x3, sigx3, n)
    z = rng.normal(z, sigz, n)

    # Outliers produce a background of spurious values
    # intersecting with the true distribution
    #
    nout = int(ntot*frac)  # frac outliers
    x1bad = rng.uniform(np.min(x1), np.max(x1), nout)
    x2bad = rng.uniform(np.min(x2), np.max(x2), nout)
    x3bad = rng.uniform(np.min(x3), np.max(x3), nout)
    zbad = np.mean(z) + rng.uniform(0, np.ptp(z), nout)

    # Combines the good values and the outliers in one vector
    #
    x1 = np.append(x1, x1bad)
    x2 = np.append(x2, x2bad)
    x3 = np.append(x3, x3bad)
    z = np.append(z, zbad)

    sigx1 = np.full_like(z, sigx1)  # Adopted error in x1
    sigx2 = np.full_like(z, sigx2)  # Adopted error in x2
    sigx3 = np.full_like(z, sigx3)  # Adopted error in x3
    sigz = np.full_like(z, sigz)    # Adopted error in z

    plt.clf()
    data = np.column_stack([x1, x2, x3])
    sigdata = np.column_stack([sigx1, sigx2, sigx3])
    pivot = np.round(np.median(data, 0))
    p = ltsfit(data, z, sigdata, sigz, pivot=pivot)
    plt.pause(1)

    # Illustrates how to obtain the best-fitting values from the class
    print(f"The best fitting parameters are: {p.coef}\n")

#------------------------------------------------------------------------------


if __name__ == '__main__':

    lts_linefit_example()
    lts_planefit_example()
    lts_hyperfit_example()
