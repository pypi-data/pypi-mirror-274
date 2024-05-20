import io
import typing
from PyQt5 import QtCore


class UploadWorker(QtCore.QThread):
    def __init__(
        self,
        domain: str,
        resolution: typing.Tuple[int, int],
        auth: typing.Optional[typing.Tuple[str, str]],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        import httpx

        self._client = httpx.Client(
            auth=auth,
        )
        self._url = domain
        self._resolution = resolution

    def upload(self, image_data: bytes, filename: str):
        try:
            from PIL import Image

            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(self._resolution)
            buffer = io.BytesIO()
            image.save(buffer, "JPEG", exif=image.getexif())
            buffer.seek(0)

            self._client.put(
                self._url,
                params=dict(filename=filename),
                data=buffer.getvalue(),
            )
        except Exception:
            pass
