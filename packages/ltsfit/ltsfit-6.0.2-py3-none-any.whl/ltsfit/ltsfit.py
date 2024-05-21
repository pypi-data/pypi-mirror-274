# ###############################################################################
#
# Copyright (C) 2012-2023, Michele Cappellari
# E-mail: michele.cappellari_at_physics.ox.ac.uk
#
# Updated versions of the software are available from my web page
# http://purl.org/cappellari/software
#
# If you have found this software useful for your research, I would
# appreciate an acknowledgement: "We used the LtsFit package described 
# in Cappellari et al. (2013, MNRAS, 432, 1709). This tool combines the 
# Least Trimmed Squares robust technique of Rousseeuw & van Driessen (2006) 
# into a least-squares fitting algorithm which can account for errors in 
# all variables, intrinsic scatter, and automatic outlier detection."
#
# This software is provided as is without any warranty whatsoever.
# Permission to use, for non-commercial purposes is granted.
# Permission to modify for personal or internal use is granted,
# provided this copyright and disclaimer are included unchanged
# at the beginning of the file. All other rights are reserved.
# In particular, redistribution of the code is not allowed.
#
###############################################################################
#
# MODIFICATION HISTORY:
#       V1.0.0: Michele Cappellari, Oxford, 21 March 2011
#       V2.0.0: Converted from lts_linefit. MC, Oxford, 06 April 2011
#       V2.0.1: Added PIVOT keyword, MC, Oxford, 1 August 2011
#       V2.0.2: Fixed program stop affecting earlier IDL versions.
#           Thanks to Xue-Guang Zhang for reporting the problem
#           and the solution. MC, Turku, 10 July 2013
#       V2.0.3: Scale line spacing with character size in text output.
#           MC, Oxford, 19 September 2013
#       V2.0.4: Check that all input vectors have the same size.
#           MC, Baltimore, 8 June 2014
#       V2.0.5: Text plotting changes. MC, Oxford, 26 June 2014
#       V3.0.0: Converted from IDL into Python. MC, Oxford, 5 November 2014
#       V3.0.1: Updated documentation. MC, Baltimore, 9 June 2015
#       V3.0.2: Fixed potential program stop without outliers.
#           Thanks to Masato Onodera for a clear report of the problem.
#         - Output boolean mask instead of good/bad indices.
#         - Removed lts_linefit_example from this file.
#           MC, Oxford, 6 July 2015
#       V3.0.3: Fixed potential program stop without outliers.
#           MC, Oxford, 1 October 2015
#       V3.0.4: Fixed potential program stop without outliers in Matplotlib 1.5.
#           MC, Oxford, 9 December 2015
#       V3.0.5: Use LimeGreen for outliers. MC, Oxford, 8 January 2016
#       V3.0.6: Check for non finite values in input.
#           MC, Oxford, 23 January 2016
#       V3.0.7: Added capsize=0 in plt.errorbar to prevent error bar caps
#           from showing up in PDF. MC, Oxford, 4 July 2016
#       V3.0.8: Fixed: store ab errors in p.ab_err as documented.
#           Thanks to Alison Crocker for the correction.
#           MC, Oxford, 5 September 2016
#       V3.0.9: Fixed typo causing full C-step to be skipped.
#           Thanks to Francesco D'Eugenio for reporting this problem.
#           Increased upper limit of intrinsic scatter accounting for
#           uncertainty of standard deviation with small samples.
#           Michele Cappellari, Oxford, 26 July 2017
#       V3.0.10: Fixed FutureWarning in Numpy 1.14. MC, Oxford, 13 April 2018
#       V3.0.11: Dropped Python 2.7 support. MC, Oxford, 12 May 2018
#       V3.0.12: Fixed clock DeprecationWarning in Python 3.7.
#           MC, Oxford, 27 September 2018
#       V3.0.13: Properly print significant trailing zeros in results.
#           Formatted documentation as dosctring. Included p.rms output.
#           MC, Oxford, 17 February 2020
#       V3.0.14: Fixed incorrect plot ranges due to a Matplotlib change.
#           Thanks to Davide Bevacqua (unibo.it) for the report.
#           MC, Oxford, 22 January 2021
#       Vx.x.x: Additional changes are documented in the CHANGELOG of the LtsFit package.
#
#------------------------------------------------------------------------------

from time import perf_counter as clock
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, stats

#----------------------------------------------------------------------------

def _display_errors(par, sig_par, epsy):
    """ Print parameters rounded according to their uncertainties """

    digits = np.zeros_like(par)
    w = (sig_par != 0) & (par != 0)
    digits[w] = np.ceil(np.log10(np.abs(par[w]))) - np.floor(np.log10(sig_par[w])) + 1
    digits = digits.clip(0)  # negative number of digits aren't allowed
    dg = list(map(str, digits.astype(int)))

    txt = ['a = '] + [f'b_{j} = ' for j in range(len(par) - 2)]

    txt1 = txt + ['scatter = ']
    str_txt = ''
    for t, d, p, s in zip(txt1, dg, par, sig_par):
        str_txt += f"\n{t:>12} {p:#.{d}g} +/- {s:#.2g}"

    if epsy:
        txt += ['\\varepsilon_y=']
    str_tex = ''
    for t, d, p, s in zip(txt, dg, par, sig_par):
        str_tex += f"${t} {p:#.{d}g} \\pm {s:#.2g}$\n"

    return str_tex, str_txt

#----------------------------------------------------------------------------

def _hyperfit(x, y, sigy=None):
    """
    Fit a hyperplane yfit = a + b1*x1 + b2*x2 + ...
    to a set of points (x1, x2,... , y)
    by minimizing chi2 = np.sum(((y - yfit)/sigy)**2)

    """
    if sigy is None:
        coef = np.linalg.lstsq(x, y, rcond=None)[0]
    else:
        coef = np.linalg.lstsq(x/sigy[:, None], y/sigy, rcond=None)[0]

    return coef   # [a, b1, b2,...]

#------------------------------------------------------------------------------

def _residuals(coef, x, y, sigx, sigy):
    """ See equation (7) of Cappellari et al. (2013, MNRAS, 432, 1709) """

    return (x @ coef - y)/np.sqrt(sigx**2 @ coef[1:]**2 + sigy**2)

#----------------------------------------------------------------------------

def _fitting(x, y, sigx, sigy, coef):

    coef, pcov, infodict, errmsg, success = optimize.leastsq(
        _residuals, coef, args=(x, y, sigx, sigy), full_output=True)

    if pcov is None or np.any(np.diag(pcov) < 0):
        sig_coef = np.full(x.shape[1], np.inf)
        chi2 = np.inf
    else:
        chi2 = np.sum(infodict['fvec']**2)
        sig_coef = np.sqrt(np.diag(pcov))  # ignore covariance

    return coef, sig_coef, chi2

#----------------------------------------------------------------------------

def _fast_algorithm(x, y, sigx, sigy, h):

    # Robust least trimmed squares regression.
    # Pg. 38 of Rousseeuw & van Driessen (2006)
    # http://dx.doi.org/10.1007/s10618-005-0024-4
    #
    m = 500 # Number of random starting points
    ndim = x.shape[1]
    coefv = np.empty((m, ndim))
    chi2v = np.empty(m)
    for j in range(m):  # Draw m random starting points
        w = np.random.choice(y.size, ndim, replace=False)
        coef = _hyperfit(x[w], y[w])  # Find a plane going through three random points
        for k in range(3):  # Run C-steps up to H_3
            res = _residuals(coef, x, y, sigx, sigy)
            good = np.argsort(np.abs(res))[:h]  # Fit the h points with the smallest errors
            coef, sig_coef, chi_sq = _fitting(x[good], y[good], sigx[good], sigy[good], coef)
        coefv[j, :] = coef
        chi2v[j] = chi_sq

    # Perform full C-steps only for the 10 best results
    #
    w = np.argsort(chi2v)
    nbest = 10
    chi_sq = np.inf
    for j in range(nbest):
        coef1 = coefv[w[j], :]
        while True:  # Run C-steps to convergence
            coefOld = coef1
            res = _residuals(coef1, x, y, sigx, sigy)
            good1 = np.argsort(np.abs(res))[:h]  # Fit the h points with the smallest errors
            coef1, sig_ab1, chi1_sq = _fitting(x[good1], y[good1], sigx[good1], sigy[good1], coef1)
            if np.allclose(coefOld, coef1):
                break
        if chi_sq > chi1_sq:
            coef = coef1  # Save best solution
            good = good1
            chi_sq = chi1_sq

    mask = np.zeros_like(y, dtype=bool)
    mask[good] = True

    return coef, mask

#------------------------------------------------------------------------------

class ltsfit:
    """
    ltsfit
    ======

    Purpose
    -------

    Fit a linear function of the form::

        y = a + b1*x1 + b2*x2 +...+ bm*xm,

    to data with errors in all coordinates and intrinsic scatter, using a robust
    method that clips outliers. The function can handle lines in 2-dim, planes in
    3-dim, or hyperplanes in N-dim, where ``x1, x2,..., xm`` are the independent
    variables and ``y`` is the dependent variable. The method was introduced in
    Sec. 3.2 of `Cappellari et al. (2013a) <https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C>`_
    and the treatment of outliers is is based on the FAST-LTS technique by
    `Rousseeuw & van Driessen (2006) <http://doi.org/10.1007/s10618-005-0024-4>`_.
    See also `Rousseeuw (1987) <http://books.google.co.uk/books?id=woaH_73s-MwC&pg=PA15>`_.
    
    Calling Sequence
    ----------------

    .. code-block:: python

        from ltsfit.ltsfit import ltsfit

        p = ltsfit(x, y, sigx, sigy, clip=2.6, corr=True, epsy=True,
                   frac=None, label='Fitted', label_clip='Clipped',
                   legend=True, pivot=None, plot=True, text=True)

        print(f"Best fitting parameters: {p.coeff}")

    The output values are stored as attributes of the ``p`` object.

    Input Parameters
    ----------------

    x: array_like with shape (n, m)
        Array with ``n`` values of the independent variables in ``m`` dimensions.

        EXAMPLE: To fit a line in 2-dim, one has a single vector ``x`` of
        length ``n`` with the independent variable and a corresponding vector of
        dependent variable ``y``.

        EXAMPLE: To fit a plane in 3-dim, one has two vectors of length ``n`` of
        independent variables ``(x1, x2)``. In this case,
        ``x = np.column_stack([x1, x2])``.

        EXAMPLE: To fit a hyperplane in 4-dim, one has three vectors of
        independent variables ``(x1, x2, x3)``. In this case,
        ``x = np.column_stack([x1, x2, x3])``.
    y: array_like with shape (n,)
        Vector of measured values for each set of ``x`` variables.
    sigx: array_like with shape (n, m)
        Array of ``1sigma`` uncertainties for each ``x`` coordinate for ``m``
        dimensions. This has the same shape as ``x``.
    sigy: array_like with shape (n,)
        Vector of ``1sigma`` uncertainties for each ``y`` value.

    Optional Keywords
    -----------------

    clip: float
        The number of standard deviations from the best fit to use as a cutoff
        for outliers. Data points that deviate more than ``clip*sigma`` from the
        best fit are excluded from the fit. The default value is ``clip=2.6``,
        which corresponds to a 99% confidence interval for a normal distribution.

        If the data has many measurements and few outliers, it may be beneficial
        to increase the clipping value, to avoid discarding valid data points.
        A reasonable choice of clipping value could be one that would eliminate
        on average one data point from a normal distribution. This can be
        calculated as::

            from scipy.stats import norm

            prob = 1/x.size
            clip = abs(norm.ppf(prob/2))

        For example, this gives ``clip=2.58`` for ``x.size=100``, ``clip=3.29``
        for ``x.size=1000`` and ``clip=3.89`` for ``x.size=10000``.
    corr: bool
        if ``True``, the correlation coefficients are printed on the plot.
        Default is ``True``.
    epsy: bool
        If ``True``, the intrinsic scatter is printed on the output plot.
        Default is ``True``.
    frac: float
        Fraction of values to include in the LTS stage.
        Up to a fraction ``frac`` of the values can be outliers.
        One must have ``0.5 <= frac <= 1``. Default is ``0.5``.

        NOTE: Set ``frac=1`` to turn off outlier detection.
    pivot: array_like with shape (m,)
        If nonzero, then ``ltsfit`` fits the following line, plane or hyperplane::

            y = a + b0*(x0 - pivot[0]) + b1*(x1 - pivot[1]) + ...

        ``pivot`` are called ``x_0``, ``y_0`` in eq.(7) of `Cappellari et al. (2013a)`_.
        Use of this keyword is strongly recommended, and suggested values are
        ``pivot = np.median(x, 0)``. This keyword has no effect on the best fit
        but is important to reduce the covariance and uncertainty in the
        intercept ``a``.  However, the covariance is weakly dependent on the
        precise value of the ``pivot``. For this reason, it is generally better
        to round the ``pivot`` values to nice numbers. Default is ``0``.
    plot: bool
        If ``True``, a plot of the fit is produced. Default is ``True``.
    text: bool
        If ``True``, the best fitting parameters are printed on the plot.
        Default is ``True``.

    Output Parameters
    -----------------

    The output values are stored as attributes of the ``ltsfit`` class.

    .coef: array_like with shape (m+1,)
        Best fitting parameters ``[a, b1, b2,..., bm]``.
    .coef_err: array_like with shape (m+1,)
        ``1*sigma`` formal uncertainties ``[a_err, b1_err, b2_err,..., bm_err]``.
    .mask: array_like with shape (n,) and dtype bool
        Boolean vector indicating which elements of ``z`` were included in
        the fit (``True``) and which were clipped as outliers (``False``).
    .rms: float
        RMS deviation between the data and the fitted relation.
    .sig_int: float
        Intrinsic scatter in the ``y`` direction around the line/plane/hyperplane.
        ``sig_int`` is called ``epsilon_y`` in eq.(6) of `Cappellari et al. (2013a)`_.
    .sig_int_err: float
        ``1*sigma`` formal error on ``sig_int``.
    .xx: array_like with shape (n,)
        Values plotted along the x-axis. This is the linear combination of the
        ``x`` variables that represents the plane/hyperplane edge-on::

            xx = a + b1*(x1 - pivot[0]) + b2*(x2 - pivot[1]) + ...

        For line fitting, these are just the ``x`` values.
    .yy: array_like with shape (n,)
        The input ``y`` values plotted along the y-axis.
    .xerr: array_like with shape (n,)
        ``1*sigma`` uncertainties for ``p.xx`` in the x-axis of the plot.
    .yerr: array_like with shape (n,)
        ``1*sigma`` uncertainties for ``p.yy`` in the y-axis of the plot.
    .xline: array_like with shape (2,)
        ``x`` coordinates of the best fitting relation as shown on the plot.
    .yline: array_like with shape (2,)
        ``y`` coordinates of the best fitting relation as shown on the plot.
    .spearmanr: array_like with shape (2,)
        Spearman ``r`` coefficient and probability ``p`` between ``(p.xx, p.yy)``
        without clipping outliers.
    .pearsonr: array_like with shape (2,)
        Pearson ``r`` coefficient and probability ``p`` between ``(p.xx, p.yy)``
        without clipping outliers.

    ###########################################################################

    """
    def __init__(self, x0, y, sigx, sigy, clip=2.6, corr=True, epsy=True,
                 frac=None, label='Fitted', label_clip='Clipped', legend=True,
                 pivot=None, plot=True, text=True):

        if x0.ndim == 1:
            x0, sigx = x0[:, None], sigx[:, None]

        n, ndim = x0.shape
        assert x0.shape == sigx.shape, 'x and sigx must have the same shape'
        assert n == y.size == sigy.size, 'y, sigy must have length x.shape[0]'
        assert np.all(np.isfinite(np.column_stack([x0, y, sigx, sigy]))), \
            'Input contains non finite values'

        if pivot is None:
            print('WARNING: Using a nonzero `pivot` keyword is always reccomended')
            pivot = np.zeros(ndim)
        else:
            pivot = np.atleast_1d(pivot)

        t = clock()

        p = ndim + 1  # space dimension
        n = y.size
        h = int((n + p + 1)/2) if frac is None else int(max(round(frac*n), (n + p + 1)/2))

        x = np.column_stack([np.ones_like(y), x0 - pivot])
        self._single_fit(x, y, sigx, sigy, h, clip)
        self.rms = np.std(x[self.mask] @ self.coef - y[self.mask], ddof=p)

        par = np.append(self.coef, self.sig_int)
        sig_par = np.append(self.coef_err, self.sig_int_err)
        str_tex, str_txt = _display_errors(par, sig_par, epsy)
        ylabel0 = 'a + ' + ' + '.join([f'(x_{j} - p_{j}) b_{j}' for j in range(ndim)])

        if p == 2:
            xx = x0.ravel()
            xerr = sigx.ravel()
            xlabel = '$x_0$'
            ylabel = '$y,\quad y_{\\rm fit} = a + (x_0 - p_{0}) b_0$'
        else:
            xx = x @ par[:-1]
            xerr = np.sqrt(sigx**2 @ par[1:-1]**2)
            xlabel = '$' + ylabel0 + '$'
            ylabel = 'y'

        self.spearmanr = stats.spearmanr(xx, y)
        self.pearsonr = stats.pearsonr(xx, y)
        self.xx = xx
        self.yy = y
        self.xerr = xerr
        self.yerr = sigy

        print('\n################# Values and formal errors ################')
        print(str_txt)
        print(f'Observed rms scatter: {self.rms:#.3g}')
        print('y = ' + ylabel0)
        for j, piv in enumerate(pivot):
            print(f'   p_{j} = {pivot[j]:#.4g}')
        print(f"Adopted clip = {clip:#.2f}*sigma; "
              f"Fitted/Clipped = {self.mask.sum()}/{(~self.mask).sum()}")
        print('Non-clipped Spearman r = %#.2g and p = %#.2g' % self.spearmanr)
        print('Non-clipped Pearson r = %#.2g and p = %#.2g' % self.pearsonr)
        print(f'Execution time {clock() - t:.2f} s')
        print('\n###########################################################\n')

        if plot:
            plt.errorbar(xx[self.mask], y[self.mask], xerr=xerr[self.mask],
                         yerr=sigy[self.mask], fmt='ob', capthick=0, capsize=0,
                         label=label)
            plt.errorbar(xx[~self.mask], y[~self.mask], xerr=xerr[~self.mask],
                         yerr=sigy[~self.mask], fmt='d', color='LimeGreen',
                         capthick=0, capsize=0, label=label_clip)
            ax = plt.gca()
            xlim = np.array(ax.get_xlim())
            ylim = np.array(ax.get_ylim())
            y1 = par[0] + par[1]*(xlim - pivot) if p == 2 else xlim
            self.xline = xlim
            self.yline = y1

            plt.plot(xlim, y1, '-k', linewidth=2, zorder=1, label='Fit')
            plt.plot(xlim, y1 + self.rms, '--r', lw=2, zorder=1, label="1$\sigma$")
            plt.plot(xlim, y1 - self.rms, '--r', lw=2, zorder=1)
            plt.plot(xlim, y1 + clip*self.rms, ':r', lw=2, zorder=1, label=f"{clip:#.1f}$\sigma$")
            plt.plot(xlim, y1 - clip*self.rms, ':r', lw=2, zorder=1)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.xlim(xlim)
            plt.ylim(ylim)
            ax.minorticks_on()

            if legend:
                plt.legend(loc=4)

            if text:
                str_tex += f'$\Delta={self.rms:#.3g}$\n'
                if np.any(pivot):
                    for j, piv in enumerate(pivot):
                        str_tex += f'$(p_{j}={piv:#.4g})$\n'
                ax.text(0.02, 0.98, str_tex, horizontalalignment='left',
                        verticalalignment='top', transform=ax.transAxes)

            if corr:
                txt = '${\\rm Spearman/Pearson}$\n'
                txt += '$r=%#.2g\, p=%#.2g$\n' % self.spearmanr
                txt += '$r=%#.2g\, p=%#.2g$\n' % self.pearsonr
                ax.text(0.98, 0.98, txt, horizontalalignment='right',
                        verticalalignment='top', transform=ax.transAxes)

# ------------------------------------------------------------------------------
    def _find_outliers(self, sig_int, x, y, sigx, sigy1, h, offs, clip):

        sigy = np.sqrt(sigy1**2 + sig_int**2) # Gaussian intrinsic scatter

        if h == len(x):     # No outliers detection

            coef = _hyperfit(x, y, sigy=sigy)  # quick initial guess
            coef, sig_coef, chi_sq = _fitting(x, y, sigx, sigy, coef)
            mask = np.ones_like(y, dtype=bool)  # No outliers

        else:   # Robust fit and outliers detection

            # Initial estimate using the maximum breakdown
            # of 50% for the method but the lowest efficiency
            #
            coef, mask = _fast_algorithm(x, y, sigx, sigy, h)

            # inside-out outliers removal
            #
            while True:
                res = _residuals(coef, x, y, sigx, sigy)
                sig = np.std(res[mask], ddof=coef.size)
                maskOld = mask
                mask = np.abs(res) <= clip*sig
                coef, sig_coef, chi_sq = _fitting(x[mask], y[mask], sigx[mask], sigy[mask], coef)
                if np.array_equal(mask, maskOld):
                    break

        # To determine 1sigma error on the intrinsic scatter the chi2
        # is decreased by 1sigma=sqrt(2(h-ndim)) while optimizing coef
        #
        h = mask.sum()
        dchi = np.sqrt(2*(h - coef.size)) if offs else 0.

        self.coef = coef
        self.coef_err = sig_coef
        self.mask = mask

        err = (chi_sq + dchi)/(h - coef.size) - 1
        print('sig_int: %10.4f  %10.4f' % (sig_int, err))

        return err

#------------------------------------------------------------------------------

    def _single_fit(self, x, y, sigx, sigy, h, clip):

        if self._find_outliers(0, x, y, sigx, sigy, h, 0, clip) < 0:
            print('No intrinsic scatter or errors overestimated')
            sig_int = 0.
            sig_int_err = 0.
        else:
            sig1 = 0.
            res = x @ self.coef - y  # Total residuals ignoring measurement errors
            std = np.std(res[self.mask], ddof=self.coef.size)
            sig2 = std*(1 + 3/np.sqrt(2*self.mask.sum()))  # Observed scatter + 3sigma error
            print('Computing sig_int')
            sig_int = optimize.brentq(self._find_outliers, sig1, sig2,
                                      args=(x, y, sigx, sigy, h, 0, clip), rtol=1e-3)
            print('Computing sig_int error')    # chi2 can always decrease
            sigMax_int = optimize.brentq(self._find_outliers, sig_int, sig2,
                                         args=(x, y, sigx, sigy, h, 1, clip), rtol=1e-3)
            sig_int_err = sigMax_int - sig_int

        self.sig_int = sig_int
        self.sig_int_err = sig_int_err

        print('Repeating at best fitting solution')
        self._find_outliers(sig_int, x, y, sigx, sigy, h, 0, clip)

#------------------------------------------------------------------------------

