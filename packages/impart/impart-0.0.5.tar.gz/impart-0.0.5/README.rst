impart
======

.. image:: https://readthedocs.org/projects/impart/badge/?version=latest
    :target: https://impart.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/impart?color=blue
    :target: https://pypi.org/project/impart
    :alt: PyPI - Version

``impart`` (**im**\ age **part**\ itioning) provides a simple representation of
images and volumes (of arbitrary size) as a partition (i.e., grid) of
fixed-size cells, with a given step size between cells.

Partitions can be indexed and sliced like NumPy arrays. Any extracted image
region is only loaded into memory after calling ``.numpy()``.
Complex indexing logic is abstracted. ``impart`` also includes some utilities, e.g., multi-core fragmentation
of partitions into their individual cells.

Viewing image sub-regions as cells with a fixed step is useful for data
processing in several domains, such as remote sensing, medical imaging, and
deep learning.

.. end-include

Installation, usage & benchmarks
--------------------------------

Please refer to the official documentation:

    https://impart.readthedocs.io/en/latest/
