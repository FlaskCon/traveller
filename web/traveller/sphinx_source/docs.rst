
.. :tocdepth:: 5

Documentation
=============

Sphinx and the other needed packages are included in **traveller/sphinx_source/docs_requirements.txt**.

To setup Sphinx:

Install the required packages using

.. code:: bash

    $ python -m pip install -r docs_requirements.txt
    
then change directory to the folder containing the source and build files for the documenatation

.. code:: bash

    $ cd traveller/sphinx_source

Run the command below in the traveller/sphinx_source folder to generate HTML pages for the documentation.

.. code:: bash

    $ make html
    
 
You can view the generated HTML pages in **_build/html** folder
