from .image_utils import ImageProcessor
from .engine import OCREngine
from numpy import ndarray
from pathlib import Path
from .helpers import show
from cv2 import imread


class PyOcr:
    def __init__(self, engine: OCREngine):
        self.engine = engine

    def process(
        self,
        image_source: Path | ndarray,
        lang: str = "spa",
        config: str = "--psm 4 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-.",
        coords: list[int] = [0, 0, 0, 0],
        show_changes: bool = False,
    ) -> str:
        # Carga de imagen
        img = (
            image_source
            if isinstance(image_source, ndarray)
            else imread(str(image_source))
        )

        # Preprocesamiento
        processed_img = ImageProcessor.prepare_for_ocr(img, coords)

        # Visualización (Opcional)
        # if show_changes:
        #     show(original=img, processed=processed_img)

        # Extracción vía Engine (Strategy)
        return self.engine.extract(processed_img, lang, config)

    def process_selected_row(
        self,
        image_source: Path | ndarray,
        lang: str = "spa",
        # Cambiamos a --psm 7 porque una fila es una sola línea de texto
        config: str = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-.",
        show_changes: bool = False,
    ) -> str:
        """Proceso especializado para detectar y leer la fila marcada en azul."""
        img = (
            image_source
            if isinstance(image_source, ndarray)
            else imread(str(image_source))
        )

        # Usa el nuevo método especializado de ImageProcessor
        processed_img = ImageProcessor.prepare_selected_row(img, 5)

        # if show_changes:
        #     show(original=img, processed=processed_img)

        return self.engine.extract(processed_img, lang, config)
