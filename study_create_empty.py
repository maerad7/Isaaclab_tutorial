import argparse

from isaaclab.app import AppLauncher
"""
isaaclab.app의 AppLauncher 클래스는 어플리케이션 실행
AppLauncher.add_app_launcher_args(parser)를 호출하면 애플리케이션 실행에 필요한 기본적인 CLI 인자가 parser에 추가
AppLauncher(args_cli)를 호출하면 애플리케이션 실행 객체가 생성
app_launcher.app을 통해 시뮬레이션 애플리케이션 객체(simulation_app)를 가져올 수 있다
"""
# create argparser
parser = argparse.ArgumentParser(description="Tutorial on creating an empty stage.")
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()
# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

from isaaclab.sim import SimulationCfg, SimulationContext
"""
isaaclab.sim: 시뮬레이터와 관련된 모든 핵심 작업을 위한 Isaac Lab의 하위 패키
"""

def main():
    """독립 실행형 스크립트에서 시뮬레이션을 시작할 때 sim.SimulationContext 클래스를 통해 시뮬레이터 재생,
     일시 정지 및 단계별 실행 제어뿐만 아니라 다양한 타임라인 이벤트 처리 및 물리 장면 구성을 수행할 수 있다"""

    # Initialize the simulation context
    sim_cfg = SimulationCfg(dt=0.01)
    sim = SimulationContext(sim_cfg)
    # Set main camera
    sim.set_camera_view([2.5, 2.5, 2.5], [0.0, 0.0, 0.0])
    """
    시뮬레이션 컨텍스트를 생성한 후, 시뮬레이션된 장면에서 작동하는 물리 엔진(physics)만 설정한다
    """
    # Play the simulator
    sim.reset()
    """
    이 메서드는 타임라인을 시작하고, 시뮬레이터에서 물리 핸들(physics handles)을 초기화하는 역할을 한다. 
    시뮬레이션을 실행하기 전에 반드시 처음에 호출해야 하며, 그렇지 않으면 시뮬레이션 핸들이 올바르게 초기화되지 않는다
    """
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
