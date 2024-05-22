from typing import Union


class Unit(type):
    def __new__(cls, name: str, bases: tuple, **kwargs):
        return super(Unit, cls).__new__(cls, name, bases, kwargs)

class LengthUnit(Unit):
    def __new__(cls, name: str, short_name: str, conversion_value: float):
        bases = (Length, )
        return super().__new__(
            cls,
            name,
            bases,
            short_name=short_name,
            conversion_value=conversion_value
        )

class TimeUnit(Unit):
    def __new__(cls, name: str, short_name: str, conversion_value: float):
        bases = (Time, )
        return super().__new__(
            cls,
            name,
            bases,
            short_name=short_name,
            conversion_value=conversion_value
        )

class Measurement():
    def __init__(self, value: Union[int, float, complex]):
        self._value = float(value)

    def to(self, unit):
        return unit(self._value * distance_unit.conversion_value)

    def __str__(self):
        return f"{self._value} {self.short_name}"

    def __neg__(self):
        return self.__class__(-self._value)

    def __pos__(self):
        raise NotImplementedError

    def __abs__(self):
        return self.__class__(abs(self.value))

    def __invert__(self):
        raise NotImplementedError

    # Binary arithmetic operators
    def __add__(self, other):
        return self.__class__(self._value + other._value)

    def __sub__(self, other):
        return self.__class__(self._value - other._value)

    def __mul__(self, other):
        return self.__class__(self._value * other._value)

    def __matmul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __floordiv__(self, other):
        raise NotImplementedError

    def __mod__(self, other):
        raise NotImplementedError

    def __divmod__(self, other):
        raise NotImplementedError

    def __pow__(self, other, modulo=None):
        raise NotImplementedError

    def __lshift__(self, other):
        raise NotImplementedError

    def __rshift__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    # Reflected binary arithmetic operators
    def __radd__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __rmul__(self, other):
        raise NotImplementedError

    def __rmatmul__(self, other):
        raise NotImplementedError

    def __rtruediv__(self, other):
        raise NotImplementedError

    def __rfloordiv__(self, other):
        raise NotImplementedError

    def __rmod__(self, other):
        raise NotImplementedError

    def __rdivmod__(self, other):
        raise NotImplementedError

    def __rpow__(self, other, modulo=None):
        raise NotImplementedError

    def __rlshift__(self, other):
        raise NotImplementedError

    def __rrshift__(self, other):
        raise NotImplementedError

    def __rand__(self, other):
        raise NotImplementedError

    def __rxor__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    # Augmented assignment operators
    def __iadd__(self, other):
        raise NotImplementedError

    def __isub__(self, other):
        raise NotImplementedError

    def __imul__(self, other):
        raise NotImplementedError

    def __imatmul__(self, other):
        raise NotImplementedError

    def __itruediv__(self, other):
        raise NotImplementedError

    def __ifloordiv__(self, other):
        raise NotImplementedError

    def __imod__(self, other):
        raise NotImplementedError

    def __ipow__(self, other, modulo=None):
        raise NotImplementedError

    def __ilshift__(self, other):
        raise NotImplementedError

    def __irshift__(self, other):
        raise NotImplementedError

    def __iand__(self, other):
        raise NotImplementedError

    def __ixor__(self, other):
        raise NotImplementedError

    def __ior__(self, other):
        raise NotImplementedError

    # Type conversion methods
    def __int__(self):
        raise NotImplementedError

    def __float__(self):
        raise NotImplementedError

    def __complex__(self):
        raise NotImplementedError

    def __index__(self):
        raise NotImplementedError

    def __round__(self, ndigits=None):
        raise NotImplementedError

    def __trunc__(self):
        raise NotImplementedError

    def __floor__(self):
        raise NotImplementedError

    def __ceil__(self):
        raise NotImplementedError

class Length(Measurement):
    pass

class Time(Measurement):
    pass


Kilometer = LengthUnit("Kilometer", "km", 1000.0)
Meter = LengthUnit("Meter", "m", 1.0)
Centimeter = LengthUnit("Centimeter", "cm", 0.01)
Millimeter = LengthUnit("Millimeter", "mm", 0.001)

Second = TimeUnit("Second", "s", 1.0)
Minute = TimeUnit("Minute", "m", 60.0)
Hour = TimeUnit("Hour", "h", 3600.0)
Day = TimeUnit("Day", "D", 86400.0)

__all__ = (
    # Type Classes
    "Unit",
    "DistanceUnit",
    "TimeUnit"

    # Distance Units
    "Meter",
    "Kilometer",
    "Centimeter",
    "Millimeter",

    # Time Units
    "Second",
    "Minute",
    "Hour",
    "Day",
)
