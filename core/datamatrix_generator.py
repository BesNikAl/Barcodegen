from PIL import Image
from pylibdmtx.pylibdmtx import encode


class DataMatrixGenerator:

    def __init__(self):
        pass

    def generate(self, data: str) -> Image.Image | None:
        """Возвращает PIL.Image (как указано в архитектуре)."""

        if not data:
            return None

        try:
            encoded = encode(data.encode("utf-8"))

            image = Image.frombytes(
                "RGB",
                (encoded.width, encoded.height),
                encoded.pixels
            )

            return image

        except Exception as error:
            print(f"Ошибка генерации DataMatrix: {error}")
            return None