from .infrast_sim import Simulator


class SimulatorOperator:

    def __init__(self, simulator: Simulator, name: str):
        self.simulator = simulator
        self.name = name

    @property
    def status(self) -> dict:
        return self.simulator.get_mowerdata()['operators']['name']

    @property
    def current_mood(self):
        return self.status['morale']

    def is_resting(self):
        return not (5 <= self.status['facility-index'] <= 8)


