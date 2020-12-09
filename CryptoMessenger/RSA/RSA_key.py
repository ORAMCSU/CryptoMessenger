"""RSA_key.py"""


# Authors:
# Julien Marzal-Hilaire
# Paul Nadal


class RSA_key:

    # --------------------PGCD--------------------
    @staticmethod
    def pgcd(a, b):
        while b > 0:
            a, b = b, a % b
        return a

    # --------------------Bezout--------------------
    @staticmethod
    def bezout(a, b):
        u0, v0, u1, v1 = 1, 0, 0, 1
        while b:
            q, r = divmod(a, b)
            a, b = b, r
            u0, v0, u1, v1 = u1, v1, u0 - q * u1, v0 - q * v1
        return u0

    # --------------------Key Creation--------------------
    @classmethod
    def key(cls, p, q):
        n = p * q

        m = (p - 1) * (q - 1)

        e = 2
        r = cls.pgcd(e, m)
        while r != 1:
            e += 1
            r = cls.pgcd(e, m)

        d = cls.bezout(e, m)

        public = (n, e)
        private = (d, n)

        clefs = [public, private]

        return clefs


print(RSA_key.key(3, 11))
