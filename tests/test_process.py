from aconsys.views.login.window import LoginWindow as AconsysApp
from keyring.credentials import Credential
from .credential.manager import CredentialManager
from datetime import date


def test_go_to_compras_view(executable_file) -> None:
    credentials: Credential = CredentialManager.get_credential(service_name="Aconsys")
    with AconsysApp(executable_file, credentials) as app:
        # app.change_work_period()
        app.change_work_period(date(2026, 6, 15))

        accounting_window = app.accounting_entry_process_from_excel()
        accounting_window.set_date_and_type_operation(date(2026, 2, 15), "99")
        accounting_window.set_file_path("values")
        accounting_window.get_validation()
