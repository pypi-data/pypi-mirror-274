"""Resolution classes and methods."""

class Resolution():
    """Data class for storing resolution."""
    
    def __init__(self, width: int, height: int) -> None:
        """Initialize the resolution.

        Args:
            width (int): The pixel width of the resolution.
            height (int): The pixel height of the resolution.
        """         
        self.width = width
        self.height = height

    @property
    def width(self) -> int:
        """Pixel width of the resolution.

        Returns:
            int: The width.
        """
        return self._width
    
    @width.setter
    def width(self, value: int):
        self._width = int

    @property
    def height(self) -> int:
        """Pixel height of the resolution.

        Returns:
            int: The height.
        """
        return self._height
    
    @height.setter
    def height(self, value: int):
        self._height = value
