.. src documentation master file, created by
   sphinx-quickstart on Tue May 14 15:21:35 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to spistats' documentation!
===============================

Description
--------
LoRaWAN, a widely deployed LPWAN protocol, raises privacy concerns due to metadata exposure, particularly concerning the exploitation of stable device identifiers. For the first time in literature, we propose two privacy-preserving pseudonym schemes tailored for LoRaWAN: resolvable pseudonyms and sequential pseudonyms. We extensively evaluate their performance and applicability through theoretical analysis and simulations based on a large-scale real-world dataset of 71 million messages. We conclude that sequential pseudonyms are the best solution.

This repository analyses the performances of sequential private identifiers: a LoRaWAN privacy orentied communication protocol.

We use efficient numerical methods to compute the mass function and the CDF of streaks of repeating events.
The expectation of packet loss is computed using Markov chains for improved performances.

Repository
----------
The code is accessible at the followin address :
https://gitlab.inria.fr/jaalmoes/spistats

Installation
------------
These python package is available on pypi, hence you can install it via pip ::

    pip install spistats

Research work 
----------------
This work is based on an extention of the follwoing research paper: 
https://inria.hal.science/hal-04525080
Please cite this paper if you use this package in your research project. ::

    @inproceedings{pelissier:hal-04525080,
      TITLE = {{Privacy-preserving pseudonyms for LoRaWAN}},
      AUTHOR = {Pélissier, Samuel and Aalmoes, Jan and Mishra, Abhishek Kumar and Cunche, Mathieu and Roca, Vincent and Donsez, Didier},
      URL = {https://inria.hal.science/hal-04525080},
      BOOKTITLE = {{WiSec 2024 - 17th ACM Conference on Security and Privacy in Wireless and Mobile Networks}},
      ADDRESS = {Seoul, South Korea},
      ORGANIZATION = {{Association for Computer Machinery (ACM)}},
      PUBLISHER = {{ACM}},
      PAGES = {1-6},
      YEAR = {2024},
      MONTH = May,
      DOI = {10.1145/xxxxxxx.xxxxxxx},
      KEYWORDS = {LoRaWAN ; Pseudonyms ; IoT ; Security \& Privacy ; Sensor networks ; Link-layer protocols ; Privacy Enhancing Technologies},
      PDF = {https://inria.hal.science/hal-04525080v2/file/WiSec2024_round2_LoRaWAN_pseudonyms-27.pdf},
      HAL_ID = {hal-04525080},
      HAL_VERSION = {v2},
    }


Quick start guide
------------------
The figures of the paper
https://inria.hal.science/hal-04525080
on LoRaWAN can be generated using ::

    pythom -m spistats.markov

Full API's documentation
---------------------
.. toctree::
   :maxdepth: 4
   :caption: Contents:

   spistats


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
