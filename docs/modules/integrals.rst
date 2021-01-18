Integrals
=========

.. module:: sympy.integrals

The ``integrals`` module in Diofant implements methods to calculate definite and indefinite integrals of expressions.

Principal method in this module is :func:`~sympy.integrals.integrals.integrate`

  - ``integrate(f, x)`` returns the indefinite integral `\int f\,dx`
  - ``integrate(f, (x, a, b))`` returns the definite integral `\int_{a}^{b} f\,dx`

Examples
--------
Diofant can integrate a vast array of functions. It can integrate polynomial functions::

    >>> init_printing(pretty_print=True, use_unicode=False,
    ...               wrap_line=False, no_global=True)
    >>> integrate(x**2 + x + 1, x)
     3    2
    x    x
    -- + -- + x
    3    2

Rational functions::

	>>> integrate(x/(x**2+2*x+1), x)
	               1
	log(x + 1) + -----
	             x + 1


Exponential-polynomial functions. These multiplicative combinations of polynomials and the functions ``exp``, ``cos`` and ``sin`` can be integrated by hand using repeated integration by parts, which is an extremely tedious process. Happily, Diofant will deal with these integrals.

::

    >>> integrate(x**2 * exp(x) * cos(x), x)
     x  2           x  2                         x           x
    E *x *sin(x)   E *x *cos(x)    x            E *sin(x)   E *cos(x)
    ------------ + ------------ - E *x*sin(x) + --------- - ---------
         2              2                           2           2


even a few nonelementary integrals (in particular, some integrals involving the error function) can be evaluated::

	>>> integrate(exp(-x**2)*erf(x), x)
	  ____    2
	\/ pi *erf (x)
	--------------
	      4


Integral Transforms
-------------------

.. module:: sympy.integrals.transforms

Diofant has special support for definite integrals, and integral transforms.

.. autofunction:: mellin_transform
.. autofunction:: inverse_mellin_transform
.. autofunction:: laplace_transform
.. autofunction:: inverse_laplace_transform
.. autofunction:: fourier_transform
.. autofunction:: inverse_fourier_transform
.. autofunction:: sine_transform
.. autofunction:: inverse_sine_transform
.. autofunction:: cosine_transform
.. autofunction:: inverse_cosine_transform
.. autofunction:: hankel_transform
.. autofunction:: inverse_hankel_transform


Internals
---------

There is a general method for calculating antiderivatives of elementary functions, called the *Risch algorithm*. The Risch algorithm is a decision procedure that can determine whether an elementary solution exists, and in that case calculate it. It can be extended to handle many nonelementary functions in addition to the elementary ones.

Diofant currently uses a simplified version of the Risch algorithm, called the *Risch-Norman algorithm*. This algorithm is much faster, but may fail to find an antiderivative, although it is still very powerful. Diofant also uses pattern matching and heuristics to speed up evaluation of some types of integrals, e.g. polynomials.

For non-elementary definite integrals, Diofant uses so-called Meijer G-functions.
Details are described :ref:`here <meijerg-label>`.

API reference
-------------

.. autofunction:: sympy.integrals.integrals.integrate
.. autofunction:: sympy.integrals.integrals.line_integrate
.. autofunction:: sympy.integrals.deltafunctions.deltaintegrate
.. autofunction:: sympy.integrals.rationaltools.ratint
.. autofunction:: sympy.integrals.rationaltools.ratint_logpart
.. autofunction:: sympy.integrals.rationaltools.ratint_ratpart
.. autofunction:: sympy.integrals.heurisch.components
.. autofunction:: sympy.integrals.heurisch.heurisch
.. autofunction:: sympy.integrals.heurisch.heurisch_wrapper
.. autofunction:: sympy.integrals.trigonometry.trigintegrate

The class `Integral` represents an unevaluated integral and has some methods that help in the integration of an expression.

.. autoclass:: sympy.integrals.integrals.Integral
   :members:

   .. data:: is_commutative

      Returns whether all the free symbols in the integral are commutative.

.. autoclass:: sympy.integrals.transforms.IntegralTransform
   :members:

.. autoclass:: sympy.integrals.transforms.MellinTransform
   :members:

.. autoclass:: sympy.integrals.transforms.InverseMellinTransform
   :members:

.. autoclass:: sympy.integrals.transforms.LaplaceTransform
   :members:

.. autoclass:: sympy.integrals.transforms.InverseLaplaceTransform
   :members:

.. autoclass:: sympy.integrals.transforms.FourierTransform
   :members:

.. autoclass:: sympy.integrals.transforms.InverseFourierTransform
   :members:

.. autoclass:: sympy.integrals.transforms.SineTransform
   :members:

.. autoclass:: sympy.integrals.transforms.InverseSineTransform
   :members:

.. autoclass:: sympy.integrals.transforms.CosineTransform
   :members:

.. autoclass:: sympy.integrals.transforms.InverseCosineTransform
   :members:

.. autoclass:: sympy.integrals.transforms.HankelTransform
   :members:

.. autoclass:: sympy.integrals.transforms.InverseHankelTransform
   :members:

Numeric Integrals
-----------------

Diofant has functions to calculate points and weights for Gaussian quadrature of
any order and any precision:

.. module:: sympy.integrals.quadrature

.. autofunction:: gauss_legendre

.. autofunction:: gauss_laguerre

.. autofunction:: gauss_hermite

.. autofunction:: gauss_gen_laguerre

.. autofunction:: gauss_chebyshev_t

.. autofunction:: gauss_chebyshev_u

.. autofunction:: gauss_jacobi
