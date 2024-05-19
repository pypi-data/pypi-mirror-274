import math
from enum import Enum

import pyvips
from pyvips import Image


class _Axis(Enum):
    ROW = 0
    COL = 1


class ImagePartition:
    """
    Partition of an image into cells.
    An ``ImagePartition`` is a two-dimensional grid overlaid onto
    an image, where any cell(s) in the grid can be selected using regular
    indexing operations (such as ``img[y, x]``, ``img[:, x1:x2]``, etc.).
    Indexing extracts the area of the selected cell(s) from the original image.

    **Note**: Instances of this class never actually load the image or any
    indexed subregions into memory. After indexing, use ``img.numpy()`` to load
    the data.
    """

    def __init__(self,
                 image: str,
                 cell_dims: tuple[int, int],
                 stride: float | tuple[float, float],
                 channels: list[int]):
        """
        Construct an image partition.

        :param image: Path to an image. The image can have an arbitrary number
            of channels.
        :param cell_dims: Dimensions ``(height, width)`` of cells in the
            partition.
        :param stride: Step size (relative to ``cell_dims``) between cells. Can
            be a single float for uniform stride, or a tuple of floats to
            specify a stride for each axis.

            The amount of overlap between adjacent cells is given
            by ``1 - stride``, e.g., 0.3 or 30% for a stride of 0.7.
        :param channels: Image channels to consider for this partition.
        """
        stride = self._check_tuple_arg(stride,
                                       f"{stride=}".split('=')[0],
                                       float.__name__)
        self.stride: tuple[float, float] = stride

        cell_dims = self._check_tuple_arg(cell_dims,
                                          f"{cell_dims=}".split('=')[0],
                                          int.__name__)
        self.cell_dims: tuple[int, int] = cell_dims

        self.image: Image = pyvips.Image.new_from_file(image)

        try:
            self.image: Image = self.image[channels]
        except IndexError as e:
            raise IndexError(f"Invalid channels for image: {channels}") from e

        self.channels: list[int] = channels

        self.image_dims: tuple[int, int] = (
            self.image.height, self.image.width)

        dims = tuple(
            int(math.ceil((dim - cell) / (cell / (1 / stride))) + 1)
            for dim, cell, stride in zip(
                self.image_dims, self.cell_dims, self.stride))

        assert len(dims) == 2
        self.dims: tuple[int, int] = (
            dims[0], dims[1])

        self.geo_transform: tuple | None = None

    @staticmethod
    def _check_tuple_arg(arg, arg_name: str, dtype: str):
        if isinstance(arg, tuple):
            if len(arg) != 2:
                raise ValueError(
                    f"{arg_name} must be a {dtype} or a tuple of two {dtype}s")
            for a in arg:
                if not a > 0:
                    raise ValueError(
                        f"{arg_name} must be greater than 0 on all axes")
        else:
            arg = (arg, arg)
        return arg

    def __getitem__(
            self,
            coordinates: (int | slice | tuple[int, int] | tuple[slice, int]
                          | tuple[int, slice] | tuple[slice, slice])) -> Image:
        """
        Return an image subregion from partition coordinates.

        :param coordinates: Partition coordinates, as int, slice, or tuple.
        :return: Image subregion as ``pyvips.Image``.
        """
        if isinstance(coordinates, tuple):
            return self.image.crop(
                *self.image_subregion_of_cell(*coordinates))
        elif isinstance(coordinates, int) or isinstance(coordinates, slice):
            return self.image.crop(
                *self.image_subregion_of_cell(coordinates, None))
        else:
            raise TypeError(f"Cannot index with '{type(coordinates)}'")

    def image_subregion_of_cell(self,
                                y: int | slice,
                                x: int | slice | None = None
                                ) -> tuple[int, int, int, int]:
        """
        Calculate the image subregion corresponding to the area of the cell
        at position (y, x) in the partition.

        :param y: Row index.
        :param x: Column index.
        :return: Bounding box in image coordinates (left, top, width, height).
        """

        top, height = self._compute_axis(_Axis.ROW.value, y)
        if x is not None:
            left, width = self._compute_axis(_Axis.COL.value, x)
        else:
            left, width = 0, self.image.width

        return left, top, width, height

    def _compute_axis(self, axis, index):
        if isinstance(index, int):
            if index < 0:
                index += self.dims[axis]
            start = index * int(
                self.cell_dims[axis] / (1. / self.stride[axis]))
            span = min(self.image_dims[axis] - start, self.cell_dims[axis])
        elif isinstance(index, slice):
            if index.start is None and index.stop is None:
                index = slice(0, self.dims[axis])
            if index.start is None:
                index = slice(0, index.stop)
            if index.stop is None:
                index = slice(index.start, self.dims[axis])

            if index.start == index.stop:
                raise ValueError(f"Empty slice: {index}")

            if index.start < 0:
                index = slice(index.start + self.dims[axis],
                              index.stop)
            if index.stop < 0:
                index = slice(index.start,
                              index.stop + self.dims[axis])

            start = index.start * int(
                self.cell_dims[axis] / (1. / self.stride[axis]))
            span = min((index.stop - index.start) * int(
                self.cell_dims[axis] / (1. / self.stride[axis])),
                       self.image_dims[axis] - start)
        else:
            raise TypeError(f"Cannot index axis with '{type(index)}'")
        return start, span

    def __str__(self) -> str:
        return (f"{ImagePartition.__name__}("
                f"{self.image}, {self.cell_dims}, "
                f"{self.stride}, {self.channels})")

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: "ImagePartition") -> bool:
        return (self.image == other.image
                and self.cell_dims == other.cell_dims
                and self.stride == other.stride
                and self.channels == other.channels
                and self.image_dims == other.image_dims
                and self.dims == other.dims)
