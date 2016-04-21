.. image:: http://readthedocs.org/projects/jpkay/badge/?version=latest
   :target: http://jpkay.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status

JPKay
=====

``JPKay`` (pun intended) aims to provide tools to handle JPK_ force-files. It provides direct access to ``jpk-force``
files without the need to export them first. Data is loaded into a DataFrame and already converted to their respective
SI units.

Currently under development, only CellHesion200_ files are supported and analysis and plot tools are coming soon (®).

Usage
*****

.. code-block:: python

    >>> jpk_file = r'path/to/jpk-force/file'
    >>> sample = CellHesion(force_file=jpk_file)
    >>> sample.data.head()

+---------+------------+--------+------------+----------+------------+----------+------------+----------+
| segment | approach            | contact               | retract               | pause                 |
+---------+------------+--------+------------+----------+------------+----------+------------+----------+
| channel | force      | height | force      | height   | force      | height   | force      | height   |
+=========+============+========+============+==========+============+==========+============+==========+
| 0       | 4.2366e-11 | 0.0001 | 5.2684e-10 | 0.000026 | 5.4484e-10 | 0.000026 | 3.3515e-11 | 0.000099 |
+---------+------------+--------+------------+----------+------------+----------+------------+----------+
| 1       | 3.4831e-11 | 0.0001 | 5.1763e-10 | 0.000026 | 5.5237e-10 | 0.000026 | 3.4518e-11 | 0.000099 |
+---------+------------+--------+------------+----------+------------+----------+------------+----------+

Plotting
********

.. code-block:: python

    >>> import matplotlib.pyplot as plt
    >>> x = sample.data.retract.height * 10**6
    >>> y = sample.data.retract.force * 10**12
    >>> plt.plot(x, y)
    >>> plt.xlabel("height [µm]"); plt.ylabel("force [pN]")

|retract|

*This is only a teaser; the full documentation can be found at*
`Read the Docs <http://jpkay.readthedocs.org/>`_

Authors
-------

-  Tony Fischer (tku137)
-  Jeremy Perez (jimixxperez)

License
-------
``JPKay`` is licensed under the MIT-license_.

.. _JPK: http://www.jpk.com/
.. _CellHesion200: http://usa.jpk.com/index.395.us.html
.. |retract| image:: docs/source/images/retract_curve.png
.. _MIT-license: https://github.com/tku137/JPKay/blob/master/LICENSE
