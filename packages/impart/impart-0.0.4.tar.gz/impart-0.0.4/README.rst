impart
==================================

.. image:: https://readthedocs.org/projects/impart/badge/?version=latest
    :target: https://impart.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

``impart`` (**im**\ age **part**\ itioning) subdivides images and volumes of
arbitrary size into a virtual grid (partition) of fixed-size tiles (cells).
Partitions can be indexed and sliced like NumPy arrays. Any extracted image
region is only loaded into memory after calling ``.numpy()``. This lightweight
view is useful for data processing in several domains, such as
remote sensing, medical imaging, and deep learning.

Some utilities are included that use ``impart``, e.g., multi-core fragmentation
of an image into its individual cells, which are then written to disk.

Image loading and cropping are implemented using ``pyvips``, which is very time
and space efficient. Refer to the `benchmarking section <#benchmarks>`_ for
performance figures.

Installation
------------

The dependency ``pyvips`` requires C libraries that prevent a simple
``pip install impart`` from succeeding on most systems.
To first install ``pyvips``, it's easiest to use ``conda``, as the conda
package already includes the needed libraries. We refer to the pyvips
installation section for more details and alternative approaches:
https://github.com/libvips/pyvips?tab=readme-ov-file#install

.. code-block:: sh

    conda create -n impart python=3.10 -y
    conda activate impart
    conda install --channel conda-forge pyvips -y
    pip install impart

For development, clone this repository and use:

.. code-block:: sh

    conda create -n impart python=3.10 -y
    conda activate impart
    conda install --channel conda-forge pyvips -y
    pip install -r requirements-dev.txt

Quickstart
----------

Below are some simple examples to help you get started. More snippets can be
found in the ``examples/`` directory.

Images
~~~~~~

.. code-block:: python

    import numpy as np

    from impart import ImagePartition

    im = ImagePartition(
            "path/to/image.png", # in this example 1920x1080x3
            cell_shape=(128, 128), # cell dimensions as (height, width)
            stride=0.5, # or, e.g., (0.2, 0.6) for asymmetric stride
            channels=(0, 1, 2) # RGB
        )

    im.shape
    >>> (16, 29) # cells arranged in 16 rows and 29 columns

    im.step_size
    >>> (64.0, 64.0)

    im[:, 0]
    >>> <pyvips.Image 128x1080 uchar, 3 bands, srgb>

    im[:3, 15:21]
    >>> <pyvips.Image 448x256 uchar, 3 bands, srgb>

    # first time any image data is loaded into memory
    image_data = im[:10, -1].numpy(dtype=np.uint8)

    im.image_subregion_of_cell(10, -1) # cell in the 10th row, last column
    >>> (1792, 640, 128, 128) # image coordinates as (left, top, width, height)


Volumes
~~~~~~~

To be added.

Benchmarks
----------

To be added.
