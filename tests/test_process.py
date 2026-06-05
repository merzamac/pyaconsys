from pathlib import Path
from aconsys.views.login.window import LoginWindow as AconsysApp
from keyring.credentials import Credential
from .manager import CredentialManager
from datetime import date
from aconsys.views.login.window import MainWindow


def test_go_to_compras_view(executable_file) -> None:
    credentials: Credential = CredentialManager.get_credential(service_name="Aconsys")
    with AconsysApp(executable_file, credentials) as app:
        # app.change_work_period()
        app.change_work_period(date(2025, 10, 30))
        if not isinstance(app, MainWindow):
            app = app.select_company("BIJOU")


def test_select() -> None:
    executable_file = Path(r"\\192.168.1.6\pycas\VAsicont.exe")
    tesseract = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    credentials: Credential = CredentialManager.get_credential(service_name="Aconsys")
    with AconsysApp(executable_file, credentials) as app:
        if not isinstance(app, MainWindow):
            app = app.select_company("BIJOU-2020", tesseract)
        

