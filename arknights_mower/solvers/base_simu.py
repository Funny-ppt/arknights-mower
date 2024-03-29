from .base_schedule import BaseSchedulerSolver
from .fake_solver import FakeSolver
from ..utils.device.fake_device import FakeDevice
from ..utils.fake_recognize import FakeRecognizer
from ..utils.infrast_sim import Simulator
from math import ceil


class SimulatorSolver(FakeSolver, BaseSchedulerSolver):
    def __init__(self):
        """ 在调用之前请确保 InfrastSim 已经初始化 """

        # device and recog should never be called
        BaseSchedulerSolver.__init__(self, FakeDevice(), FakeRecognizer())

        self.simulator = Simulator()
        self.scripts = ''
        self.last_script = None

    def execute_script(self, script: str):
        self.scripts += script + '\n'
        self.last_script = script
        self.simulator.execute_script(script)

    def sleep(self, interval: float = 1, rebuild: bool = True) -> None:
        interval = ceil(interval)
        if interval > 0:
            self.execute_script(f'simulate {interval}')