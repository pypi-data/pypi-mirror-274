"""
Michele Cappellari, 7 July 2023

"""
import numpy as np
from .ltsfit import ltsfit

class lts_planefit(ltsfit):
    """
    This is a wrapper for existing code that uses the lts_planefit procedure.
    For new code, one should call ltsfit directly.

    """
    def __init__(self, x0, y0, z, sigx, sigy, sigz, clip=2.6, corr=False,
                 epsz=True, frac=None, label='Fitted', label_clip='Clipped',
                 pivotx=0, pivoty=0, plot=True, text=True):

        x0 = np.column_stack([x0, y0])
        sigx = np.column_stack([sigx, sigy])
        pivot = np.hstack([pivotx, pivoty])

        super().__init__(x0, z, sigx, sigz, clip=clip, corr=corr, epsy=epsz,
                         frac=frac, label=label, label_clip=label_clip,
                         pivot=pivot, plot=plot, text=text)
        print("\nWarning: the definition of the x-y axes in the plot has changed in JUL/2023\n")

        self.abc     = self.coef
        self.abc_err = self.coef_err
