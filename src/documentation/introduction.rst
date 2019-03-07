.. _introduction:


******************
Introduction [#]_
******************

.. [#] Documentation on how we built this documentation and the rest of the project (using Waf) is at http://hmgaudecker.github.io/econ-project-templates/.


.. _getting_started:

Getting started
===============

Welcome to the documentation of our final project for the course Effective Programming
Practices for Economists (WS 18/19, University of Bonn). In this project, we
apply a variant of the particle smoother to estimate the unobserved factors
of a dynamic factor model. The model is a simplified version of the skills
model in :cite:`cunha2010`. Since the data is simulated, we can evaluate the
performance of the estimation in the end.

The steps of the project are:

1. Data generation and management
2. Application of the particle smoother
3. Description of estimation results
4. Bundle results in a research paper

.. _project_structure:

Structure of the project
========================
Our source code (all in the folder :file:`src/`) is distributed across folders that follow the main steps listed
above. :file:`data_management` contains the do-files that generate the simulated
data (see :ref:`data_management`). :file:`analysis` contains the Python
scripts we wrote to apply the particle smoother to this data (see :ref:`analysis`).
In :file:`final` there are scripts that summarize the estimation results (:ref:`final`),
and :file:`paper` contains the latex-file (and a script that dynamically creates content
for it) for the research paper (:ref:`paper`).

.. _parameter_files:

Parameter files
===============

The model, the generated data and the estimation procedure all can be changed
by changing parameters in the according files in :file:`src/model_specs`.

The most general parameters are found in the file :file:`smoother.json`

.. literalinclude:: ../model_specs/smoother.json

The random seed gives reproducible results of all the randomization that takes place
during the data generation and estimation. The number of particles is an important
parameter of the particle smoother (naturally, the more, the better). It *must be*
the *product* of the next to parameters, *draws_constant* and *draws_varying*,
which denote the number of draws for the constant and the non-constant
factors, respectively (they are concatenated to particles via the Cartesian product).
The number of periods describes the "deepness" of one dynamic chain, while all
measurements belonging to one chain are *one* "observation" (this would be a
"case" in the terminology in :cite:`cunha2010`).

The parameters in the files :file:`measurements.json` and :file:`transitions.json`
describe the measurement and transition equations of the model. The notation follows
:cite:`chs_rep`, so we refer to them or the research paper in this project.

:file:`true_prior.json` contains the variances of the normal distribution the
factors (underlying the simulated data) are drawn from.

In general, the particle smoother will run with the *true* parameters and the
true prior (i.e. the first particles are drawn from the same distribution that the
true factors are drawn from). Therefore, the formerly mentioned parameters are
accessed both in :ref:`data_management` and in :ref:`analysis`.

.. _prior_specs:

Two "prior" specifications
===========================

For a Bayesian estimation technique like the particle smoother, the quality of
the prior usually plays an important role for the estimation. This should be true especially
if the length of the chain is as short as in our setting (8 periods). To find out about the
sensitivity of our estimation technique to the prior in this setting, we run
the estimation twice: once with the true, but "random" prior, and once with
a "degenerate" prior, where the first particles are not randomly drawn, but instead
are all fixed to the same, true factor-combination in period 1. For more information
on the implementation of this, see the section :ref:`analysis_priors`.
