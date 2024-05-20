import json
import sys
import typing
import importlib.util

import click

from PyQt5 import QtWidgets, QtCore

from photobooth.config import Config


def start_camera_worker(
    configuration: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None,
    testing: typing.Optional[str] = None,
) -> typing.Tuple[QtCore.QObject, QtCore.QThread]:
    from photobooth import adapters

    if testing:
        camera = adapters.camera.DummyCameraWorker(folder=testing)
    elif importlib.util.find_spec("gphoto2") is not None:
        camera = adapters.camera.NikonCameraWorker(configuration=configuration)
    else:
        raise RuntimeError(
            "Package gphoto2 is missing please install with: "
            "pip install photobooth[dslr]"
        )

    camera_thread = QtCore.QThread()
    camera.moveToThread(camera_thread)
    camera_thread.finished.connect(camera.shutdown)

    return camera, camera_thread


def start_upload_worker() -> typing.Tuple[QtCore.QObject, QtCore.QThread]:
    from photobooth import adapters

    if Config.UPLOAD_DOMAIN is not None:
        upload = adapters.upload.UploadWorker(
            domain=Config.UPLOAD_DOMAIN,
            resolution=Config.UPLOAD_MAX_RESOLUTION,
            auth=Config.UPLOAD_AUTH,
        )
        upload_thread = QtCore.QThread()
        upload.moveToThread(upload_thread)
        return upload, upload_thread

    return None, None


def start_hardware_button_worker() -> (
    typing.Tuple[
        typing.Optional[QtCore.QObject],
        typing.Optional[QtCore.QObject],
        typing.Optional[QtCore.QThread],
        typing.Optional[QtCore.QThread],
    ]
):
    from photobooth import adapters

    if importlib.util.find_spec("gpiozero") is not None:
        left_button, right_button = (
            adapters.buttons.ButtonWorker(gpio=Config.HARDWAREBUTTON_LEFT_BUTTON_GPIO),
            adapters.buttons.ButtonWorker(gpio=Config.HARDWAREBUTTON_RIGHT_BUTTON_GPIO),
        )

        left_button_thread, right_button_thread = (QtCore.QThread(), QtCore.QThread())
        left_button.moveToThread(left_button_thread)
        right_button.moveToThread(right_button_thread)
        left_button_thread.started.connect(left_button.wait_for_press)
        right_button_thread.started.connect(right_button.wait_for_press)

        return left_button, right_button, left_button_thread, right_button_thread
    click.echo("No Hardware Buttons found.", err=True)
    return (None, None, None, None)


@click.command
@click.option(
    "-c",
    "--config",
    "config",
    help="Configuration to load.",
    type=click.Path(exists=True, path_type=str),
    default=None,
)
@click.option(
    "-d",
    "--dslr-config",
    "dslr_config",
    help="DSLR Configuration to check on start.",
    type=click.Path(exists=True, path_type=str),
    default=None,
)
@click.option(
    "-s",
    "--window-size",
    "window_size",
    help=(
        "The window size in pixel (width, height). "
        "If none is provided opens in fullscreen mode."
    ),
    type=(int, int),
    default=None,
)
@click.option(
    "-t",
    "--testing",
    "testing",
    help="Directory containing images to use for faking the camera.",
    type=click.Path(exists=True, path_type=str),
    default=None,
)
def cli(
    window_size: typing.Optional[typing.Tuple[int, int]] = None,
    config: typing.Optional[str] = None,
    dslr_config: typing.Optional[str] = None,
    testing: typing.Optional[str] = None,
):
    if config is not None:
        Config.from_file(config)

    if dslr_config is not None:
        with open(dslr_config, "r") as file:
            dslr_config = json.load(file)

    app = QtWidgets.QApplication([])

    camera, camera_thread = start_camera_worker(
        configuration=dslr_config, testing=testing
    )
    left_button, right_button, *button_threads = start_hardware_button_worker()
    upload, upload_thread = start_upload_worker()

    from photobooth.entrypoints.main_widget import MainWidget

    main_widget = MainWidget(
        left_hardware_button=left_button,
        right_hardware_button=right_button,
    )

    from photobooth.service_layer.messagebus import MessageBus

    message_bus = MessageBus(  # noqa: F841
        main_widget=main_widget, camera=camera, upload=upload
    )

    if window_size is None:
        main_widget.showFullScreen()
    else:
        main_widget.resize(*window_size)
    main_widget.show()

    try:
        for button_thread in button_threads:
            if button_thread is not None:
                button_thread.start()
        if upload_thread is not None:
            upload_thread.start()
        camera_thread.start()
        status_code = app.exec()
    finally:
        camera_thread.quit()
        camera_thread.wait()
        if upload is not None:
            upload_thread.quit()
            upload_thread.wait()
        for button_thread in button_threads:
            if button_thread is not None:
                button_thread.quit()
                button_thread.wait()

    sys.exit(status_code)


if __name__ == "__main__":
    cli()
