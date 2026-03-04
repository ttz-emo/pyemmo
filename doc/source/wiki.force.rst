.. _section-wiki-force:

Force Calculation
=================


Force Computation by Maxwell Stress Tensor
------------------------------------------

Calculation of the foce density using the Maxwell Stress Tensor (MST) :math:`\sigma`.
See e.g. `Nicola Bianchi "Electrical Machine Analysis Using Finite Elements" <https://doi.org/10.1201/9781315219295>`_ or `Wikipedia <https://en.wikipedia.org/wiki/Maxwell_stress_tensor>`_ for a detailed explaination of the matter.
In physics, the Maxwell Stress Tensor is the stress tensor of an electromagnetic field.
For **low frequency** (magnetostatic) electromagnetic simulations the MST only contains the magnetic components.
The individual components :math:`i,j` (dimensions of the room, in cartesian coordinates e.g. :math:`x,y`) of that 3x3 tensor can be expressed by:

.. math::

   \sigma_{i,j} = \frac{1}{\mu_0} ( B_{i}B_{j} - \frac{1}{2} \delta_{i,j} B^2)

.. math:
..    \sigma = \vec{H}\cdot(\vec{B}\cdot\vec{n}) - \frac{1}{2\mu_0}\vec{n}\cdot(\vec{B}\cdot\vec{H})

where:

    - :math:`\vec{H}` is the magnetic field strength in A/m.
    - :math:`\vec{B}` is the magnetic flux density in T.
    - :math:`\vec{n}` is the normal vector on the plane.
    - :math:`\mu_0` is the permeability of the vacuum.
    - :math:`\delta_{i,j}` is the `Kronecker delta <https://en.wikipedia.org/wiki/Kronecker_delta>`_ which is:

        .. math::

            \delta_{ij} =
            \begin{cases}
            1 & \text{if } i=j \\
            0 & \text{if } i \ne j
            \end{cases}

So the second term in the equation will only be present for the main diagonal.

The implementation as GetDP PostProcessing quantity looks like this:

.. code-block:: c

    Function{
        ...
        T_max[] = ( SquDyadicProduct[$1] - SquNorm[$1] * TensorDiag[0.5, 0.5, 0.5] ) / mu0;
        ...
    }
    ...
    {
        Name Force_MST;
        Value{
            Term{
                [ T_max[{Curl a}] * XYZ[] ];
                In Region[{Rotor_Airgap, Stator_Airgap}];
                Jacobian Vol;
            }
        }
    }

It first defines a general function ``T_max`` for the MST.
The ``SquDyadicProduct`` is the squared `dyadic product <https://en.wikipedia.org/wiki/Dyadic_product>`_ of the given vector and ``SquNorm`` is the squared norm of the vector.
This function is used in the PostProcessing quantity ``Force_MST`` with the input of ``{Curl a}`` which is the magnetic flux density (:math:`\vec{B} = \mathrm{rot}(\vec{A})`).
Multiplying this with the position vector ``XYZ[]`` of the current element/node results in the force density vector at that position in cartesian coordinates.
Note that the quantity is only defined in the regions ``Rotor_Airgap`` and ``Stator_Airgap`` since we can assume :math:`\mu_r=1` their and airgap force density is typically of interest in electrical machine analysis.

Additionally to this general evaluation there are the following depended PostProcessing definitions:

    - ``Force_MST_Cyl``: Transforms the cartesian force density to cylindrical coordinates.
    - ``Force_MST_Rad``: Computes the radial component of the force density vector.
    - ``Force_MST_Tan``: Computes the tangential component of the force density vector.

Force Computation by Virtual Works Method
-----------------------------------------

Using **Virtual Work** method allows to calculate the total net force on a surface of curve by the variation of the coenergy :math:`\delta W'`.

.. code-block:: c

    {
        Name Force_vw ;
        Value {
            Integral {
                Type Global;
                [ 0.5 * nu[] * VirtualWork [{d a}] * axialLength[] ];
                In ElementsOf[Rotor_Airgap, OnOneSideOf Rotor_Bnd_MB];
                Jacobian Vol;
                Integration I1;
            }
        }
    }
