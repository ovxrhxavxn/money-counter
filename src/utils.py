from pathlib import Path

class UtilsMethod:

    def save_image(self, path: str | Path, image: bytes):

        with open(f'{path}', 'wb') as file:

            file.write(image)

    def read_image(self, path: str | Path):

        with open(f'{path}', 'rb') as image:

            image_bytes = image.read()

        return image_bytes