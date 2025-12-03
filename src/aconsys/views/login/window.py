from pathlib import Path
from subprocess import Popen

from pydantic import SecretStr

from ...base.window import TopLevelWindow
from ..main.window import MainWindow
from .controls import CONNECT_BUTTON, LOGIN_WINDOW, PASSWORD_EDIT, USERNAME_EDIT
from keyring.credentials import Credential


class LoginWindow(TopLevelWindow):
    """Manage the ACONSYS login window."""

    _window = LOGIN_WINDOW
    _executable_file: Path
    _popen: Popen | None = None

    def __init__(
        self, executable_file_path: Path | str, credential: Credential
    ) -> None:
        self._executable_file: Path = Path(executable_file_path)
        if not self._executable_file.is_file():
            raise ValueError("INVALID EXECUTABLE FILE PATH.")
        self._credential = credential
        self._popen: Popen
        return super().__init__()

    def __enter__(
        self,
    ) -> MainWindow:
        return self.login(self._credential)

    def __exit__(self, exc_type, exc_val, exc_tb):
        value = MainWindow()
        ## eliminar el proceso aqui

    def login(self, credential: Credential) -> MainWindow:
        """Login to ACONSYS."""
        if MainWindow.exists():
            return MainWindow()

        if not self.exists():
            self._popen = Popen(self._executable_file)

        self.wait_for()

        username_edit = USERNAME_EDIT.GetValuePattern()
        username_edit.SetValue(credential.username)

        password_edit = PASSWORD_EDIT.GetValuePattern()
        password_edit.SetValue(credential.password)

        connect_btn = CONNECT_BUTTON.GetInvokePattern()
        connect_btn.Invoke()

        if self.exists():
            raise RuntimeError(
                "Error in login. Incorrect password or username. Or the window not responding."
            )

        return MainWindow()
