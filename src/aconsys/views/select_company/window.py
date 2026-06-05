from pathlib import Path

from ...base.window import TopLevelWindow
from .controls import SELECTION_WINDOW, _AREA_SELECTION
from uiautomation import SendKeys
from aconsys.ocr import PyOcr, TesseractEngine, img_to_ndarry, take_screenshot
from time import sleep
from PIL.Image import Image
from aconsys.views.main.window import MainWindow


class SelectionCompanyWindow(TopLevelWindow):
    """Manage the SELECTION COMPANY window."""

    _window = SELECTION_WINDOW

    def __init__(self) -> None:
        return super().__init__()

    def select_company(self, company_name: str, tesseract_path: Path) -> MainWindow:

        assert self._window.Exists(15)

        companies_area = _AREA_SELECTION.PaneControl(
            searchDepth=1, ClassName="TL50.ApexList32.20"
        )

        self._window.SetActive()  # Traer al frente
        companies_area.SetFocus()

        # 2. Inicialización de herramientas (Idealmente esto vendría de self o inyectado)
        tesseract: TesseractEngine = TesseractEngine(tesseract_path)
        ocr_tool: PyOcr = PyOcr(engine=tesseract)

        last_company_detected = ""
        while True:
            SendKeys("{DOWN}")
            sleep(5)
            # 1. Captura y OCR
            screenshot: Image = take_screenshot(companies_area)
            raw_text: str = ocr_tool.process_selected_row(
                image_source=img_to_ndarry(screenshot)
            )
            # 2. Limpieza de texto
            #temp = "".join(c for c in raw_text if c.isalpha() or c.isspace())
            temp = (raw_text.lstrip("0123456789").rstrip())
            temp  = temp.upper().replace(" ","")
            company_selected = temp.upper().replace("BIJOL","BIJOU")
            # A. ¿Es la empresa que buscamos?
            if company_selected == company_name:
                SendKeys("{ENTER}")
                break
            # B. ¿Estamos estancados? (Llegamos al final de la lista)
            if company_selected == last_company_detected:
                # Si la de ahora es igual a la anterior, es que el {DOWN} ya no baja más
                raise ValueError(f"Error: company not found'{company_name}'.")

            # C. Si no es ninguna de las anteriores, seguimos bajando
            last_company_detected = (
                company_selected  # Guardamos para la siguiente vuelta
            )
            sleep(0.3)
        return MainWindow()
