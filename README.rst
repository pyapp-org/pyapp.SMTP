############
pyApp - SMTP
############

*Let us handle the boring stuff!*

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: http://github.com/ambv/black
   :alt: Once you go Black...

.. image:: https://api.codeclimate.com/v1/badges/e25e476cd1cd598e89f4/maintainability
   :target: https://codeclimate.com/github/pyapp-org/pyapp.SMTP/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/e25e476cd1cd598e89f4/test_coverage
   :target: https://codeclimate.com/github/pyapp-org/pyapp.SMTP/test_coverage
   :alt: Test Coverage

This extension provides an `SMTP` client object configured via pyApp settings.


Installation
============

Install using *pip*::

    pip install pyApp-SMTP

Install using *pipenv*::

    pip install pyApp-SMTP


Add the `SMTP` block into your runtime settings file::

    SMTP = {
        "default": {
            "host": "localhost",
        }
    }


.. note::

    In addition to the *host* any argument that can be provided to `smtplib.SMTP` can be
    provided.


Usage
=====

The following example creates an SMTP client instance::

    from pyapp_ext.smtp import get_client

    smtp = get_client()


API
===

`pyapp_ext.smtp.get_client() -> SMTP`

    Get named `SMTP` instance.

