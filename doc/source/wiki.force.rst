.. _section-wiki-force:

Force Calculation
=================


Force Computation by Maxwell Stress Tensor
------------------------------------------

Calculation of the foce density using the Maxwell Stress Tensor (MST) :math:`\sigma`.
See e.g. `Nicola Bianchi "Electrical Machine Analysis Using Finite Elements" <https://doi.org/10.1201/9781315219295>`_ or `Wikipedia <https://en.wikipedia.org/wiki/Maxwell_stress_tensor>`_ for a detailed explaination of the matter.
In physics, the Maxwell Stress Tensor is the stress tensor of an electromagnetic field.
For **low frequency** (magnetostatic) electromagnetic simulations the MST only contains the magnetic components.
The individual components :math:`i,j` (dimensions of the room, in cartesian coordinates e.g. :math:`x,y,z`) of that 3x3 tensor can be expressed by:

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
                [ T_max[{Curl a}] * Unit[XYZ[]] ];
                In Region[{Rotor_Airgap, Stator_Airgap}];
                Jacobian Vol;
            }
        }
    }

It first defines a general function ``T_max`` for the MST.
The ``SquDyadicProduct`` is the squared `dyadic product <https://en.wikipedia.org/wiki/Dyadic_product>`_ of the given vector and ``SquNorm`` is the squared norm of the vector.
This function is used in the PostProcessing quantity ``Force_MST`` with the input of ``{Curl a}`` which is the magnetic flux density (:math:`\vec{B} = \mathrm{rot}(\vec{A})`).
Multiplying this with the unity vector normal to the cylindrical airgap surface/curve ``Unit[XYZ[]]`` results in the force density vector at that position in cartesian coordinates.
Note that the quantity is only defined in the regions ``Rotor_Airgap`` and ``Stator_Airgap`` since we can assume :math:`\mu_r=1` their and airgap force density is typically of interest in electrical machine analysis.

Additionally to this general evaluation there are the following depended PostProcessing definitions:

    - ``Force_MST_Cyl``: Transforms the cartesian force density to cylindrical coordinates.
    - ``Force_MST_Rad``: Computes the radial component of the force density vector.
    - ``Force_MST_Tan``: Computes the tangential component of the force density vector.

In the literature regarding electrical machines one often finds the definition of the MST in cylindrical coordinates.
But it can be shown, that the cartesian and cylindrical implementation of the tensor result in the same force density results.

We would assume :math:`\sigma_\mathrm{rad,tan} = \mathrm{cart2cyl}(\sigma_{x,y})`. Therefore we compare the results of

.. math::

    \sigma_\mathrm{rad,cyl} = \frac{1}{2 \mu_0} (B_\mathrm{rad}^2 - B_\mathrm{tan}^2)\\


with the radial component of the cartesian force density vector result

.. math::
    \sigma_\mathrm{rad,cart} = \sigma_\mathrm{x,y} \cdot \vec{n}_\mathrm{r}\\

Note that the radial component of a vector (:math:`\sigma_\mathrm{x,y}`) in cartesian coordintates is the scalar product of that vector with the unit vector in radial direction.
In GetDP the PostProcessing for these quantities looks like

.. code-block:: c

    ...
    Name MagStaDyn_a_2D; NameOfFormulation MagStaDyn_a_2D; NameOfSystem A;
    PostQuantity {
        {
            Name Force_MST_Rad_Cart;
            Value{
                Term{
                    [ CompRad[T_max[{Curl a}] * Unit[XYZ[]]] ];
                    In Region[{Rotor_Airgap, Stator_Airgap}];
                    Jacobian Vol;
                }
            }
        }
        {
            Name Force_MST_Rad_Cyl;
            Value{
                Term{
                    [ 0.5/mu0 *(CompRad[{Curl a}]^2 - CompTan[{Curl a}]^2) ];
                    In Region[{Rotor_Airgap, Stator_Airgap}];
                    Jacobian Vol;
                }
    ...

where
:code:`CompRad[] = $1 * Vector[ Cos[AngularPosition[]#4], Sin[#4], 0.];`
and
:code:`CompTan[] = $1 * Vector[-Sin[AngularPosition[]#4], Cos[#4], 0.];`.

The results of a test simulation show that both approaches give the same results while the deviation is on the order of the numerical accuracy:

.. figure:: ../images/force/comp_F_rad.png
   :align: center

   Comparison of radial force density derived from different MST formulations.

The same thing is true for the tangential component:

.. figure:: ../images/force/comp_F_tan.png
   :align: center

    Comparison of tangential force density derived from different MST formulations.
|

Force Computation by Virtual Works Method
-----------------------------------------

Using **Virtual Work** method allows to calculate the total net force on a volume by the variation of the coenergy :math:`\delta W'`.
You can find the implementation for the Virtual Work method in Getdp `here <https://gitlab.onelab.info/getdp/getdp/-/blob/master/src/functions/F_Misc.cpp?ref_type=heads#L327>`_.

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
