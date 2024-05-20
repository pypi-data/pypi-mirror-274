import math
import types
from enum import Enum

import pyvips
from numpy import isclose
from pyvips import Image


class _Axis(Enum):
    ROW = 0
    COL = 1


class ImagePartition:
    """
    An ``ImagePartition`` is a two-dimensional grid overlaid onto
    an image, where any cell(s) in the grid can be selected using regular
    indexing operations (such as ``img[y, x]``, ``img[:, x1:x2]``, etc.).

    Indexing selects the area of the indexed cell(s) from the original image,
    but does not load data into memory. After indexing, use ``.numpy()`` on the
    returned ``pyvips.Image`` to load its data.
    """

    def __init__(self,
                 image: str,
                 cell_shape: tuple[int, int],
                 stride: float | tuple[float, float] = 1.0,
                 channels: tuple[int, ...] = (0, 1, 2)):
        """
        Construct an image partition.

        :param image: Path to an image. The image can have an arbitrary number
            of channels.
        :param cell_shape: Shape ``(height, width)`` of cells in the
            partition.
        :param stride: Step size (relative to ``cell_shape``) between cells.
            Can be a single float for uniform stride, or a tuple of floats to
            specify a stride for each axis.
            The amount of overlap between adjacent cells is ``1 - stride``,
            e.g., 0.3 or 30% for a stride of 0.7.
        :param channels: Image channels to consider for this partition.
        """
        cell_shape = self._check_tuple_arg(
            cell_shape, f"{cell_shape=}".split('=')[0], int.__name__)
        self.cell_shape: tuple[int, int] = cell_shape

        stride: tuple[float, float] = self._check_tuple_arg(
            stride, f"{stride=}".split('=')[0], float.__name__)
        self._stride = stride

        step_size = tuple(
            c * s for c, s in zip(cell_shape, stride))
        assert len(step_size) == 2

        self.step_size: tuple[float, float] = (step_size[0], step_size[1])

        self.image: Image = pyvips.Image.new_from_file(image)

        try:
            self.image: Image = self.image[list(channels)]
        except IndexError as e:
            raise IndexError(f"Invalid channels for image: {channels}") from e

        self.channels: tuple[int, ...] = channels

        self.image_shape: tuple[int, int] = (
            self.image.height, self.image.width)

        shape = tuple(
            # The first cell, plus however many steps
            # fit into the remaining space, rounded up
            1 + math.ceil(max(0, dim - cell) / step)
            for dim, cell, step in zip(
                self.image_shape, self.cell_shape, self.step_size))

        assert len(shape) == 2
        self.shape: tuple[int, int] = (
            shape[0], shape[1])

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

    __I = int | slice | None | types.EllipsisType

    def __getitem__(self, index: __I | tuple[__I, __I]) -> Image:
        """
        Return an image subregion from an index.

        :param index: Partition index.
        :return: Image subregion as ``pyvips.Image``.
        """
        if isinstance(index, tuple):
            if len(index) > 2:
                raise ValueError(
                    f"Cannot index more than two axes in an image")
            return self.image.crop(*self.compute_image_subregion(*index))
        elif isinstance(index, ImagePartition.__I):
            return self.image.crop(*self.compute_image_subregion(index))
        else:
            raise TypeError(
                f"Index has invalid type '{type(index).__name__}'")

    def compute_image_subregion(self,
                                y: __I,
                                x: __I = None) -> tuple[int, int, int, int]:
        """
        Compute the image subregion corresponding to the area of the cell(s)
        over ``self.image[y, x]``.

        :param y: Row index or slice.
        :param x: Column index or slice.
        :return: Bounding box in image coordinates (left, top, width, height).
        """

        top, height = self._compute_axis(_Axis.ROW, y)
        left, width = self._compute_axis(_Axis.COL, x)

        return left, top, width, height

    def _compute_axis(self, axis: _Axis, index: __I) -> tuple[int, int]:
        axis = axis.value
        if isinstance(index, int):
            if index >= self.shape[axis]:
                raise IndexError(
                    f"Index {index} is out of bounds for axis {axis} "
                    f"with size {self.shape[axis]}")
            if index < 0:
                index += self.shape[axis]
            index = slice(index, index + 1)
        elif index is None or isinstance(index, types.EllipsisType):
            index = slice(0, self.shape[axis])

        if not isinstance(index, slice):
            raise TypeError(
                "Cannot index axis with "
                f"value of type '{type(index).__name__}'")

        return self._compute_axis_from_slice(axis, index)

    def _compute_axis_from_slice(
            self, axis: int, index: slice) -> tuple[int, int]:
        if (index.start is not None
                and not isinstance(index.start, int)
                or (index.stop is not None
                    and not isinstance(index.stop, int))):
            raise TypeError("slice indices must be integers or None")

        if index.start is None and index.stop is None:
            index = slice(0, self.shape[axis])
        elif index.start is None:
            index = slice(0, index.stop)
        elif index.stop is None:
            index = slice(index.start, self.shape[axis])

        if index.start >= self.shape[axis]:
            raise IndexError(
                f"{index} is out of bounds for axis {axis} "
                f"with size {self.shape[axis]}")
        if index.stop > self.shape[axis]:
            index = slice(index.start, self.shape[axis])

        if index.start >= index.stop:
            raise ValueError(f"Empty or inverted slice: {index}")

        if index.start < 0:
            index = slice(index.start + self.shape[axis],
                          index.stop)
        if index.stop < 0:
            index = slice(index.start,
                          index.stop + self.shape[axis])

        start = math.ceil(
            index.start * self.step_size[axis])
        stop = math.ceil(self.cell_shape[axis]
                         + (index.stop - 1) * self.step_size[axis])
        span = min(stop - start, self.image_shape[axis] - start)

        return start, span

    def __str__(self) -> str:
        return (f"{ImagePartition.__name__}("
                f"{self.image}, {self.cell_shape}, "
                f"{self._stride}, {self.channels})")

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: "ImagePartition") -> bool:
        return (self.image == other.image
                and self.cell_shape == other.cell_shape
                and self._stride == other._stride
                and isclose(other.step_size, self.step_size)
                and self.channels == other.channels
                and self.image_shape == other.image_shape
                and self.shape == other.shape)
