"""define a two dimensional point used by polygon objects."""


class Point:
    """represent a point with x and y coordinates."""

    def __init__(self, x: int, y: int) -> None:
        """initialize a point with x and y coordinates."""
        self.__x: int = x
        self.__y: int = y

    @property
    def x(self) -> int:
        """return the x coordinate."""
        return self.__x

    @x.setter
    def x(self, value: int) -> None:
        """set the x coordinate."""
        self.__x = value

    @property
    def y(self) -> int:
        """return the y coordinate."""
        return self.__y

    @y.setter
    def y(self, value: int) -> None:
        """set the y coordinate."""
        self.__y = value
