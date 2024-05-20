import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QObject


class ButtonWorker(QtCore.QThread):
    button_pressed = QtCore.pyqtSignal()

    def __init__(self, gpio: int, parent: typing.Optional[QObject] = None) -> None:
        super().__init__(parent)

        import gpiozero

        self._button = gpiozero.Button(gpio)

    def wait_for_press(self):
        self._button.wait_for_press()
        self._button.wait_for_release()
        self.button_pressed.emit()
        QtCore.QTimer.singleShot(500, self.wait_for_press)
