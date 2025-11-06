import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(
    description="This script demonstrates adding a custom robot to an Isaac Lab environment."
)
parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to spawn.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import numpy as np
import torch

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import AssetBaseCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR


"""
spawn 파라미터
spawn 파라미터를 사용하면, 시뮬레이션에서 사용할 로봇의 USD asset을 지정할 수 있습니다.

actuators 파라미터
actuators 파라미터는 액추에이터 설정 딕셔너리를 정의합니다.
"""
JETBOT_CONFIG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(usd_path=f"{ISAAC_NUCLEUS_DIR}/Robots/NVIDIA/Jetbot/jetbot.usd"),
    actuators={"wheel_acts": ImplicitActuatorCfg(joint_names_expr=[".*"], damping=None, stiffness=None)},
)
"""
 물리 속성 설정(physics properties) 과 로봇의 초기 상태(init_state) 설정 추가가
"""

"""
        rigid_props 파라미터
        로봇이 시뮬레이션에서 '물리적 객체'로서 어떻게 작동할지를 정의하는 RigidBodyPropertiesCfg 객체를 받아 그 속성을 정의합니다.

        articulation_props 파라미터
        로봇의 계층 구조(articulation)와 관련된 속성을 정의하는 ArticulationRootPropertiesCfg 객체를 받아 그 속성을 정의합니다.

        init_state 파라미터
        로봇의 초기 상태를 정의하는 InitialStateCfg 객체를 받아 그 속성을 정의합니다.

        joint_pos 파라미터
        로봇의 각 조인트의 초기 위치를 정의하는 딕셔너리를 받아 그 속성을 정의합니다.
        USD에서 정의된 조인트 이름을 Key로, 해당 조인트의 위치를 float 값으로 갖는 딕셔너리입니다

        pos 파라미터
        로봇이 배치될 초기 위치이며, 이는 월드 좌표계가 아니라 environment 좌표계 기준입니다.
        예를 들어, (0.25, -0.25, 0.0)으로 설정하면 environment의 원점에서 해당 위치만큼 오프셋된 지점에 로봇이 생성됩니다.  
"""
DOFBOT_CONFIG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAAC_NUCLEUS_DIR}/Robots/Yahboom/Dofbot/dofbot.usd",
       
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=0
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "joint1": 0.0,
            "joint2": 0.0,
            "joint3": 0.0,
            "joint4": 0.0,
        },
        pos=(0.25, -0.25, 0.0),
    ),
    actuators={
        "front_joints": ImplicitActuatorCfg(
            joint_names_expr=["joint[1-2]"],
            effort_limit_sim=100.0,
            velocity_limit_sim=100.0,
            stiffness=10000.0,
            damping=100.0,
        ),
        "joint3_act": ImplicitActuatorCfg(
            joint_names_expr=["joint3"],
            effort_limit_sim=100.0,
            velocity_limit_sim=100.0,
            stiffness=10000.0,
            damping=100.0,
        ),
        "joint4_act": ImplicitActuatorCfg(
            joint_names_expr=["joint4"],
            effort_limit_sim=100.0,
            velocity_limit_sim=100.0,
            stiffness=10000.0,
            damping=100.0,
        ),
    },
)