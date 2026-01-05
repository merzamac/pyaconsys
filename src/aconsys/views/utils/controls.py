from typing import TypeVar

import _ctypes
from uiautomation import Control

TControl = TypeVar("TControl", bound=Control)


# def wait_control_dont_exist(
#     control: TControl,
# ) -> None:
#     """
#     Espera hasta que el control ya no esté disponible (por ejemplo, desaparezca de la ventana).

#     Args:
#         control: el control (WindowSpecification)


#     """
#     while True:
#         try:
#             # Intentamos acceder al wrapper para forzar la resolución
#             control.wrapper_object()
#         except (ElementNotFoundError, TimeoutError):
#             return  # El control ya no existe


def wait_control_exist(
    control: TControl,
) -> None:
    """
    Espera hasta que el control esté disponible.
    Usar el metodo con precaución.

    Args:
        control: Clases derivadas de Control (Control)

    """
    exists: bool = False

    while not exists:
        try:
            exists = control.Exists()
        except TimeoutError:
            pass
        except _ctypes.COMError as e:
            pass
