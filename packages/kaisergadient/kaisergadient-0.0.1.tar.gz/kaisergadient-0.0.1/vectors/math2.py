import math

class Vector2d:
    def __init__(self, x, y):
        self.x, self.y = x,y

    @staticmethod
    def zero():
        return Vector2d(0, 0)
    def up():
        return Vector2d(0, 1)

    def __str__(self):
        return str((self.x, self.y))

    def __add__(self, other):
        if other.__class__ != Vector2d:
            return Vector2d(self.x + other, self.y + other)
        else:
            return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if other.__class__ != Vector2d:
            return Vector2d(self.x - other, self.y - other)
        else:
            return Vector2d(self.x - other.x, self.y - other.y)
    def magnitude(self):
       return math.sqrt(self.x**2 + self.y**2)
    def __mul__(self, other):
        if other.__class__ != Vector2d:
            return Vector2d(self.x * other, self.y * other)
        else:
            return Vector2d(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if other.__class__ != Vector2d:
            return Vector2d(self.x / other, self.y/other)
        else:
            return Vector2d(self.x / other.x, self.y/other.y)

    def __matmul__(self, other):
        if other.__class__ != Vector2d:
            return Vector2d(self.x * other, self.y * other)
        else:
            return Vector2d(self.x * other.x, self.y * other.y)

    def __rmul__(self, other):
        if other.__class__ != Vector2d:
            return Vector2d(self.x * other, self.y * other)
        else:
            return Vector2d(self.x * other.x, self.y * other.y)


class Vector3d:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x,y,z

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __add__(self, other):
        if other.__class__ != Vector3d:
            return Vector3d(self.x + other, self.y + other, self.z + other)
        else:
            return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if other.__class__ != Vector2d:
            return Vector3d(self.x - other, self.y - other, self.z - other)
        else:
            return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)
    def magnitude(self):
       return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def __mul__(self, other):
        if other.__class__ != Vector2d:
            return Vector3d(self.x * other, self.y * other, self.z * other)
        else:
            return Vector3d(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):
        if other.__class__ != Vector2d:
            return Vector3d(self.x / other, self.y/other, self.z/other)
        else:
            return Vector3d(self.x / other.x, self.y/other.y, self.z/other.z)
