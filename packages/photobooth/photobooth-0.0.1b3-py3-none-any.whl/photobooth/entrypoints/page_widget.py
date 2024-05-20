import textwrap
import typing

from PyQt5 import QtWidgets, QtCore, QtGui
from photobooth.config import Config

from photobooth.entrypoints import Pages, picture_item


class ButtonPage(QtWidgets.QWidget):
    PAGE: Pages
    LEFT_BUTTON: typing.Optional[str] = None
    RIGHT_BUTTON: typing.Optional[str] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        self.setStyleSheet(
            """
                QPushButton {
                    background-color: #50000000;
                    padding: 10px;
                    border: 2px solid #ffffff;
                    font-size: 20px;
                    font-weight: bold;
                    color: #ffffff;
                }

                QGraphicsView {
                    background-color: transparent;
                    padding: 0px;
                    border: none;
                }

                QLabel {
                    background-color: transparent;
                    font-size: 30px;
                    color: #ffffff;
                }
            """
        )

        if self.LEFT_BUTTON is not None:
            left_button = QtWidgets.QPushButton(self.LEFT_BUTTON)
            left_button.pressed.connect(self.trigger_left_button_press)
            layout.addWidget(left_button, 2, 1)

        if self.RIGHT_BUTTON is not None:
            right_button = QtWidgets.QPushButton(self.RIGHT_BUTTON)
            right_button.pressed.connect(self.trigger_right_button_press)
            layout.addWidget(right_button, 2, 3)

    def trigger_left_button_press(self):
        return self.parentWidget().left_button_pressed.emit(self.PAGE)

    def trigger_right_button_press(self):
        return self.parentWidget().right_button_pressed.emit(self.PAGE)


class StartupPage(ButtonPage):
    PAGE = Pages.STARTUP_PAGE
    RIGHT_BUTTON = Config.WIDGET_STARTUP_RIGHT_BUTTON

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._label = QtWidgets.QLabel()
        self._label.setStyleSheet(
            f"""
                QLabel {{
                    background-color: transparent;
                    font-size: 30px;
                    color: {Config.WIDGET_STARTUP_CAMERA_MESSAGE_COLOR};
                }}
            """
        )
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self._label, 1, 1, 1, -1)

        self._label.setText(Config.WIDGET_STARTUP_CAMERA_MESSAGE)

    def set_status(self, status: str) -> None:
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self._label.setText(
            Config.WIDGET_STARTUP_CAMERA_ERROR_MESSAGE.format(
                status=textwrap.indent(status, " - ", lambda line: True)
            )
        )


class ViewButtonPage(ButtonPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._view = QtWidgets.QGraphicsView()
        self._view.setScene(QtWidgets.QGraphicsScene())
        self.layout().addWidget(self._view, 1, 1, 1, -1)


class GalleryPosition(typing.NamedTuple):
    x: float
    y: float
    rotate: int = 0


class GalleryPage(ViewButtonPage):
    PAGE = Pages.GALLERY_PAGE
    RIGHT_BUTTON = Config.WIDGET_GALLERY_RIGHT_BUTTON

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.gallery_stack = self._setup_gallery()

    def load_gallery(self):
        self._view.scene().clear()
        for position, pixmap in self.gallery_stack:
            if pixmap is not None:
                self._view.scene().addItem(
                    picture_item.PictureItem(
                        pixmap=pixmap,
                        container_size=self._view.size(),
                        **position._asdict(),
                    )
                )
        self._view.scene().setSceneRect(
            0, 0, self._view.width() - 2, self._view.height() - 2
        )

    def add_image(self, pixmap: QtGui.QPixmap):
        position, old_pixmap = self.gallery_stack.pop(0)

        self.gallery_stack.append((position, pixmap))

        if old_pixmap is not None:
            del old_pixmap

        self.load_gallery()

    def remove_image(self):
        position, old_pixmap = self.gallery_stack.pop()

        self.gallery_stack.insert(0, (position, None))

        if old_pixmap is not None:
            del old_pixmap

        self.load_gallery()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        self.load_gallery()

    @staticmethod
    def _setup_gallery() -> (
        typing.List[typing.Tuple[GalleryPosition, typing.Optional[QtGui.QPixmap]]]
    ):
        return [
            (GalleryPosition(x=x, y=y, rotate=rotate), None)
            for x, y, rotate in Config.WIDGET_GALLERY_POSITIONS
        ]


class SingleImagePage(ViewButtonPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._pixmap_item = self._view.scene().addPixmap(QtGui.QPixmap())

    def show_image(self, pixmap: QtGui.QPixmap) -> None:
        pixmap.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        self._pixmap_item.setPixmap(pixmap)
        self.resize_pixmap()

    def resize_pixmap(self) -> None:
        if (self._view.width() < self._pixmap_item.pixmap().width()) or (
            self._view.height() < self._pixmap_item.pixmap().height()
        ):
            self._view.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if not self._pixmap_item.pixmap().isNull():
            self.resize_pixmap()
        super().resizeEvent(event)


class LiveviewPage(SingleImagePage):
    PAGE = Pages.LIVEVIEW_PAGE
    LEFT_BUTTON = Config.WIDGET_LIVEVIEW_LEFT_BUTTON
    RIGHT_BUTTON = Config.WIDGET_LIVEVIEW_RIGHT_BUTTON


class PreviewPage(SingleImagePage):
    PAGE = Pages.PREVIEW_PAGE
    LEFT_BUTTON = Config.WIDGET_PREVIEW_LEFT_BUTTON
    RIGHT_BUTTON = Config.WIDGET_PREVIEW_RIGHT_BUTTON


class CapturePage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(QtWidgets.QStackedLayout())

        self._label = QtWidgets.QLabel()
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self._label)

        self._countdown: typing.Optional[typing.Iterable] = None

        self._timer: QtCore.QTimer
        self._setup_timer()

    def _setup_timer(self):
        self._timer = QtCore.QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._update_label)

    def reset_countdown(self) -> None:
        self._label.setStyleSheet(
            f"""
                QLabel {{
                    background-color: transparent;
                    font-size: 120px;
                    font-weight: bold;
                    color: {Config.WIDGET_CAPTURE_COUNTDOWN_COLOR};
                }}
            """
        )
        self._countdown = iter(Config.WIDGET_CAPTURE_COUNTDOWN)
        self._update_label()
        self._timer.start()

    def _update_label(self):
        try:
            self._label.setText(str(next(self._countdown)))
        except StopIteration:
            self._timer.stop()
            pass

    def set_image_number(self, number):
        self._timer.stop()
        self._label.setStyleSheet(
            f"""
                QLabel {{
                    background-color: transparent;
                    font-size: 30px;
                    color: {Config.WIDGET_CAPTURE_FILE_NUMBER_MESSAGE_COLOR};
                }}
            """
        )
        self._label.setText(
            Config.WIDGET_CAPTURE_FILE_NUMBER_MESSAGE.format(number=number)
        )
