=======
Domains
=======

.. module:: sympy.domains

Here we document the various implemented ground domains.  There are
three types: abstract domains, concrete domains, and "implementation
domains".  Abstract domains cannot be (usefully) instantiated at all,
and just collect together functionality shared by many other domains.
Concrete domains are those meant to be instantiated and used.  In some
cases, there are various possible ways to implement the data type the
domain provides.  For example, depending on what libraries are
available on the system, the integers are implemented either using the
python built-in integers, or using gmpy.  Note that various aliases
are created automatically depending on the libraries available.  As
such e.g. ``ZZ`` always refers to the most efficient implementation of
the integer ring available.

Abstract Domains
****************

.. autoclass:: sympy.domains.domain.Domain
   :members:

.. autoclass:: sympy.domains.field.Field
   :members:

.. autoclass:: sympy.domains.ring.Ring
   :members:

.. autoclass:: sympy.domains.simpledomain.SimpleDomain
   :members:

.. autoclass:: sympy.domains.compositedomain.CompositeDomain
   :members:

.. autoclass:: sympy.domains.characteristiczero.CharacteristicZero
   :members:

Concrete Domains
****************

.. autoclass:: FiniteRing
   :members:

.. autoclass:: FiniteField
   :members:

.. autoclass:: IntegerRing
   :members:

.. autoclass:: RationalField
   :members:

.. autoclass:: AlgebraicField
   :members:

.. autoclass:: RealAlgebraicField
   :members:

.. autoclass:: ComplexAlgebraicField
   :members:

.. autoclass:: sympy.polys.rings.PolynomialRing
   :members:

.. autoclass:: sympy.polys.univar.UnivarPolynomialRing
   :members:

.. autoclass:: sympy.polys.fields.FractionField
   :members:

.. autoclass:: RealField
   :members:

.. autoclass:: ComplexField
   :members:

.. autoclass:: ExpressionDomain
   :members:

Implementation Domains
**********************

.. autoclass:: sympy.domains.finitefield.PythonFiniteField
.. autoclass:: sympy.domains.finitefield.GMPYFiniteField

.. autoclass:: sympy.domains.integerring.PythonIntegerRing
.. autoclass:: sympy.domains.integerring.GMPYIntegerRing

.. autoclass:: sympy.domains.rationalfield.PythonRationalField
.. autoclass:: sympy.domains.rationalfield.GMPYRationalField

Domain Elements
***************

.. autoclass:: sympy.domains.finitefield.ModularInteger
   :members:

.. autoclass:: sympy.domains.finitefield.GaloisFieldElement
   :members:
