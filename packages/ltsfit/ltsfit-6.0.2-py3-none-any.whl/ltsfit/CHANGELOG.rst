
Changelog
=========

V6.0.1: MC, Oxford, 20 July 2023
  - New function ``ltsfit`` to fit hyperplanes in N-dim. This procedure
    generalizes and replaces both ``lts_linefit`` and ``lts_planefit``, which
    are now deprecated wrappers for ``ltsfit``. This change was suggested and
    motivated by Francesco D'Eugenio (cam.ac.uk), who shared his own 4-dim
    ``lts_hyperfit`` and his paper on a useful application.
  - ``ltsfit``: When fitting planes/hyperplanes, plot the independent variable
    on the y-axis to be consistent with line fitting. Also plot a legend.
  - Updated all ``ltsfit_examples``.
  - Fixed inconsistency between the version number on PyPi and in the Changelog.

V5.0.20: MC, Oxford, 3 October 2022
  - Fixed program stop due to Matplotlib change.
    Thanks to Hitesh Lala (Heidelberg) for the report.
  - Extract documentation from docstrings and show it on PyPi.

V5.0.19: MC, Oxford, 22 January 2021
  - Fixed incorrect plot ranges due to a Matplotlib change.
    Thanks to Davide Bevacqua (unibo.it) for the report.

V5.0.18: MC, Oxford, 17 February 2020
  - Properly print significant trailing zeros in results.

V5.0.17: MC, Oxford, 22 January 2020
  - Formatted documentation as docstring.
  - Included p.rms output.
  - Published on PyPi. Increased major version number by mistake.

V2.0.16: MC, Oxford, 27 September 2018
  - Fixed clock DeprecationWarning in Python 3.7.

V2.0.15: MC, Oxford, 12 May 2018
  - Dropped Python 2.7 support.

V2.0.14: MC, Oxford, 13 April 2018
  - Fixed FutureWarning in Numpy 1.14.

V2.0.13: Michele Cappellari, Oxford, 26 July 2017
  - Increased upper limit of intrinsic scatter accounting for
    uncertainty of standard deviation with small samples.

V2.0.12: MC, Oxford, 5 September 2016
  - Fixed: store ab errors in p.ab_err as documented.
    Thanks to Alison Crocker for the correction.

V2.0.11: MC, Oxford, 4 July 2016
  - Added capsize=0 in plt.errorbar to prevent error bar caps
    from showing up in PDF.

V2.0.10: MC, Oxford, 23 January 2016
  - Check for non finite values in input.

V2.0.9: MC, Oxford, 8 January 2016
  - Use LimeGreen for outliers.

V2.0.8: MC, Oxford, 9 December 2015
  - Fixed potential program stop without outliers in Matplotlib 1.5.
  - Increased maximum intrinsic scatter for brentq, to avoid possible
    stops in extreme situations.

V2.0.7: MC, Oxford, 1 October 2015
  - Fixed potential program stop without outliers.

V2.0.6: MC, Oxford, 5 September 2015
  - Optionally pass a legend label.

V2.0.5: MC, Oxford, 6 July 2015
  - Fixed potential program stop without outliers.
    Thanks to Masato Onodera for a clear report of the problem.
  - Output boolean mask instead of good/bad indices.
  - Removed lts_linefit_example from this file.
  - Print verbose output during calculation.

V2.0.4: MC, Baltimore, 9 June 2015
  - Updated documentation.

V2.0.3: MC, Oxford, 10 December 2014
  - Uses np.std rather than biweight to estimate scatter upper limit.

V2.0.2: MC, 6 November 2014
  - Included _linefit function to avoid np.polyfit bug with weights.

V2.0.1: MC, Oxford, 23 October 2014
  - Fixed program stop with zero scatter.

V2.0.0: MC, Portsmouth, 23 June 2014
  - Converted from IDL into Python.

V1.0.6: MC, Baltimore, 8 June 2014
  - Check that all input vectors have the same size.

V1.0.5: MC, Oxford, 19 September 2013
  - Scale line spacing with character size in text output.

V1.0.4: MC, Turku, 10 July 2013
  - Fixed program stop affecting earlier versions of IDL.
    Thanks to Xue-Guang Zhang for reporting the problem
    and the solution.

V1.0.3: MC, Oxford, 13 March 2013
  - Added CLIP keyword.

V1.0.2: MC, Oxford, 1 August 2011
  - Added PIVOT keyword.

V1.0.1: MC, Oxford, 28 July 2011
  - Included _EXTRA and OVEPLOT, keywords.

V1.0.0: Michele Cappellari, Oxford, 21 March 2011
  - Created and tested.
