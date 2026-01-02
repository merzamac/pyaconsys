from random import randint
from uiautomation.uiautomation import (
    PaneControl,
    GroupControl,
)
from uiautomation import SetGlobalSearchTimeout, Click

SetGlobalSearchTimeout(5)


def get_error_message(window_group: GroupControl) -> str:
    """Retorna el mensaje de error si existe Periodo o Voucher"""

    # Patrones más específicos según lo que esperas
    patterns = (
        r"^Voucher_Exis[\s\S]*",
        r"^Periodo[\s\S]*",
    )  # Limitar longitud

    for pattern in patterns:

        control: PaneControl = window_group.PaneControl(
            searchDepth=1, RegexName=pattern
        )

        if control.Exists():
            # Extraer información relevante
            rectangle = control.BoundingRectangle

            Click(x=rectangle.xcenter(), y=rectangle.ycenter() + 90)

            return control.Name

    return ""
