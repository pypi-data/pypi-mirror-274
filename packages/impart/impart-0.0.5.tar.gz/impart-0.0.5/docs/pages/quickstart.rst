Quickstart
----------

Below are some simple examples to help you get started. More snippets can be
found in the `Usage guide`_.

.. _Usage guide: /docs/pages/usage_guide.rst

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
