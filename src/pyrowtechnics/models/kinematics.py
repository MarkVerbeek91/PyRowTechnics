from pydy.system import System
from sympy import Matrix, simplify, solve, symbols
from sympy.physics.mechanics import (
    Body,
    JointsMethod,
    KanesMethod,
    PinJoint,
    ReferenceFrame,
    dynamicsymbols,
    inertia,
    mechanics_printing,
)

mechanics_printing(pretty_print=False)
q1, q2, q3, u1, u2, u3 = dynamicsymbols("q1:4, u1:4")
l1, l2, l3, l4, rho = symbols("l1:5, rho")

N = ReferenceFrame("N")
inertias = [inertia(N, 0, 0, rho * line**3 / 12) for line in (l1, l2, l3, l4)]
link1 = Body("Link1", frame=N, mass=rho * l1, central_inertia=inertias[0])
link2 = Body("Link2", mass=rho * l2, central_inertia=inertias[1])
link3 = Body("Link3", mass=rho * l3, central_inertia=inertias[2])
link4 = Body("Link4", mass=rho * l4, central_inertia=inertias[3])

joint1 = PinJoint(
    "J1",
    link1,
    link2,
    coordinates=q1,
    speeds=u1,
    parent_point=l1 / 2 * link1.x,
    child_point=-l2 / 2 * link2.x,
    joint_axis=link1.z,
)
joint2 = PinJoint(
    "J2",
    link2,
    link3,
    coordinates=q2,
    speeds=u2,
    parent_point=l2 / 2 * link2.x,
    child_point=-l3 / 2 * link3.x,
    joint_axis=link2.z,
)
joint3 = PinJoint(
    "J3",
    link3,
    link4,
    coordinates=q3,
    speeds=u3,
    parent_point=l3 / 2 * link3.x,
    child_point=-l4 / 2 * link4.x,
    joint_axis=link3.z,
)

loop = link4.masscenter.pos_from(link1.masscenter) + l1 / 2 * link1.x + l4 / 2 * link4.x
fh = Matrix([loop.dot(link1.x), loop.dot(link1.y)])

method = JointsMethod(link1, joint1, joint2, joint3)
t = dynamicsymbols._t
qdots = solve(method.kdes, [q1.diff(t), q2.diff(t), q3.diff(t)])
fhd = fh.diff(t).subs(qdots)

method._method = KanesMethod(
    method.frame,
    q_ind=[q1],
    u_ind=[u1],
    q_dependent=[q2, q3],
    u_dependent=[u2, u3],
    kd_eqs=method.kdes,
    configuration_constraints=fh,
    velocity_constraints=fhd,
    forcelist=method.loads,
    bodies=method.bodies,
)
simplify(method.method._form_eoms())

sys = System(method)

if __name__ == "__main__":
    pass
