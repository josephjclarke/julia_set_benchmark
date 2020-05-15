import numpy as np

max_real = 2.0
max_imag = max_real
number = 5000
max_radius = 50.0
iters = 100


def iterate_until_escape(z):
    z0 = z
    ni = np.zeros(z0.shape, dtype=np.int)
    for i in range(1, iters):
        ni0 = (ni == 0)
        z0[np.where(ni0)] = z0[np.where(ni0)]**2 - 0.5
        ni[np.logical_and(ni0, abs(z0) > max_radius)] = i
    return ni


def to_rgb(i):
    if i == 0:
        return "255 255 255 "
    else:
        b = 255 * i // iters
        return "0 {0} {0} ".format(b)


def jul(z):
    return iterate_until_escape(z)


xs = np.linspace(-max_real, max_real, number)
ys = np.linspace(max_imag, -max_imag, number)


def main():
    with open("set.ppm", "w") as file:
        file.write(f"P3\n{number} {number}\n255\n")
        contents = "".join([
            to_rgb(it)
            for it in np.nditer(jul(xs[np.newaxis, :] +
                                    1j * ys[:, np.newaxis]))
        ])


main()
