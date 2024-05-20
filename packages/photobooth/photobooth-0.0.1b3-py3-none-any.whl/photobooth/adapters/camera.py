import time
from pathlib import Path
import typing

from PyQt5 import QtCore


class CameraWorker(QtCore.QObject):
    status = QtCore.pyqtSignal(str)
    liveview_captured = QtCore.pyqtSignal(bytes)
    image_name_fetched = QtCore.pyqtSignal(str)
    image_captured = QtCore.pyqtSignal(bytes, str)

    def start_liveview(self) -> None:
        raise NotImplementedError

    def stop_liveview(self) -> None:
        raise NotImplementedError

    def liveview(self) -> None:
        raise NotImplementedError

    def capture(self, offset: int = 0) -> None:
        timer = QtCore.QTimer()
        timer.singleShot(int(offset), self._capture)

    def _capture(self) -> None:
        raise NotImplementedError

    def check(self) -> None:
        raise NotImplementedError

    def startup(self) -> None:
        self._liveview_timer = QtCore.QTimer()
        self._liveview_timer.setInterval(int(1.0 / 40 * 1000))
        self._liveview_timer.timeout.connect(
            self.liveview, type=QtCore.Qt.ConnectionType.QueuedConnection
        )

    def shutdown(self) -> None:
        pass


class DummyCameraWorker(CameraWorker):
    def __init__(self, folder: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._pictures = list(Path(folder).glob("*.JPG"))

        self._liveview_timer: QtCore.QTimer

        self._error = True

    def start_liveview(self) -> None:
        self._liveview_timer.start()

    def stop_liveview(self) -> None:
        self._liveview_timer.stop()

    def liveview(self) -> None:
        self.liveview_captured.emit(open(self._pictures[0], mode="rb").read())

    def _capture(self) -> None:
        path = self._pictures.pop(0)
        self.image_name_fetched.emit(path.name)
        time.sleep(1)
        self.image_captured.emit(open(path, mode="rb").read(), path.name)
        self._pictures.append(path)

    def check(self) -> None:
        if self._error:
            self._error = False
            return self.status.emit("Config Diff1\nConfig Diff2")

        return self.status.emit("")


class NikonCameraWorker(CameraWorker):
    def __init__(
        self,
        *args,
        configuration: typing.Optional[
            typing.List[typing.Dict[str, typing.Any]]
        ] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        import gphoto2

        self._configuration = configuration
        self._camera: gphoto2.Camera

        self._liveview_timer: QtCore.QTimer

    def start_liveview(self) -> None:
        self._liveview_timer.start()

    def stop_liveview(self) -> None:
        self._liveview_timer.stop()

    def liveview(self) -> None:
        camera_file = self._camera.capture_preview()
        self.liveview_captured.emit(
            memoryview(camera_file.get_data_and_size()).tobytes()
        )

    def _capture(self, offset: int = 0) -> None:
        import gphoto2

        camera_path = self._camera.capture(gphoto2.GP_CAPTURE_IMAGE)

        self.image_name_fetched.emit(camera_path.name)
        camera_file = self._camera.file_get(
            camera_path.folder,
            camera_path.name,
            gphoto2.GP_FILE_TYPE_NORMAL,
        )

        self.image_captured.emit(
            memoryview(camera_file.get_data_and_size()).tobytes(),
            camera_path.name,
        )

    def check(self) -> None:
        import gphoto2

        cameras = gphoto2.Camera.autodetect()
        if len(cameras) == 0:
            self.status.emit("No camera found. Please turn on and try again.")
            return None

        if self._configuration is None:
            self.status.emit("")
            return None

        camera = gphoto2.Camera()
        try:
            camera.init()
            config = camera.get_config()

            message = ""
            for setting in self._configuration:
                child = config.get_child_by_name(setting["name"])
                if setting["name"] == "availableshots":
                    if child.get_value() < setting["value"]:
                        message += (
                            f"\n{setting['label']}: "
                            f"{child.get_value()} < {setting['value']}"
                        )

                else:
                    if isinstance(setting["value"], list):
                        if child.get_value() not in setting["value"]:
                            message += (
                                f"\n{setting['label']}: "
                                f"{child.get_value()} not in {setting['value']}"
                            )
                    elif child.get_value() != setting["value"]:
                        message += (
                            f"\n{setting['label']}:"
                            f" {child.get_value()} != {setting['value']}"
                        )

            self.status.emit(message)
            return None
        except Exception:
            self.status.emit("Error please restart.")
            return None
        finally:
            camera.exit()
            del camera

    def startup(self) -> None:
        super().startup()
        import gphoto2

        self._camera = gphoto2.Camera()

        self._camera.init()

    def shutdown(self) -> None:
        if hasattr(self, "_camera"):
            self._camera.exit()
