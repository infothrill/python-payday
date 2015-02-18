payday - radically simple invoice generation
============================================
*payday* is a command line tool that can be used to generate high quality
printable invoices using just a couple of YAML files and HTML templates.
Currently, it supports Jinja2 and Webkit based PDF rendering capabilities.

With *payday*, your entire billing history becomes easy to maintain in a source
control system.

Features
--------
* stores client metadata in YAML files
* stores bills in YAML files
* renders custom HTML/PDF bills using combinations of
   * jinja2 (HTML)
   * wkhtmltopdf (PDF)
   * not used currently: phantomjs (PDF, PNG)
   * not used currently: xhtml2pdf (PDF)

Non-functional features
-----------------------
Store your invoices in easy to read and edit lighweight files. Manage your
invoice files wherever and however you like.

* no web gui, no REST
* no cloud
* no database
* no security issues

Filesystem layout:

.. code-block::

   example/                  This is the root which you keep in your SCM
   ├── billing               Right now, this one is hardcoded...
   │   ├── archive           Put old PDFs here for reference
   │   └── templates         Want different layouts for different clients?
   │       └── default
   │           └── assets
   └── clients               All client metadata including invoice data is here
       └── snakeoil
           └── invoices


Problematic features
--------------------
Not sure how to generate multi page layouts via HTML.

Installation
------------

.. code-block:: bash

   sudo apt-get install python-setuptools python-pip python-virtualenv python-dev wkhtmltopdf xvfb
   python setup.py install

Usage examples
--------------
.. code-block:: bash

   payday-client list
   payday-invoice list
   payday-invoice info 201408-01
   payday-invoice render 201408-01 out.pdf example/


An example PDF as rendered using the data stored in the example/ subdirectory
is provided for demonstration.

Notes on PDF rendering engines
------------------------------
I personally got the best results with wkhtmltopdf, since if doesn't rasterize
the output and thus creates a PDF with selectable text while at the same time
producing good quality rendering because it is based on Webkit.

Requirements
------------
* Python 2.7
* wkhtmltopdf
* xvfb (virtual framebuffer) on Linux
* OS X or Linux (Debian based distros have been used)

Support for Python3 is not available at this point due to Jinja2 being
incompatible.

Status
------
This thing is unfinished and was hacked together during a couple of sessions
at the end of each month while I worked as a a freelance.
Since I stopped being a freelance, I am not developing this actively anymore,
however, I will be happy to support it with merge requests and potentially
handing over to an interested adopter.
