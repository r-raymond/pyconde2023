import math


class Vec:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __len__(self):
        return math.sqrt(self * self)

    def scale(self, fac):
        return Vec(self.x * fac, self.y * fac, self.z * fac)

    def normal(self):
        return self.scale(1 / self.__len__())

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Sphere:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    def intersect(self, line):
        dif = line.p - self.q
        sp = line.v * dif

        rat = 4 * (sp * sp - (dif * dif - self.r**2))

        if rat >= 0:
            sqrat = math.sqrt(rat)
            t = min(-1 * sp + sqrat / 2, -1 * sp - sqrat / 2)
            return line.p + line.v.scale(t)

        else:
            return None

    def get_normal(self, p):
        dif = p - self.q
        return dif.normal()


class Line:
    def __init__(self, p, v):
        self.p = p
        self.v = v
