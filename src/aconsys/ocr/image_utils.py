from numpy import ndarray, array
from .helpers import get_roi_from_image, scale_image
from cv2 import (
    cvtColor,
    COLOR_BGR2GRAY,
    threshold,
    THRESH_BINARY_INV,
    COLOR_BGR2HSV,
    THRESH_OTSU,
    inRange,
    findNonZero,
    boundingRect,
    getStructuringElement,
    erode,
    MORPH_RECT,
)


class ImageProcessor:
    """Clase dedicada exclusivamente a manipular la imagen."""

    @staticmethod
    def prepare_for_ocr(
        image: ndarray, coords: list[int], scale_factor: int = 3
    ) -> ndarray:
        # 1. Recorte (ROI)
        roi = image if not any(coords) else get_roi_from_image(image, *coords)

        # 2. Escalado
        roi_resized = scale_image(roi, scale_factor)

        # 3. Conversión a escala de grises
        gray = cvtColor(roi_resized, COLOR_BGR2GRAY)

        # 4. Umbralización (Thresholding)
        #
        _, thresh = threshold(gray, 140, 255, THRESH_BINARY_INV)

        return thresh

    @staticmethod
    def prepare_selected_row(image: ndarray, scale_factor: int = 3) -> ndarray:
        """
        Método especializado: Detecta la barra azul, recorta y optimiza.
        Diseñado para capturar solo la empresa seleccionada.
        """
        # 1. Detectar el área azul (Fondo de selección)
        # Convertimos a HSV porque es más robusto para detectar colores específicos
        hsv = cvtColor(image, COLOR_BGR2HSV)

        # Rangos para el azul de selección de Windows antiguo
        lower_blue = array([100, 150, 50])
        upper_blue = array([140, 255, 255])

        mask = inRange(hsv, lower_blue, upper_blue)
        points = findNonZero(mask)

        if points is not None:
            # Obtenemos el rectángulo que encierra todo el azul detectado
            x, y, w, h = boundingRect(points)
            # Recortamos la franja (todo el ancho de la lista, pero solo el alto azul)
            roi = image[y : y + h, 0 : image.shape[1]]
        else:
            # Si no hay azul, usamos la imagen completa para no romper el flujo
            roi = image

        # 2. Escalado para mejorar precisión de OCR
        roi_resized = scale_image(roi, scale_factor)

        # 3. Procesamiento de color para contraste máximo
        gray = cvtColor(roi_resized, COLOR_BGR2GRAY)

        # 4. Umbralización de OTSU (Automática)
        # Como el texto es blanco sobre azul, al invertir (INV) quedará
        # negro sobre blanco. OTSU calculará el mejor umbral automáticamente.
        _, thresh = threshold(gray, 0, 255, THRESH_BINARY_INV + THRESH_OTSU)

        return thresh
