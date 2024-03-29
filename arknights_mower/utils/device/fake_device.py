from arknights_mower.utils.log import logger


class FakeDevice(object):
    """ Fake Device """

    def __init__(self):
        pass

    def start(self) -> None:
        pass

    def run(self, cmd: str) -> None:
        pass

    def launch(self) -> None:
        """ fake - launch the application """
        logger.info("明日方舟，启动！")

    def exit(self) -> None:
        """ fake - exit the application """
        logger.info("退出游戏")

    def send_keyevent(self, keycode: int) -> None:
        """ fake - send a key event """
        logger.debug(f'keyevent: {keycode}')

    def send_text(self, text: str) -> None:
        """ send a text """
        logger.debug(f'text: {repr(text)}')

    def screencap(self, save: bool = False) -> None:
        """ fake - get a screencap """
        pass

    def current_focus(self) -> None:
        """ fate - detect current focus app """
        pass

    def display_frames(self) -> None:
        """ fake - get display frames if in compatibility mode"""
        pass
    def tap(self, point) -> None:
        """ tap """
        logger.debug(f'tap: {point}')

    def swipe(self, start, end, duration: int = 100) -> None:
        """ swipe """
        logger.debug(f'swipe: {start} -> {end}, duration={duration}')

    def swipe_ext(self, points, durations, up_wait: int = 500) -> None:
        """ swipe_ext """
        logger.debug(
            f'swipe_ext: points={points}, durations={durations}, up_wait={up_wait}')

    def check_current_focus(self) -> bool:
        """ fake - check if the application is in the foreground """
        return True
