def cross_product(a, b):
    return magnitude(a)*magnitude(b)*abs(delta_sin(a, b))

def magnitude(x):
    return (sum(i**2 for i in x)) ** 0.5

def delta_sin(a, b):
    cos_b_a = (a[0]*b[0] + a[1]*b[1])/(magnitude(a)*magnitude(b))
    sin_b_a = (1 - cos_b_a**2)**0.5
    return sin_b_a

CONSTANT2 = 'HELLO'