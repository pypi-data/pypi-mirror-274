import configparser
import json
import re
import typing
from importlib import resources


with resources.as_file(resources.files("photobooth")) as file:
    DEFAULT_WIDGET_BACKGROUND_IMAGE = str(file.joinpath("resources/oak.jpg"))


class Config:
    WIDGET_TITLE: str = "Photobooth"
    WIDGET_BACKGROUND_IMAGE: str = DEFAULT_WIDGET_BACKGROUND_IMAGE

    WIDGET_STARTUP_RIGHT_BUTTON: str = "Check camera"
    WIDGET_STARTUP_CAMERA_MESSAGE: str = "Please, turn on your camera!"
    WIDGET_STARTUP_CAMERA_ERROR_MESSAGE: str = (
        "Please check you camera. Camera has the following status:\n{status}"
    )
    WIDGET_STARTUP_CAMERA_MESSAGE_COLOR: str = "#333"

    WIDGET_GALLERY_RIGHT_BUTTON = "Photo"
    WIDGET_GALLERY_POSITIONS: typing.List[typing.Tuple[float, float, int]] = [
        (0.0, 0.0, 2),
        (-0.8, -0.6, -6),
        (0.7, -0.65, 10),
        (0.4, 0.8, -4),
        (-0.5, 0.8, 8),
        (-0.9, 0.6, -6),
        (0.05, -0.9, 4),
        (0.95, 0.95, 2),
        (0.85, -0.05, -4),
        (-0.95, -0.95, -4),
        (-0.1, -0.05, 12),
        (0.9, -0.95, -10),
        (0.0, 0.95, 2),
        (-0.65, 0.95, 4),
        (0.25, 0.05, 4),
        (-0.5, -0.5, -10),
    ]

    WIDGET_LIVEVIEW_LEFT_BUTTON: str = "Back"
    WIDGET_LIVEVIEW_RIGHT_BUTTON: str = "Photo"
    WIDGET_LIVEVIEW_TIMEOUT: int = 10000

    WIDGET_CAPTURE_COUNTDOWN: typing.Tuple[typing.Union[str, int], ...] = (
        "3",
        "2",
        "Smile!",
    )
    WIDGET_CAPTURE_COUNTDOWN_COLOR: str = "#333"
    WIDGET_CAPTURE_FILE_NUMBER_MESSAGE: str = "This photo has the number: {number}"
    WIDGET_CAPTURE_FILE_NUMBER_MESSAGE_COLOR: str = "#333"

    WIDGET_PREVIEW_LEFT_BUTTON: str = "Delete"
    WIDGET_PREVIEW_RIGHT_BUTTON: str = "Next"
    WIDGET_PREVIEW_TIMEOUT: int = 5000

    CAMERA_FILE_NUMBER_PATTERN: re.Pattern = re.compile(r"P\d{2}_(\d{4}).JPG")
    CAMERA_SHUTTER_DELAY: int = 0

    HARDWAREBUTTON_LEFT_BUTTON_GPIO: int = 23
    HARDWAREBUTTON_RIGHT_BUTTON_GPIO: int = 24

    UPLOAD_DOMAIN: typing.Optional[str] = None
    UPLOAD_MAX_RESOLUTION: typing.Tuple[int, int] = (1920, 1280)
    UPLOAD_AUTH: typing.Optional[typing.Tuple[str, str]] = None

    @classmethod
    def from_file(cls, path: str):
        config = configparser.ConfigParser()
        with open(path, mode="r", encoding="utf-8") as file:
            config.read_string(file.read())
        pass

        if config.has_section("widget"):
            cls.WIDGET_TITLE = config["widget"].get("title", cls.WIDGET_TITLE)
            cls.WIDGET_BACKGROUND_IMAGE = config["widget"].get(
                "background_image", cls.WIDGET_BACKGROUND_IMAGE
            )

        if config.has_section("widget.gallery"):
            cls.WIDGET_GALLERY_RIGHT_BUTTON = config["widget.gallery"].get(
                "right_button", cls.WIDGET_GALLERY_RIGHT_BUTTON
            )
            positions = config["widget.gallery"].get("positions")
            if positions is not None:
                cls.WIDGET_GALLERY_POSITIONS = json.loads(positions)

        if config.has_section("widget.liveview"):
            cls.WIDGET_LIVEVIEW_LEFT_BUTTON = config["widget.liveview"].get(
                "left_button", cls.WIDGET_LIVEVIEW_LEFT_BUTTON
            )
            cls.WIDGET_LIVEVIEW_RIGHT_BUTTON = config["widget.liveview"].get(
                "right_button", cls.WIDGET_LIVEVIEW_RIGHT_BUTTON
            )
            cls.WIDGET_LIVEVIEW_TIMEOUT = int(
                config["widget.liveview"].get(
                    "timeout", str(cls.WIDGET_LIVEVIEW_TIMEOUT)
                )
            )

        if config.has_section("widget.capture"):
            countdown = config["widget.capture"].get("countdown")
            if isinstance(countdown, str):
                cls.WIDGET_CAPTURE_COUNTDOWN = countdown.split(",")
            cls.WIDGET_CAPTURE_COUNTDOWN_COLOR = config["widget.capture"].get(
                "countdown_color", cls.WIDGET_CAPTURE_COUNTDOWN_COLOR
            )
            cls.WIDGET_CAPTURE_FILE_NUMBER_MESSAGE = (
                config["widget.capture"]
                .get("file_number_message", cls.WIDGET_CAPTURE_FILE_NUMBER_MESSAGE)
                .replace("\\n", "\n")
            )
            cls.WIDGET_CAPTURE_FILE_NUMBER_MESSAGE_COLOR = config["widget.capture"].get(
                "file_number_message_color",
                cls.WIDGET_CAPTURE_FILE_NUMBER_MESSAGE_COLOR,
            )

        if config.has_section("widget.preview"):
            cls.WIDGET_PREVIEW_LEFT_BUTTON = config["widget.preview"].get(
                "left_button", cls.WIDGET_PREVIEW_LEFT_BUTTON
            )
            cls.WIDGET_PREVIEW_RIGHT_BUTTON = config["widget.preview"].get(
                "right_button", cls.WIDGET_PREVIEW_RIGHT_BUTTON
            )
            cls.WIDGET_PREVIEW_TIMEOUT = int(
                config["widget.preview"].get("timeout", str(cls.WIDGET_PREVIEW_TIMEOUT))
            )

        if config.has_section("camera"):
            pattern = config["camera"].get("file_number_pattern")
            if isinstance(pattern, str):
                cls.CAMERA_FILE_NUMBER_PATTERN = re.compile(pattern=pattern)
            cls.CAMERA_SHUTTER_DELAY = int(
                config["camera"].get("shutter_delay", str(cls.CAMERA_SHUTTER_DELAY))
            )

        if config.has_section("hardwarebutton"):
            cls.HARDWAREBUTTON_LEFT_BUTTON_GPIO = int(
                config["hardwarebutton"].get(
                    "left_button", cls.HARDWAREBUTTON_LEFT_BUTTON_GPIO
                )
            )
            cls.HARDWAREBUTTON_RIGHT_BUTTON_GPIO = int(
                config["hardwarebutton"].get(
                    "right_button", cls.HARDWAREBUTTON_RIGHT_BUTTON_GPIO
                )
            )

        if config.has_section("upload"):
            cls.UPLOAD_DOMAIN = config["upload"].get("domain")

            resolution = config["upload"].get("max_resolution")
            if resolution is not None:
                cls.UPLOAD_MAX_RESOLUTION = tuple(map(int, resolution.split(",")))

            username = config["upload"].get("username")
            password = config["upload"].get("password")
            if username is not None and password is not None:
                cls.UPLOAD_AUTH = (username, password)
