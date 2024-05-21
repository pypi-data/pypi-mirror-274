The LtsFit Package
==================

**Robust Least Squares Regression with Uncertainties and Scatter in Any Dimension**

.. image:: https://img.shields.io/pypi/v/ltsfit.svg
    :target: https://pypi.org/project/ltsfit/
.. image:: https://img.shields.io/badge/arXiv-1208.3522-orange.svg
    :target: https://arxiv.org/abs/1208.3522
.. image:: https://img.shields.io/badge/DOI-10.1093/mnras/stt562-green.svg
    :target: https://doi.org/10.1093/mnras/stt562

LtsFit is a Python package for **very robust** hyperplane fitting in N dimensions,
with uncertainties in all coordinates and intrinsic scatter. It implements the
method described in Section 3.2 of
`Cappellari et al. (2013a) <https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C>`_
and uses the Least Trimmed Squares (LTS) technique to iteratively clip outliers
`(Rousseeuw & van Driessen 2006) <http://doi.org/10.1007/s10618-005-0024-4>`_.

.. contents:: :depth: 2

Attribution
-----------

Please also cite `Cappellari et al. (2013a) <https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C>`_
if you use this software for your research. This is the paper where the
implementation was described. The BibTeX entry for the paper is::

    @ARTICLE{Cappellari2013a,
        author = {{Cappellari}, M. and {Scott}, N. and {Alatalo}, K. and
            {Blitz}, L. and {Bois}, M. and {Bournaud}, F. and {Bureau}, M. and
            {Crocker}, A.~F. and {Davies}, R.~L. and {Davis}, T.~A. and {de Zeeuw},
            P.~T. and {Duc}, P.-A. and {Emsellem}, E. and {Khochfar}, S. and
            {Krajnovi{\'c}}, D. and {Kuntschner}, H. and {McDermid}, R.~M. and
            {Morganti}, R. and {Naab}, T. and {Oosterloo}, T. and {Sarzi}, M. and
            {Serra}, P. and {Weijmans}, A.-M. and {Young}, L.~M.},
        title = "{The ATLAS$^{3D}$ project - XV. Benchmark for early-type
            galaxies scaling relations from 260 dynamical models: mass-to-light
            ratio, dark matter, Fundamental Plane and Mass Plane}",
        journal = {MNRAS},
        eprint = {1208.3522},
        year = 2013,
        volume = 432,
        pages = {1709-1741},
        doi = {10.1093/mnras/stt562}
    }

Installation
------------

install with::

    pip install ltsfit

Without writing access to the global ``site-packages`` directory, use::

    pip install --user ltsfit

To upgrade the package to the latest version use::

    pip install --upgrade ltsfit

Documentation
-------------

See ``ltsfit/examples`` and the files docstrings.
They are copied by ``pip`` within the global folder
`site-packages <https://stackoverflow.com/a/46071447>`_.

###########################################################################
