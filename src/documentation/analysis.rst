.. _analysis:

************************************
Particle smoother
************************************

Documentation of the code in :file:`analysis`. The scripts in this folder build
the core of the project. For a description of how the particle smoother
(in our implementation) works, we refer you to the research paper of this project.

.. _analysis_prepare:

Prepare the data for analysis
======================================

These scripts rearrange the data generated in :ref:`data_management` to make
them more accessible for analysis, and store the results in the pickle-format.

.. automodule:: src.analysis.prepare_data
    :members:

---------------------------------------

.. automodule:: src.analysis.extract_true_factors
    :members:

.. _analysis_priors:

Draw the prior and the transition errors
========================================

.. automodule:: src.analysis.initial_draws
    :members:

Main classes for the particle smoother
=======================================

In these classes lies the main logic of the particle smoother. The methods are
bundled to classes so that the parameters for the measurement / transition equations
are stored in one central place and can easily be accessed. Additionally, the
measurement class stores all the data relevant for estimation.

Note: in :ref:`particle_smoother`, three measurement objects are
instantiated (one for each factor), while only one transition object is created.

.. automodule:: src.analysis.measurement
    :members:

-------------------------------

.. automodule:: src.analysis.transition
    :members:
    
.. _particle_smoother:

Main loop of the particle smoother
====================================

The main loop consists of a forward iteration over the periods (this is identical to the
particle *filter*), where the generated particles are weighted using the
measurements of each period, and a *backward* iteration (such that all measurements
are used for estimating the underlying state of *every* period). For the resampling
step during the forward iteration, the multinomial-module in *numpy.random*
is used. The estimation result of *particle_smoother* is stored as a pickle
of a pandas DataFrame.

.. automodule:: src.analysis.particle_smoother
    :members: