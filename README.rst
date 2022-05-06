==================
Sharing Configs API
==================

:Version: 0.1.0
:Source: https://github.com/maykinmedia/sharing-configs-api
:Keywords: ``django``, ``github``
:PythonVersion: 3.9

|build-status| |coverage| |docker| |black| |python-versions|

API to share configurations using GitHub

Developed by `Maykin Media B.V.`_


Introduction
============

The Sharing Configs API provides endpoints to download and upload files and
is designed to be used together with `Sharing Configs`_ library.

Using Sharing Configs API administrators can easily configure backends used
to store the files. They also can fine-tune the access to files using permissions.

The API clients can easily upload and download files and explore the folder
structure via endpoints.

The API backend is extensible, i.e. developers can create plugins to use other
storage backends.

API specification
=================

|lint-oas| |generate-sdks| |generate-postman-collection|

==============  ==============  =============================
Version         Release date    API specification
==============  ==============  =============================
latest          n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/sharing-configs-api/master/src/sharing/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/sharing-configs-api/master/src/sharing/openapi.yaml>`_,
==============  ==============  =============================

Previous versions are supported for 6 month after the next version is released.

See: `All versions and changes <https://github.com/maykinmedia/sharing-configs-api/blob/master/CHANGELOG.rst>`_

Documentation
=============

See ``INSTALL.rst`` for installation instructions, available settings and
commands.

License
=======

Copyright © Maykin Media, 2022

Licensed under the EUPL_.

References
==========

* `Issues <https://github.com/maykinmedia/sharing-configs/issues>`_
* `Code <https://github.com/maykinmedia/sharing-configs-api.git>`_



.. |build-status| image:: https://github.com/maykinmedia/sharing-configs-api/actions/workflows/ci.yml/badge.svg?branch=master
    :alt: Build status
    :target: https://github.com/maykinmedia/sharing-configs-api/actions/workflows/ci.yml?branch=master

.. |coverage| image:: https://codecov.io/github/maykinmedia/sharing-configs-api/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/gh/maykinmedia/sharing-configs-api

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |docker| image:: https://img.shields.io/docker/v/maykinmedia/sharing-configs-api
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/sharing-configs-api

.. |python-versions| image:: https://img.shields.io/badge/python-3.9%2B-blue.svg
    :alt: Supported Python version

.. |lint-oas| image:: https://github.com/maykinmedia/objects-api/workflows/lint-oas/badge.svg
    :alt: Lint OAS
    :target: https://github.com/maykinmedia/sharing-configs-api/actions?query=workflow%3Alint-oas

.. |generate-sdks| image:: https://github.com/maykinmedia/objects-api/workflows/generate-sdks/badge.svg
    :alt: Generate SDKs
    :target: https://github.com/maykinmedia/sharing-configs-api/actions?query=workflow%3Agenerate-sdks

.. |generate-postman-collection| image:: https://github.com/maykinmedia/objects-api/workflows/generate-postman-collection/badge.svg
    :alt: Generate Postman collection
    :target: https://github.com/maykinmedia/sharing-configs-api/actions?query=workflow%3Agenerate-postman-collection


.. _Maykin Media B.V.: https://www.maykinmedia.nl
.. _Sharing Configs: https://github.com/maykinmedia/sharing-configs.git
.. _EUPL: LICENSE.md
