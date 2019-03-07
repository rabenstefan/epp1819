.. _introduction:


******************
Introduction [#]_
******************

.. [#] Documentation on Waf, and more background is at http://hmgaudecker.github.io/econ-project-templates/.


.. _getting_started:

Getting started
===============

In this project, we want to evaluate the runtime of a function over increasing input-size.
Specifically, the function is the update-step of the unscented Kalman filter that we programmed.
To test the runtime, we take household-data that was used in :cite:`chs2010`.
To illustrate the result, we provide a scatterplot with a regression curve, and we create a paper and a presentation.

The steps of the project are:

1. Data management
2. Runtime-analysis
3. Visualisation in a plot
4. Research paper and presentation


.. _project_paths:

Project paths
=============

This part shows how we structure our project in the file system.

.. literalinclude:: ../../wscript
    :start-after: out = "bld"
    :end-before:     # Convert the directories into Waf nodes

The paths follow the steps of the analysis in the :file:`src` directory:

    1. **data_management** → **OUT_DATA**
    2. **analysis** → **OUT_ANALYSIS**
    3. **final** → **OUT_FIGURES**

We can access these paths in our Python code by adding a line::

    from bld.project_paths import XXX

at the top of the scripts.

We put the function we want to time (*fast_batch_update*) in the part :ref:`model_code`, 
since it is part of the (unscented) Kalman filter which could be described as a model for an 
underlying data generating process.
