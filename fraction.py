from math import gcd


class Fraction:
    def __init__(self, num, den=1):
        if den == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        if den < 0:
            num, den = -num, -den
        common = gcd(num, den) or 1
        self.num = num // common
        self.den = den // common

    def __str__(self):
        return "{}/{}".format(self.num, self.den)

    def __repr__(self):
        return self.__str__()

    def __float__(self):
        return self.num / self.den

    # ---------- addition ----------
    def __add__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den + other.num * self.den,
                             self.den * other.den)
        elif isinstance(other, int):
            return Fraction(self.num + other * self.den, self.den)
        elif isinstance(other, float):
            return float(self) + other
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    # ---------- subtraction ----------
    def __sub__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den - other.num * self.den,
                             self.den * other.den)
        elif isinstance(other, int):
            return Fraction(self.num - other * self.den, self.den)
        elif isinstance(other, float):
            return float(self) - other
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, int):
            return Fraction(other * self.den - self.num, self.den)
        elif isinstance(other, float):
            return other - float(self)
        return NotImplemented

    # ---------- multiplication ----------
    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.num, self.den * other.den)
        elif isinstance(other, int):
            return Fraction(self.num * other, self.den)
        elif isinstance(other, float):
            return float(self) * other
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)