from __future__ import annotations
from typing import Any, Generic, Iterable, TypeVar, overload


T = TypeVar("T")
class Vector(Generic[T]):
    components: tuple[T, ...]

    def __init__(self, *components: T) -> None:
        self.components = components

    # === addition / subtraction produce a Vector with the component result type ===
    @overload
    def __add__(self: Vector[int], other: Vector[float]) -> Vector[float]: ...
    @overload
    def __add__(self: Vector[float], other: Vector[int]) -> Vector[float]: ...
    @overload
    def __add__(self: Vector[T], other: Vector[T]) -> Vector[T]: ...

    def __add__(self, other: Vector[Any]) -> Vector[Any]:
        if len(self.components) != len(other.components):
            raise ArithmeticError("Add: Undefined Operation for vectors of different sizes.")
        return Vector(*(c + k for c, k in zip(self.components, other.components)))

    @overload
    def __sub__(self: Vector[int], other: Vector[float]) -> Vector[float]: ...
    @overload
    def __sub__(self: Vector[float], other: Vector[int]) -> Vector[float]: ...
    @overload
    def __sub__(self: Vector[T], other: Vector[T]) -> Vector[T]: ...

    def __sub__(self, other: Vector[Any]) -> Vector[Any]:
        if len(self.components) != len(other.components):
            raise ArithmeticError("Sub: Undefined Operation for vectors of different sizes.")
        return Vector(*(c - k for c, k in zip(self.components, other.components)))


    # === dot product: returns scalar ===
    @overload
    def __mul__(self: Vector[int], other: Vector[float]) -> float: ...
    @overload
    def __mul__(self: Vector[float], other: Vector[int]) -> float: ...
    @overload
    def __mul__(self: Vector[T], other: Vector[T]) -> T: ...
    @overload
    def __mul__(self: Vector[int], other: float) -> Vector[float]: ...
    @overload
    def __mul__(self: Vector[float], other: int) -> Vector[float]: ...
    @overload
    def __mul__(self: Vector[T], other: T) -> Vector[T]: ...

    def __mul__(self, other: Vector[Any] | Any) -> Any:
        if isinstance(other, Vector):
            # Dot Product
            if len(self.components) != len(other.components):
                raise ArithmeticError("Mul: Undefined Operation for vectors of different sizes.")
            res = 0
            for c, k in zip(self.components, other.components):
                res += c * k
            return res
        else:
            # Scalar Multiplication
            scalar = other
            return Vector(*(scalar * c for c in self.components))

    @overload
    def __rmul__(self: Vector[int], scalar: float) -> Vector[float]: ...
    @overload
    def __rmul__(self: Vector[float], scalar: int) -> Vector[float]: ...
    @overload
    def __rmul__(self: Vector[T], scalar: T) -> Vector[T]: ...

    def __rmul__(self, scalar: T) -> Vector[T]:
        return Vector(*(scalar * c for c in self.components))

    @overload
    def __truediv__(self: Vector[int], other: Vector[float]) -> float: ...
    @overload
    def __truediv__(self: Vector[float], other: Vector[int]) -> float: ...
    @overload
    def __truediv__(self: Vector[T], other: Vector[T]) -> T: ...
    @overload
    def __truediv__(self: Vector[int], other: float) -> Vector[float]: ...
    @overload
    def __truediv__(self: Vector[float], other: int) -> Vector[float]: ...
    @overload
    def __truediv__(self: Vector[T], other: T) -> Vector[T]: ...

    def __truediv__(self, other: Vector[Any] | Any) -> Any:
        if isinstance(other, Vector):
            # Dot Product
            if len(self.components) != len(other.components):
                raise ArithmeticError("Div: Undefined Operation for vectors of different sizes.")
            res = 0
            for c, k in zip(self.components, other.components):
                res += c / k
            return res
        else:
            # Scalar Division
            scalar = other
            return Vector(*(c / scalar for c in self.components))

    @overload
    def __floordiv__(self: Vector[int], other: Vector[float]) -> float: ...
    @overload
    def __floordiv__(self: Vector[float], other: Vector[int]) -> float: ...
    @overload
    def __floordiv__(self: Vector[T], other: Vector[T]) -> T: ...
    @overload
    def __floordiv__(self: Vector[int], other: float) -> Vector[float]: ...
    @overload
    def __floordiv__(self: Vector[float], other: int) -> Vector[float]: ...
    @overload
    def __floordiv__(self: Vector[T], other: T) -> Vector[T]: ...

    def __floordiv__(self, other: Vector[Any] | Any) -> Any:
        if isinstance(other, Vector):
            # Dot Product
            if len(self.components) != len(other.components):
                raise ArithmeticError("Div: Undefined Operation for vectors of different sizes.")
            res = 0
            for c, k in zip(self.components, other.components):
                res += c // k
            return res
        else:
            # Scalar Division
            scalar = other
            return Vector(*(c // scalar for c in self.components))

    def __str__(self):
        return str(self.components)
    
    def __repr__(self):
        return f"Vector{self.components}"
    
    def __len__(self):
        return len(self.components)
    
    def __getitem__(self, key: int) -> T:
        return self.components[key]
    
    def __iter__(self) -> Iterable[T]:
        return iter(self.components)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.components == other.components
    
    def __neg__(self) -> Vector[T]:
        return Vector(*(-c for c in self.components))
    
    def __abs__(self) -> Vector[T]:
        return Vector(*(abs(c) for c in self.components))
    
    def __round__(self, n: int = 0) -> Vector[T]:
        return Vector(*(round(c, n) for c in self.components))
    
    def __floor__(self) -> Vector[T]:
        return Vector(*(c // 1 for c in self.components))
    
    def __ceil__(self) -> Vector[T]:
        return Vector(*(c // 1 + 1 for c in self.components))
    
    def __hash__(self) -> int:
        return hash(self.components)
    
    def __bool__(self) -> bool:
        return any(self.components)
    
    def __copy__(self) -> Vector[T]:
        return Vector(*self.components)
    
    def __deepcopy__(self, _: dict[int, Any]) -> Vector[T]:
        return Vector(*self.components)
    
    def __len__(self) -> int:
        return len(self.components)
    
    def norm(self, p: float = 2.0) -> float:
        if p == float("inf"):
            return max(abs(c) for c in self.components)
        return sum(c ** p for c in self.components) ** (1 / p)