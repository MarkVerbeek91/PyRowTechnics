from enum import Enum
from math import pi
from types import SimpleNamespace
from typing import Any

import pytest

from pyrowtechnics.models.geometry_only import Rower  # noqa


class BodyParts(Enum):
    lower_leg = 0
    upper_leg = 1
    body = 2
    upper_arm = 3
    lower_arm = 4


def test_body_part_enum__number_of_limbs__equals_5():
    assert len(BodyParts) == 5


class JointNames(Enum):
    knee = 0
    hip = 1
    shoulder = 2
    elbow = 3


def test_joints_enum__number_of_joints__equals_4():
    assert len(JointNames) == 4


class Pose(SimpleNamespace):
    def __init__(self, **kwargs: Any):
        angles = kwargs.pop("angles", [0] * len(JointNames))
        pose = dict(map(lambda x: (str(x[0]), x[1]), zip(JointNames, angles)))
        super().__init__(**pose)


@pytest.mark.parametrize("joint", JointNames)
def test_pose__by_default__all_joint_zero(joint):
    assert getattr(Pose(), str(joint)) == 0


DEGREE90 = pi / 2


@pytest.mark.parametrize("joint", JointNames)
def test_pose__set_joints_all_90d__all_joint_90d(joint):
    assert getattr(Pose(angles=[DEGREE90] * 4), str(joint)) == DEGREE90


class RowerClass:
    def __init__(self, start_pose):
        self.start_pose = start_pose


def test_rower__in_flat_pose__hand_at_max_x_distance():
    assert RowerClass(Pose())
