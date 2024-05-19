impart
==================================

``impart`` is short for **im**\ age **part**\ itioning.
It also means "to give" in English.

Quickly index, slice and split arbitrarily large images with any number of
channels! Also works on volumes, i.e., collections/time-series of same-sized
images.

Useful for working with image data in several domains, such as
remote sensing, medical imaging, deep learning, and more.

Image loading and cropping is done with ``pyvips``, which is very time and space
efficient. Refer to the `benchmarking section <#benchmarks>`_ for performance
figures.

Installation
------------

The dependency ``pyvips`` requires system libraries that prevent a simple
``pip install impart`` from succeeding on most systems.
To first install ``pyvips``, it's easiest to use ``conda``, as the conda
package already includes the needed system libraries. We refer to the pyvips
installation section for more details and alternative approaches:
https://github.com/libvips/pyvips?tab=readme-ov-file#install

.. code-block:: console

    conda create -n impart python=3.10 -y
    conda activate impart
    conda install --channel conda-forge pyvips -y
    pip install impart

For development, clone this repository and use:

.. code-block:: console

    conda create -n impart python=3.10 -y
    conda activate impart
    conda install --channel conda-forge pyvips
    pip install -r requirements-dev.txt

Quickstart
----------

Below are some simple examples to help you get started. More snippets can be
found in the ``examples/`` directory.

Images
~~~~~~

.. code-block:: python

    from impart import ImagePartition

    im = ImagePartition(
            "path/to/image.png", # in this example 1920x1080x3
            cell_dims=(128, 128), # size of cells as (height, width)
            stride=0.5, # or, e.g., (0.2, 0.6) for asymmetric stride
            channels=[0, 1, 2] # RGB
        )

    im.dims
    >>> (16, 29) # cells arranged in 16 rows and 29 columns

    im[:, 0]
    >>> <pyvips.Image 128x1080 uchar, 3 bands, srgb>

    im[:3, 15:21]
    >>> <pyvips.Image 384x192 uchar, 3 bands, srgb>

    # first time any image data is loaded into memory
    im[:10, -1].write_to_file("slice.png")

    im.image_subregion_of_cell(10, -1) # cell in the 10th row, last column
    >>> (1792, 640, 128, 128) # image coordinates as (left, top, width, height)


Volumes
~~~~~~~

To be added.

Benchmarks
----------

To be added.
