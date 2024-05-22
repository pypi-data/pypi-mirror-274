# taylorexpansion/series.py

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def taylor_series(func, n_terms, x0=0):
    """
    Compute the Taylor series expansion of a given function.

    Parameters:
    func (function): The function to expand.
    n_terms (int): Number of terms in the Taylor series.
    x0 (float): The point around which to expand the function.

    Returns:
    list: Coefficients of the Taylor series expansion.
    """
    import sympy as sp

    x = sp.symbols('x')
    f = func(x)
    series = f.series(x, x0, n_terms).removeO()
    return series

