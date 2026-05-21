"""Test fixtures."""

from os import environ
from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr
from pytest import fixture

load_dotenv()


@fixture(scope="session")
def executable_file() -> Path:
    """Path to the Aconsys executable file."""
    return Path(environ["ACONSYS_EXECUTABLE_FILE_PATH"])


@fixture(scope="session")
def server() -> str:
    """Address of the Aconsys server."""
    return environ["ACONSYS_SERVER"]


@fixture(scope="session")
def database() -> str:
    """Database name for the Aconsys server."""
    return environ["ACONSYS_DATABASE"]


@fixture(scope="session")
def username() -> str:
    """Username for the Aconsys server."""
    return environ["ACONSYS_USERNAME"]


@fixture(scope="session")
def password() -> SecretStr:
    """Password for the Aconsys server."""
    return SecretStr(environ["ACONSYS_PASSWORD"])


@fixture(scope="session")
def tesseract() -> Path:
    return Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
