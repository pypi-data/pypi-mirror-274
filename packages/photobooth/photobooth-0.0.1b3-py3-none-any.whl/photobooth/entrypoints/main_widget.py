from PyQt5 import QtWidgets, QtCore, QtGui
from photobooth.adapters.buttons import ButtonWorker
from photobooth.config import Config

from photobooth.entrypoints import Pages, page_widget


class MainWidget(QtWidgets.QWidget):
    left_button_pressed = QtCore.pyqtSignal(Pages)
    right_button_pressed = QtCore.pyqtSignal(Pages)

    def __init__(
        self,
        left_hardware_button: ButtonWorker,
        right_hardware_button: ButtonWorker,
        **kwargs,
    ) -> None:
        self.layout: QtWidgets.QStackedLayout
        super().__init__(**kwargs)
        self.setWindowTitle(Config.WIDGET_TITLE)
        self.setLayout(QtWidgets.QStackedLayout())

        if left_hardware_button is not None:
            left_hardware_button.button_pressed.connect(
                self._left_hardware_button_pressed
            )
        if right_hardware_button is not None:
            right_hardware_button.button_pressed.connect(
                self._right_hardware_button_pressed
            )

        self._create_pages()

    def _create_pages(self):
        self.layout().insertWidget(
            Pages.STARTUP_PAGE.value,
            page_widget.StartupPage(parent=self),
        )

        self.layout().insertWidget(
            Pages.GALLERY_PAGE.value,
            page_widget.GalleryPage(parent=self),
        )

        self.layout().insertWidget(
            Pages.LIVEVIEW_PAGE.value,
            page_widget.LiveviewPage(parent=self),
        )

        self.layout().insertWidget(
            Pages.CAPTURE_PAGE.value,
            page_widget.CapturePage(parent=self),
        )

        self.layout().insertWidget(
            Pages.PREVIEW_PAGE.value,
            page_widget.PreviewPage(parent=self),
        )

    def _left_hardware_button_pressed(self):
        self.left_button_pressed.emit(Pages(self.layout().currentIndex()))

    def _right_hardware_button_pressed(self):
        self.right_button_pressed.emit(Pages(self.layout().currentIndex()))

    def activate_page(self, page: Pages):
        self.layout().setCurrentIndex(page.value)

        widget = self.layout().currentWidget()
        if page == Pages.CAPTURE_PAGE:
            widget.reset_countdown()
        elif page == Pages.PREVIEW_PAGE:
            widget.resize_pixmap()

    def set_camera_status(self, status: str):
        self.layout().widget(Pages.STARTUP_PAGE.value).set_status(status=status)

    def refresh_liveview(self, image_data: bytes):
        self.layout().widget(Pages.LIVEVIEW_PAGE.value).show_image(
            pixmap=self.convert_image_data_to_pixmap(image_data=image_data)
        )

    def set_image_number(self, image_name: str):
        number = Config.CAMERA_FILE_NUMBER_PATTERN.fullmatch(image_name)
        if number is not None:
            self.layout().widget(Pages.CAPTURE_PAGE.value).set_image_number(
                number.group(1)
            )

    def set_preview_image(self, image_data: bytes, *args):
        self.layout().widget(Pages.PREVIEW_PAGE).show_image(
            pixmap=self.convert_image_data_to_pixmap(image_data=image_data)
        )

    def add_image_to_gallery(self, image_data: bytes, *args):
        self.layout().widget(Pages.GALLERY_PAGE.value).add_image(
            pixmap=self.convert_image_data_to_pixmap(image_data=image_data)
        )

    def resizeEvent(self, event: QtGui.QResizeEvent):
        background = QtGui.QPixmap(Config.WIDGET_BACKGROUND_IMAGE)
        background = background.scaled(
            self.width(),
            self.height(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        palette = QtGui.QPalette()
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Window,
            QtGui.QBrush(background),
        )
        self.setPalette(palette)
        super().resizeEvent(event)

    @staticmethod
    def convert_image_data_to_pixmap(image_data) -> QtGui.QPixmap:
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(memoryview(image_data).tobytes())
        return pixmap
