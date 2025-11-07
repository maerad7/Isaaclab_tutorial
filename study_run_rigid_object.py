import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Tutorial on spawning and interacting with a rigid object. ")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import torch

import isaacsim.core.utils.prims as prim_utils
import isaaclab.sim as sim_utils
import isaaclab.utils.math as math_utils
from isaaclab.assets import RigidObject, RigidObjectCfg
from isaaclab.sim import SimulationContext

def design_scene():
    # Ground_plane
    cfg = sim_utils.GroundPlaneCfg()
    cfg.func("/World/defaultGroundPlane", cfg)
    
    #Light
    cfg = sim_utils.DomeLightCfg(intensity=2000.0, color=(0.8, 0.8, 0.8))
    cfg.func("/World/Light",cfg)

    # Create sperate Group
    # 각 그룹마다 로봇 
    origins = [[0.25, 0.25, 0.0], [-0.25, 0.25, 0.0], [0.25, -0.25, 0.0], [-0.25, -0.25, 0.0]]
    for i, origin in enumerate(origins):
        prim_utils.create_prim(f"/World/Origin{i}", "Xform", translation=origin)

    # Rigid Object
    """
    spawn 파라미터는 객체의 물리적 특성을 정의하는 설정을 포함한다.
    radius: 원뿔의 반지름
    height: 원뿔의 높이
    rigid_props: 강체 물리 속성
    mass_props: 질량 속성
    collision_props: 충돌 속성
    visual_material: 시각적 재료 속성
    init_state: 초기 상태 설정
    """
    cone_cfg = RigidObjectCfg(
        prim_path="/World/Origin.*/Cone",
        spawn=sim_utils.ConeCfg(
            radius=0.1,
            height=0.2,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0), metallic=0.2),
        ),
        init_state = RigidObjectCfg.InitialStateCfg(),
    )

    cone_object = RigidObject(cfg=cone_cfg)


    # return the scene information
    scene_entities = {"cone": cone_object}
    return scene_entities, origins

def run_simulator(sim, entities, origins):
    """Runs the simulation loop."""
    # Extract scene entities

    #참고: 여기서는 가독성을 위해 이렇게 작성했지만, 일반적으로 엔티티를 딕셔너리에서 직접 접근하는 것이 더 좋습니다.
    #   이 딕셔너리는 다음 튜토리얼에서 InteractiveScene 클래스로 대체됩니다.

    cone_object = entities["cone"]
    
    # 시뮬레이션 단계 정의
    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0

    # Simulate physics
    while simulation_app.is_running():
        # reset
        if count % 250 == 0:
            # reset counters
            sim_time = 0.0
            count = 0
            # reset root state
            # 이것은 원뿔 객체의 기본 루트 상태를 복제하고,
            # origins(환경의 원점 위치)를 기준으로 원기둥 표면상 임의의 위치를 샘플링하여 위치를 지정하는 코드입니다.
            # 즉, 원뿔을 환경 내 무작위 원기둥 주변에 재배치하게 해줍니다.
            root_state = cone_object.data.default_root_state.clone()
            root_state[:, :3] += origins
            root_state[:, :3] += math_utils.sample_cylinder(
                radius=0.1, h_range=(0.25, 0.5), size=cone_object.num_instances, device=cone_object.device
            )

            # write root state to simulation
            # 루트 상태(root_state)의 각 인스턴스는 13개의 값을 가집니다.
            # 앞의 7개 값: [위치(x, y, z), 쿼터니언(qx, qy, qz, qw)] → 포즈(자세)
            # 뒤의 6개 값: [선속도(vx, vy, vz), 각속도(wx, wy, wz)] → 속도
            # 따라서 [:, :7]이 포즈, [:, 7:]이 속도를 의미합니다.
            cone_object.write_root_pose_to_sim(root_state[:, :7])
            cone_object.write_root_velocity_to_sim(root_state[:, 7:])

        # apply sim data
        cone_object.write_data_to_sim()
        # perform step
        sim.step()
        # update sim-time
        sim_time += sim_dt
        count += 1
        # update buffers
        cone_object.update(sim_dt)
        # print the root position
        if count % 50 == 0:
            print(f"Root position (in world): {cone_object.data.root_pos_w}")

def main():
    """Main function."""
    # 시뮬레이션 설정을 생성하고 시뮬레이션 컨텍스트(엔진)를 초기화합니다.
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = SimulationContext(sim_cfg)

    sim.set_camera_view(eye=[1.5, 0.0, 1.0], target=[0.0, 0.0, 0.0])
    # Design scene
    scene_entities, scene_origins = design_scene()
    scene_origins = torch.tensor(scene_origins, device=sim.device)

    # Play the simulator
    sim.reset()

    # Now we are ready!
    print("[INFO]: Setup complete...")
    # Run the simulator
    run_simulator(sim, scene_entities, scene_origins)

if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()