"""
Bentham Instruments spectral analysis package.
"""
from __future__ import annotations
import numpy
import typing
from . import colorimetry
from . import io
from . import monochromator
from . import physics
from . import utils
__all__ = ['AKIMA', 'CUBIC', 'Interpolation', 'LINEAR', 'NONE', 'Observer', 'POLYNOMIAL', 'Scan', 'colorimetry', 'io', 'monochromator', 'physics', 'utils']
class Interpolation:
    """
    Members:
    
      NONE
    
      AKIMA
    
      CUBIC
    
      LINEAR
    
      POLYNOMIAL
    """
    AKIMA: typing.ClassVar[Interpolation]  # value = <Interpolation.AKIMA: 1>
    CUBIC: typing.ClassVar[Interpolation]  # value = <Interpolation.CUBIC: 2>
    LINEAR: typing.ClassVar[Interpolation]  # value = <Interpolation.LINEAR: 3>
    NONE: typing.ClassVar[Interpolation]  # value = <Interpolation.NONE: 0>
    POLYNOMIAL: typing.ClassVar[Interpolation]  # value = <Interpolation.POLYNOMIAL: 4>
    __members__: typing.ClassVar[dict[str, Interpolation]]  # value = {'NONE': <Interpolation.NONE: 0>, 'AKIMA': <Interpolation.AKIMA: 1>, 'CUBIC': <Interpolation.CUBIC: 2>, 'LINEAR': <Interpolation.LINEAR: 3>, 'POLYNOMIAL': <Interpolation.POLYNOMIAL: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Observer:
    """
    Observer struct
    """
    def __init__(self, x: Scan, y: Scan, z: Scan) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def x(self) -> Scan:
        ...
    @property
    def y(self) -> Scan:
        ...
    @property
    def z(self) -> Scan:
        ...
class Scan:
    """
    
    Class to manipulate spectral data consisting of wavelength and value pairs.
    
    Usage:
    >>> scan1 = benanalysis.Scan() # create empty scan object
    >>> scan1[400] = 1.1  # start assigning values to wavelengths
    >>> print(scan1[400]) # and retrieving them
    1.1
    >>> scan2 = benanalysis.Scan([400,405,410,415,420],[1,2,3,4,5])  # initialise with list or numpy arrays
    >>> scan2(402) # call with one value to interpolate
    2.4
    >>> scan2(402,415) # call with one value to integrate
    35.1
    >>> scan3 = log10(scan1+1) * scan2  # do complex maths
    Scan(400→420[5])
    >>> scan3.to_numpy()
    [[4.00000000e+02 4.05000000e+02 4.10000000e+02 4.15000000e+02
      4.20000000e+02]
     [9.06190583e-02 2.27644692e-01 3.62476233e-01 4.88559067e-01
      6.05519368e-01]]
    """
    __hash__: typing.ClassVar[None] = None
    epsilon: float
    interpolation: Interpolation
    @typing.overload
    def __add__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __add__(self, arg0: float) -> Scan:
        ...
    @typing.overload
    def __call__(self, wavelength: float) -> float:
        """
          Indirect access to the data to allow interpolation. Note does not extrapolate
          or throw, returns zero if wavelength is out of bounds.
        """
    @typing.overload
    def __call__(self, wavelength_from: float, wavelength_to: float) -> float:
        """
          The numerical integral result of the interpolated function over the range
          [wavelength_from, wavelength_to].
        """
    def __eq__(self, arg0: Scan) -> bool:
        ...
    def __getitem__(self, arg0: float) -> float:
        ...
    @typing.overload
    def __iadd__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __iadd__(self, arg0: float) -> Scan:
        ...
    @typing.overload
    def __imul__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __imul__(self, arg0: float) -> Scan:
        ...
    @typing.overload
    def __init__(self, epsilon: float = 1e-20, interpolation: Interpolation = Scan.Interpolation.AKIMA) -> None:
        """
              Initialise an empty Scan, storing epsilon and interpolation.
        
              Parameters
              ----------
              epsilon : float, optional
                Wavelength epsilon (default is Scan.Default_Wavelength_Epsilon)
              interpolation : Interpolation, optional
                Interpolation type (default is Interpolation.Akima)
        """
    @typing.overload
    def __init__(self, wavelength_array: list[float], value_array: list[float], epsilon: float = 1e-20, interpolation: Interpolation = Scan.Interpolation.AKIMA) -> None:
        """
              Initialise a scan with lists of wavelength and values, wavelength epsilon, and interpolation type.
        
              Parameters
              ----------
              wavelength_array : list of float
                List of wavelengths
              value_array : list of float
                List of values corresponding to the wavelengths
              epsilon : float, optional
                Wavelength epsilon (default is Scan.Default_Wavelength_Epsilon)
              interpolation : Interpolation, optional
                Interpolation type (default is Interpolation.Akima)
        """
    @typing.overload
    def __isub__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __isub__(self, arg0: float) -> Scan:
        ...
    def __iter__(self) -> typing.Iterator[float]:
        ...
    @typing.overload
    def __itruediv__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __itruediv__(self, arg0: float) -> Scan:
        ...
    @typing.overload
    def __mul__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __mul__(self, arg0: float) -> Scan:
        ...
    def __neg__(self) -> Scan:
        ...
    @typing.overload
    def __pow__(self, arg0: float) -> Scan:
        ...
    @typing.overload
    def __pow__(self, arg0: Scan) -> Scan:
        ...
    def __radd__(self, arg0: float) -> Scan:
        ...
    def __repr__(self) -> str:
        ...
    def __rmul__(self, arg0: float) -> Scan:
        ...
    def __rpow__(self, arg0: float) -> Scan:
        ...
    def __rsub__(self, arg0: float) -> Scan:
        ...
    def __rtruediv__(self, arg0: float) -> Scan:
        ...
    def __setitem__(self, arg0: float, arg1: float) -> None:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def __sub__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __sub__(self, arg0: float) -> Scan:
        ...
    @typing.overload
    def __truediv__(self, arg0: Scan) -> Scan:
        ...
    @typing.overload
    def __truediv__(self, arg0: float) -> Scan:
        ...
    def add(self, wavelength: float, value: float) -> None:
        """
        Add a wavelength, value point to the scan.
        """
    def is_interpolated(self) -> bool:
        """
          Returns whether or not the scan uses interpolation (a SplineType other than
          NONE).
        """
    def items(self) -> typing.Iterator[tuple[float, float]]:
        ...
    def to_lists(self) -> list[list[float]]:
        """
        Convert Scan object to a pair of lists
        """
    def to_numpy(self) -> numpy.ndarray[numpy.float64]:
        """
          Convert Scan object to a 2D numpy array where index 0 and 1 are arrays of
          wavelengths and values respectively
        """
    def values(self) -> list[float]:
        """
        return the values from the scan object
        """
    def wavelengths(self) -> list[float]:
        """
        return the wavelengths from the scan object
        """
    @property
    def integral(self) -> float:
        """
        Returns the integral of the Scan over the entire wavelength domain
        """
    @property
    def x(self) -> Scan:
        """
        Returns Scan(self.wavelengths(), self.wavelengths())
        """
AKIMA: Interpolation  # value = <Interpolation.AKIMA: 1>
CUBIC: Interpolation  # value = <Interpolation.CUBIC: 2>
LINEAR: Interpolation  # value = <Interpolation.LINEAR: 3>
NONE: Interpolation  # value = <Interpolation.NONE: 0>
POLYNOMIAL: Interpolation  # value = <Interpolation.POLYNOMIAL: 4>
