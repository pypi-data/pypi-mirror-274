class Complex:
    def __init__(self, real, img):
        self.real = real
        self.img = img
    def __add__(self, numx):
        NewReal = self.real + numx.real
        NewImg = self.img + numx.img
        return Complex(NewReal,NewImg)
    def __sub__(self, numx):
        NewReal = self.real - numx.real
        NewImg = self.img - numx.img
        return Complex(NewReal,NewImg)
    def __sub__(self, numx):
        NewReal = self.real - numx.real
        NewImg = self.img - numx.img
        return Complex(NewReal,NewImg)
    def __mul__(self, numx):
        NewReal = self.real * numx.real - self.img * numx.img
        NewImg = self.real * numx.img + self.img * numx.real
        return Complex(NewReal, NewImg)
    def __truediv__(self, other):
        denominator = other.real ** 2 + other.img ** 2
        if denominator == 0:
            raise ZeroDivisionError("division by zero")
        NewReal = (self.real * other.real + self.img * other.img) / denominator
        NewImg = (self.img * other.real - self.real * other.img) / denominator
        return Complex(NewReal, NewImg)
    def __mod__(self, other):
        raise NotImplementedError("Modulus operation is not typically defined for complex numbers")

    def __eq__(self, other):
        return self.real == other.real and self.img == other.img

    def __ne__(self, other):
        return not self.__eq__(other)

    def __abs__(self):
        return (self.real**2 + self.img**2) ** 0.5

    
    def __repr__(self):
        return f"Complex({self.real}, {self.img})"

    def __str__(self):
        return f"{self.real}i + {self.img}j"

num1 = Complex(10,20)
num2 = Complex(20,40)
print(num1 + num2)