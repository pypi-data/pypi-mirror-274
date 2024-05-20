import math

from PyQt5 import QtWidgets, QtCore, QtGui


class PictureItem(QtWidgets.QGraphicsPixmapItem):
    IMAGE_SCALE_RATIO = 0.35

    def __init__(
        self,
        pixmap: QtGui.QPixmap,
        container_size: QtCore.QSize,
        x: float,
        y: float,
        rotate: int,
    ):
        container_width = container_size.width()
        container_height = container_size.height()

        pixmap = self._transform_pixmap(
            pixmap,
            target_size=QtCore.QSize(
                math.floor(container_width * self.IMAGE_SCALE_RATIO),
                math.floor(container_height * self.IMAGE_SCALE_RATIO),
            ),
            rotate=rotate,
        )

        offset_x = math.floor((1 + x) / 2 * (container_width - pixmap.width()))
        offset_y = math.floor((1 + y) / 2 * (container_height - pixmap.height()))

        super().__init__(pixmap)
        self.setOffset(offset_x, offset_y)

    @staticmethod
    def _transform_pixmap(
        pixmap: QtGui.QPixmap, target_size: QtCore.QSize, rotate: int
    ) -> QtGui.QTransform:
        return pixmap.scaled(
            target_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        ).transformed(QtGui.QTransform().rotate(rotate), QtCore.Qt.SmoothTransformation)
