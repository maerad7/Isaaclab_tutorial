"""
1. Primitive (Prim): USD 장면의 기본 구성 요소로 장면 그래프의 노드(node)라고 볼 수 있다. 각 노드는 메시(mesh),
 광원(light), 카메라(camera) 또는 변환(transform)일 수 있다.

2.Attribute: Prim이 가지는 속성(attribute)으로 키-값(key-value) 쌍의 형태를 띤다. 예를 들어, 특정 prim이 
color라는 속성을 가지며, 그 값이 red일 수도 있다.

3.Relationship: Prim 간의 연결을 나타낸다. 이는 다른 prim을 참조하는 포인터와 같은 개념으로, 예를 들어 
메시(mesh) prim이 shading을 위한 material prim과 관계를 가질 수 있다.

4.Stage: 프리미티브(prim)와 속성(attribute) 및 관계(relationship)의 모음을 USD 스테이지(stage)라고 한다. 
이는 장면의 모든 prim을 위한 컨테이너로 생각할 수 있다. 즉, USD 스테이지는 장면을 구성하는 모든 prim을 
관리하는 공간이며, 장면을 디자인한다는 것은 곧 USD stage를 구성하는 것과 같다.
"""

import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Tutorial on spawning prims into the scene.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import isaacsim.core.utils.prims as prim_utils
import isaaclab.sim as sim_utils
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

def design_scene():
    """
    지면 평면 생성: GroundPlaneCfg 모양과 크기 등의 변경 가능한 속성을 갖는 격자 모양의 접지면을 구성한다.
    """
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)
    """
    조명 생성: 장면에 조명 설정을 불러온다. 여기에는 원거리 조명(distant
    lights), 구형 조명(sphere lights), 디스크 조명(disk lights), 원통형 조명(cylinder lights)이 포함된다.
    """
    cfg_light_distant = sim_utils.DistantLightCfg(
        intensity=3000.0,
        color=(0.75, 0.75, 0.75),
    )
    cfg_light_distant.func("/World/lightDistant", cfg_light_distant, translation=(1, 0, 10))
    """
    Xform은 변환(transformation) 속성만 포함하는 기본 요소(primitive)로 다른 prim을 그 아래에 그룹화(parent-child 관계)하고
    그룹 전체를 변형하는 데 사용된다. 아래는 Xform Prim을 생성하여 하위에 있는 모든 기본 형상을 그룹화하는 예제
    """
    prim_utils.create_prim("/World/Objects", "Xform")
    """
    빨간 원뿔 생성: ConeCfg 모양과 크기 등의 변경 가능한 속성을 갖는 빨간 원뿔을 구성한다.
    """
    cfg_cone = sim_utils.ConeCfg(
        radius=0.15,
        height=0.5,
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),
    )
    cfg_cone.func("/World/Objects/Cone1", cfg_cone, translation=(-1.0, 1.0, 1.0))
    cfg_cone.func("/World/Objects/Cone2", cfg_cone, translation=(-1.0, -1.0, 1.0))
    """
    녹색 원뿔 생성: ConeCfg 모양과 크기 등의 변경 가능한 속성을 갖는 녹색 원뿔을 구성한다. 
    이 원뿔은 충돌(collider)과 관성(rigid body)을 가지며, 물리 엔진에서 충돌 감지와 동적 행동을 포함한다.
    """
    cfg_cone_rigid = sim_utils.ConeCfg(
        radius=0.15,
        height=0.5,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(), #강체 물리(Rigid body physics)를 추가
        mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
        collision_props=sim_utils.CollisionPropertiesCfg(),
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0)),
    )
    cfg_cone_rigid.func("/World/Objects/ConeRigid", cfg_cone_rigid, translation=(-0.2, 0.0, 2.0), orientation=(0.5, 0.0, 0.5, 0.0))
    """
    파란 사각형 생성: MeshCuboidCfg 모양과 크기 등의 변경 가능한 속성을 갖는 파란 사각형을 구성한다.
    이 사각형은 변형 가능한 물리(deformable body)를 가지며, 물리 엔진에서의의 변형 감지가 포함한다.
    """
    cfg_cuboid_deformable = sim_utils.MeshCuboidCfg(
        size=(0.2, 0.5, 0.2),
        deformable_props=sim_utils.DeformableBodyPropertiesCfg(),
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 0.0, 1.0)),
        physics_material=sim_utils.DeformableBodyMaterialCfg(),
    )
    cfg_cuboid_deformable.func("/World/Objects/CuboidDeformable", cfg_cuboid_deformable, translation=(0.15, 0.0, 2.0))
    """
    USD 파일에서 테이블 생성: UsdFileCfg를 사용하여 특정 USD 파일(table_instanceable.usd)을 장면에 불러온다.
    이 파일은 테이블의 인스턴스(instance)를 생성하는 데 사용된다.테이블은 mesh primitive이며, 연관된 material primitive가 있다. 
    이 모든 정보는 USD 파일에 저장되어 있다
    """
    cfg = sim_utils.UsdFileCfg(usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Mounts/SeattleLabTable/table_instanceable.usd")
    cfg.func("/World/Objects/Table", cfg, translation=(0.0, 0.0, 1.05))


def main():
    """Main function."""
    sim_cfg = sim_utils.SimulationCfg(dt=0.01, device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)
    # Set main camera
    sim.set_camera_view([2.0, 0.0, 2.5], [-0.5, 0.0, 0.5])
    # Design scene
    design_scene()
    # Play the simulator
    sim.reset()
    # Now we are ready!
    print("[INFO]: Setup complete...")

    # Simulate physics
    while simulation_app.is_running():
        # perform step
        sim.step()


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
    # Initialize the simulation context