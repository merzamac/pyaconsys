import cv2
from numpy import ndarray, array
from pathlib import Path
from .image_utils import ImageProcessor
from .engine import OCREngine
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

        if show_changes:
            show(original=img, processed=processed_img)

        # Extracción vía Engine (Strategy)
        return self.engine.extract(processed_img, lang, config)

    def process_selected_row(
        self,
        image_source: Path | ndarray,
        lang: str = "spa",
        # CAMBIO CRÍTICO: Añadido espacio ' ' y guion '-' al final de la whitelist.
        # Sin el espacio, Tesseract se rompe al intentar leer "BIJOU - 2020".
        config: str = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ- ",
        show_changes: bool = False,
    ) -> str:
        """Proceso especializado para detectar y leer la fila marcada en azul."""
        img = (
            image_source
            if isinstance(image_source, ndarray)
            else imread(str(image_source))
        )

        # Usamos el método interno de la clase para extraer la fila azul
        processed_img = self.prepare_selected_row_v2(img, padding=8)

        # Guarda lo que procesó OpenCV para que puedas auditarlo visualmente en tu disco
        cv2.imwrite("debug_ocr_input.png", processed_img)

        if show_changes:
            show(original=img, processed=processed_img)

        return self.engine.extract(processed_img, lang, config)

    def prepare_selected_row_v2(self, img: ndarray, padding: int = 5) -> ndarray:
        """Aísla la fila azul, la recorta y la deja en texto negro sobre fondo blanco."""
        # 1. Convertir a HSV para aislar el fondo azul de la fila seleccionada
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Rangos específicos para capturar el azul de selección clásico de sistemas informáticos
        lower_blue = array([100, 120, 50])
        upper_blue = array([140, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # 2. Encontrar las coordenadas del bloque azul
        contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Tomamos el contorno más grande (la fila seleccionada)
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Recortamos la fila azul de la imagen original en escala de grises
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            crop = gray[y:y+h, x:x+w]
            
            # 3. Aplicar Otsu SOLO al recorte (letras blancas sobre fondo oscuro)
            # THRESH_BINARY_INV las convierte automáticamente a letras negras sobre fondo blanco
            _, thresh = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            final_row = thresh
        else:
            # Si por algún motivo no detecta azul, binariza la imagen normal invertida
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, final_row = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 4. Añadir margen blanco para Tesseract (evita que los caracteres toquen el borde)
        if padding > 0:
            final_row = cv2.copyMakeBorder(
                final_row, padding, padding, padding, padding, 
                cv2.BORDER_CONSTANT, value=[255, 255, 255]
            )
            
        return final_row