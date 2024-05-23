from __future__ import annotations

class Vector():
    
    value: tuple

    def __init__(self, *values) -> None:
        """Initialize a Vector"""
        self.value = values

    def __eq__(self, other: Vector) -> bool:
        """Compare a Vector"""
        if len(self.value) != len(other.value):
            return False

        for i in range(len(self.value)):
            if self.value[i] != other.value[i]:
                return False

        return True

    def __str__(self) -> str:
        return f"Vector({', '.join([str(x) for x in self.value])})"

    def __call__(self) -> tuple:
        return self.value
