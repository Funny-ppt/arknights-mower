from . import typealias as tp
class FakeRecognizer(object):

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        pass

    def update(self, screencap: bytes = None, rebuild: bool = True) -> None:
        pass

    def color(self, x: int, y: int) -> None:
        pass

    def save_screencap(self, folder):
        pass

    def detect_connecting_scene(self) -> bool:
        return True

    def detect_index_scene(self) -> bool:
        return True

    def check_loading_time(self):
        pass

    def get_scene(self) -> int:
        return -1

    def get_infra_scene(self) -> int:
        return -1