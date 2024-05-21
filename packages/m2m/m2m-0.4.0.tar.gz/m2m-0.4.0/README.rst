===========
M2M Daemons
===========

Copyright (c) 2022-2024 Jérémie DECOCK (www.jdhp.org)

* Web site: https://gitlab.com/jdhp/sensors-m2m-daemons
* Online documentation: https://jdhp.gitlab.io/m2m
* Examples: https://jdhp.gitlab.io/m2m/gallery/
* Source code: https://gitlab.com/jdhp/sensors-m2m-daemons
* Issue tracker: https://gitlab.com/jdhp/sensors-m2m-daemons/issues
* M2M Daemons on PyPI: https://pypi.org/project/m2m


Description
===========

M2M Daemons

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

C.f. requirements.txt


.. _install:

Installation (development environment)
======================================

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the M2M Daemons source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Windows
-------

From the M2M Daemons source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Installation (production environment)
=====================================

::

    python3 -m pip install m2m


Documentation
=============

* Online documentation: https://jdhp.gitlab.io/m2m
* API documentation: https://jdhp.gitlab.io/m2m/api.html


Example usage
=============

::

    mqtt2influx --dry --verbose --config-path examples/config.yml


Build and run the Python Docker image
=====================================

Build the docker image
----------------------

From the M2M Daemons source code::

    docker build -t m2m:latest .

Run unit tests from the docker container
----------------------------------------

From the M2M Daemons source code::

    docker run m2m pytest

Run an example from the docker container
----------------------------------------

From the M2M Daemons source code::

    docker run m2m mqtt2influx

Bug reports
===========

To search for bugs or report them, please use the M2M Daemons Bug Tracker at:

    https://gitlab.com/jdhp/sensors-m2m-daemons/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe
