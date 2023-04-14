# default position is at the catch
from math import cos, pi, sin, sqrt

from matplotlib import pyplot as plt

LOWER_LEG_LENGTH = 0.5  # meter
UPPER_LEG_LENGTH = 0.45  # meter
BODY_LENGTH = 0.55  # meter
UPPER_ARM_LENGTH = 0.4  # meter
LOWER_ARM_LENGTH = 0.3  # meter

heel = [0, 0]
lower_leg = [LOWER_LEG_LENGTH, 0]
upper_leg = [UPPER_LEG_LENGTH, 0]
body = [BODY_LENGTH, 0]
upper_arm = [UPPER_ARM_LENGTH, 0]
lower_arm = [LOWER_ARM_LENGTH, 0]


class Rower:
    body_parts = [
        heel,
        lower_leg,
        upper_leg,
        body,
        upper_arm,
        lower_arm,
    ]

    def __iter__(self):
        for part in self.body_parts:
            yield part

    def get_xs(self):
        xs = [p[0] for p in iter(self)]
        return [sum(xs[: i + 1]) for i in range(len(xs))]

    def get_ys(self):
        ys = [p[1] for p in iter(self)]
        return [sum(ys[: i + 1]) for i in range(len(ys))]

    @staticmethod
    def rotate(vector, angle):
        length = sqrt(pow(vector[0], 2) + pow(vector[1], 2))
        return [length * cos(angle), length * sin(angle)]

    def pose(self, angles):
        for i, (vector, angle) in enumerate(zip(self.body_parts[1:], angles)):
            self.body_parts[i + 1] = self.rotate(vector, angle)


rower = Rower()

catch_angles = [pi / 2, -pi / 3, pi / 2, pi / 4, 0]  # noqa

# rower.pose([0]*6)
# rower.pose(catch_angles)
x_data, y_data = rower.get_xs(), rower.get_ys()

assert x_data[-1] == 2.2

# rotated_leg = rower.rotate(upper_leg, 0)
# x_data = [heel_position[0], lower_leg[0], rotated_leg[0]]
# y_data = [heel_position[1], lower_leg[1], rotated_leg[1]]

plt.plot(x_data, y_data, "o-")
plt.show()

# handle_position = sum()
