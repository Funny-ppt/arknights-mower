import typing
from abc import abstractmethod

from ..utils import typealias as tp
from ..utils.log import logger


class FakeSolver:
    """ a solver that always ignore operate requests """
    def __init__(self) -> None:
        pass

    def transition(self) -> bool:
        return True

    def get_color(self, pos: tp.Coordinate) -> tp.Pixel:
        return 0, 0, 0

    def get_pos(self, poly: tp.Location, x_rate: float = 0.5, y_rate: float = 0.5) -> tp.Coordinate:
        return None

    @abstractmethod
    def sleep(self, interval: float = 1, rebuild: bool = True) -> None:
        pass

    def input(self, referent: str, input_area: tp.Scope, text: str = None) -> None:
        pass

    def find(self, res: str, draw: bool = False, scope: tp.Scope = None, thres: int = None, judge: bool = True,
             strict: bool = False, score=0.0) -> tp.Scope:
        return None

    def tap(self, poly: tp.Location, x_rate: float = 0.5, y_rate: float = 0.5, interval: float = 1,
            rebuild: bool = True) -> None:
        if interval > 0:
            self.sleep(interval, rebuild)

    def tap_element(self, element_name: str, x_rate: float = 0.5, y_rate: float = 0.5, interval: float = 1,
                    rebuild: bool = True, score: float = 0.0,
                    draw: bool = False, scope: tp.Scope = None, judge: bool = True, detected: bool = False) -> bool:
        return True

    def tap_index_element(self, name):
        self.tap(None, interval=2)

    def template_match(self, res: str, scope: typing.Optional[tp.Scope] = None, method: int = None):
        return None

    def swipe(self, start: tp.Coordinate, movement: tp.Coordinate, duration: int = 100, interval: float = 1,
              rebuild: bool = True) -> None:
        """ swipe """
        if duration > 0:
            self.sleep(duration / 1000)
        if interval > 0:
            self.sleep(interval)

    def swipe_only(self, start: tp.Coordinate, movement: tp.Coordinate, duration: int = 100,
                   interval: float = 1) -> None:
        """ swipe only, no rebuild and recapture """
        self.sleep(interval)

    def swipe_noinertia(self, start: tp.Coordinate, movement: tp.Coordinate, duration: int = 50, interval: float = 0.2,
                        rebuild: bool = False) -> None:
        self.sleep(interval)

    def back(self, interval: float = 1, rebuild: bool = True) -> None:
        self.sleep(interval)

    def scene(self) -> int:
        return 0

    def get_infra_scene(self) -> int:
        return 0

    def is_login(self):
        return True

    def login(self):
        pass

    def get_navigation(self):
        pass

    def back_to_infrastructure(self):
        pass

    def back_to_index(self):
        logger.info('back to index')
        pass

    def waiting_solver(self, scenes, wait_count=20, sleep_time=3):
        return True

    def wait_for_scene(self, scene, method, wait_count=10, sleep_time=1):
        return True
