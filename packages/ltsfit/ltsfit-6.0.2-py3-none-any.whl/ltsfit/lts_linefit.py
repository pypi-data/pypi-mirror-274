"""
Michele Cappellari, 7 July 2023

"""
from .ltsfit import ltsfit

class lts_linefit(ltsfit):
    """
    This is a wrapper for existing code that uses the lts_linefit procedure.
    For new code, one should call ltsfit directly.

    """
    def __init__(self, x0, y, sigx, sigy, clip=2.6, epsy=True, label='Fitted',
                 label_clip='Clipped', frac=None, pivot=0, plot=True,
                 text=True, corr=True):

        super().__init__(x0, y, sigx, sigy, clip=clip, corr=corr, epsy=epsy,
                         frac=frac, label=label, label_clip=label_clip, pivot=pivot,
                         plot=plot, text=text)

        self.ab     = self.coef
        self.ab_err = self.coef_err

