from numba import njit, uintc, complex128

max_real = 2.0
max_imag = max_real
number = 5000
max_radius = 50.0
iters = 100


@njit(uintc(complex128), nogil=True)
def iterate_until_escape(z):
    z0 = z
    for i in range(1, iters):
        z0 = z0**2 - 0.5
        if abs(z0) > max_radius:
            return i
    return 0


@njit(nogil=True)
def to_rgb(i):
    if i == 0:
        return "255 255 255 "
    else:
        b = 255 * i // iters
        return "0 {0} {0} ".format(b)


@njit(uintc(complex128), nogil=True)
def jul(z):
    return iterate_until_escape(z)


@njit
def xloop(y):
    return [
        jul((2 * max_imag / number) * (x + 1j * y) - (2 + 2j))
        for x in range(number)
    ]


def main():
    with open("set.ppm", "w") as file:
        file.write(f"P3\n{number} {number}\n255\n")
        for y in range(number, 0, -1):
            file.write("".join([
                "0 {0} {0} ".format(it) if it != 0 else "255 255 255 "
                for it in xloop(y)
            ]))
    return


main()
