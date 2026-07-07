from io import BytesIO

from PIL import Image
from pylibdmtx.pylibdmtx import encode

from PyQt6.QtGui import QPixmap, QImage


class DataMatrixGenerator:

    def __init__(self):
        pass

    def generate(self, data: str):

        if not data:
            return None

        try:
            encoded = encode(data.encode("utf-8"))

            image = Image.frombytes(
                "RGB",
                (encoded.width, encoded.height),
                encoded.pixels
            )

            buffer = BytesIO()

            image.save(
                buffer,
                format="PNG"
            )

            qt_image = QImage.fromData(
                buffer.getvalue()
            )

            return QPixmap.fromImage(
                qt_image
            )

        except Exception as error:
            print(f"Ошибка генерации DataMatrix: {error}")
            return None