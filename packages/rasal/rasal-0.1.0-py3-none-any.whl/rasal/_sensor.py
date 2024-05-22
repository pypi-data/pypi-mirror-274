from .units import Length


class Sensor():
    
    def __init__(
            self,
            name: str,
            width: Length,
            height: Length,
            squeeze: float
    ) -> None:
        """Initialize the sensor.

        Args:
            name (str): The name of the sensor.
            width (Length): The width of the sensor.
            height (Length): The height of the sensors.
            squeeze (float): Any squeeze applied to the sensor.
        """
        self.width = width
        self.height = height
        self.squeeze = squeeze
        self.name = name

    @property
    def width(self) -> Length:
        """The width of the sensor.

        Returns:
            Length: The width.
        """
        return self._width
    
    @width.setter
    def width(self, value: Length):
        self._width = value

    @property
    def height(self) -> Length:
        """The height of the sensor.

        Returns:
            Length: The height.
        """
        return self._height
    
    @width.setter
    def height(self, value: Length):
        self._height = value

    @property
    def squeeze(self) -> float:
        """The squeeze of the sensor.

        Returns:
            float: The squeeze.
        """
        return self._squeeze

    @squeeze.setter
    def squeeze(self, value: float):
        self._squeeze = value

    @property
    def name(self) -> str:
        """The name of the sensor.

        Returns:
            str: The name.
        """         
        return self._name

    @name.setter    
    def name(self, value):
        self._name = value

    def squeezed_width(self) -> Length:
        """The "true" squeezed width of the sensor.

        Effectively just: 
            sensor.width * sensor.squeeze

        Returns:
            Length: The resulting squeezed width.
        """
        return self.width * self.squeeze

    def squeezed_height(self) -> Length:
        """The "true" squeezed height of the sensor.

        Effectively just: 
            sensor.height * sensor.squeeze

        Returns:
            Length: The resulting squeezed height.
        """
        return self.height * self.squeeze
