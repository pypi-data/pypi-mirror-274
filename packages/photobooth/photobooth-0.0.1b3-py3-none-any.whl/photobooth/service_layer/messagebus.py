from functools import partial
import typing

from PyQt5 import QtCore
from photobooth.adapters.upload import UploadWorker

from photobooth.config import Config
from photobooth.entrypoints import Pages
from photobooth.entrypoints.main_widget import MainWidget
from photobooth.adapters.camera import CameraWorker


class MessageBus(QtCore.QObject):
    check_camera = QtCore.pyqtSignal()
    camera_status = QtCore.pyqtSignal(str)
    startup_camera = QtCore.pyqtSignal()

    liveview = QtCore.pyqtSignal()
    liveview_image = QtCore.pyqtSignal(bytes)
    abort_liveview = QtCore.pyqtSignal()

    capture = QtCore.pyqtSignal()
    image_name = QtCore.pyqtSignal(str)
    image = QtCore.pyqtSignal(bytes, str)

    add_image = QtCore.pyqtSignal(bytes, str)
    delete_image = QtCore.pyqtSignal()

    def __init__(
        self,
        main_widget,
        camera: CameraWorker,
        upload: UploadWorker,
        parent: typing.Optional[QtCore.QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._state: Pages = Pages.STARTUP_PAGE

        self._shutter_countdown: int = (
            len(Config.WIDGET_CAPTURE_COUNTDOWN) * 1000 - Config.CAMERA_SHUTTER_DELAY
        )

        self._timeout_timer = QtCore.QTimer()
        self._set_timeouts()

        self._connect_main_widget(main_widget=main_widget)
        self._connect_camera(camera=camera)
        self._connect_upload(upload=upload)

        main_widget.activate_page(page=self._state)

    def _connect_main_widget(self, main_widget: MainWidget):
        # Trigger: control -> widget
        def trigger_page(page: Pages):
            def __trigger():
                main_widget.activate_page(page=page)
                self._state = page

            return __trigger

        def timed_page_trigger(milliseconds: int, page: Pages):
            timer = QtCore.QTimer()
            return partial(timer.singleShot, milliseconds, trigger_page(page=page))

        def _startup_camera(status: str):
            if len(status) == 0:
                trigger_page(page=Pages.GALLERY_PAGE)()
            else:
                main_widget.set_camera_status(status)

        self.camera_status.connect(_startup_camera)

        self.liveview.connect(trigger_page(page=Pages.LIVEVIEW_PAGE))
        self.liveview_image.connect(main_widget.refresh_liveview)
        self.abort_liveview.connect(trigger_page(page=Pages.GALLERY_PAGE))

        self.capture.connect(trigger_page(page=Pages.CAPTURE_PAGE))
        self.image_name.connect(main_widget.set_image_number)
        self.image_name.connect(
            timed_page_trigger(milliseconds=2000, page=Pages.PREVIEW_PAGE)
        )
        self.image.connect(main_widget.set_preview_image)

        self.add_image.connect(trigger_page(page=Pages.GALLERY_PAGE))
        self.add_image.connect(main_widget.add_image_to_gallery)
        self.delete_image.connect(trigger_page(page=Pages.GALLERY_PAGE))

        # Trigger: widget -> control
        main_widget.left_button_pressed.connect(self.define_action_left)
        main_widget.right_button_pressed.connect(self.define_action_right)

    def _connect_camera(self, camera: CameraWorker):
        # Trigger: control -> camera
        self.check_camera.connect(camera.check)

        def _startup_camera(status: str):
            if len(status) == 0:
                self.startup_camera.emit()

        self.camera_status.connect(_startup_camera)

        self.startup_camera.connect(camera.startup)

        self.liveview.connect(camera.start_liveview)
        self.abort_liveview.connect(camera.stop_liveview)

        self.capture.connect(camera.stop_liveview)
        self.capture.connect(partial(camera.capture, offset=self._shutter_countdown))

        # Trigger: camera -> control
        camera.status.connect(self.camera_status)

        camera.liveview_captured.connect(self.liveview_image)

        camera.image_name_fetched.connect(self.image_name)
        camera.image_captured.connect(self.image)

    def _connect_upload(self, upload: typing.Optional[UploadWorker]):
        if upload is not None:
            # Trigger: control -> upload
            self.add_image.connect(upload.upload)

    def _set_timeouts(self):
        self.liveview.connect(
            partial(
                self.__timeout, self.abort_liveview.emit, Config.WIDGET_LIVEVIEW_TIMEOUT
            )
        )
        self.image.connect(
            partial(self.__timeout, self.add_image.emit, Config.WIDGET_PREVIEW_TIMEOUT)
        )

    def __timeout(
        self,
        signal: typing.Callable,
        milliseconds: int,
        *args,
    ):
        self._timeout_timer = QtCore.QTimer()
        self._timeout_timer.timeout.connect(self._timeout_timer.stop)
        self._timeout_timer.timeout.connect(partial(signal, *args))
        self._timeout_timer.start(milliseconds)

    def define_action_left(self, page: Pages):
        if page != self._state:
            return

        self._timeout_timer.stop()
        if page == Pages.STARTUP_PAGE:
            pass
        elif page == Pages.GALLERY_PAGE:
            pass
        elif page == Pages.LIVEVIEW_PAGE:
            self.abort_liveview.emit()
        elif page == Pages.CAPTURE_PAGE:
            pass
        elif page == Pages.PREVIEW_PAGE:
            self.delete_image.emit()
        else:
            pass

    def define_action_right(self, page: Pages):
        if page != self._state:
            return

        self._timeout_timer.stop()
        if page == Pages.STARTUP_PAGE:
            self.check_camera.emit()
        elif page == Pages.GALLERY_PAGE:
            self.liveview.emit()
        elif page == Pages.LIVEVIEW_PAGE:
            self.capture.emit()
        elif page == Pages.CAPTURE_PAGE:
            pass
        elif page == Pages.PREVIEW_PAGE:
            self._timeout_timer.timeout.emit()
            self.liveview.emit()
        else:
            pass
