url-summary
===========

.. image:: https://img.shields.io/pypi/v/url-summary.svg
   :target: https://pypi.python.org/pypi/url-summary
   :alt: PyPI Version

.. image:: https://img.shields.io/travis/TeamHG-Memex/url-summary/master.svg
   :target: http://travis-ci.org/TeamHG-Memex/url-summary
   :alt: Build Status

.. image:: http://codecov.io/github/TeamHG-Memex/url-summary/coverage.svg?branch=master
   :target: http://codecov.io/github/TeamHG-Memex/url-summary?branch=master
   :alt: Code Coverage

Show summary of a large number of URLs in a Jupyter Notebook: analyze domains, paths, query keys and values.
This is useful if you want to have a quick glance at URLs obtained by crawling.

.. image:: https://raw.githubusercontent.com/TeamHG-Memex/url-summary/master/url-summary-example.png
   :alt: url-summary example

Installation
------------

Install from PyPI::

    pip install url-summary


Usage
-----

::

    import url_summary

    url_summary.get_summary(urls)

Will show as a summary for a given list (or iterable) of urls.
``top_items`` (20 by default) controls how many top-level items to show,
and ``top_urls`` (3 by default) sets the number of random urls to show
for each top-level item.

Returned object ``url_summary.UrlSummaryResult``
is a list subclass with a nice Jupyter Notebook display.


License
-------

License is MIT.


