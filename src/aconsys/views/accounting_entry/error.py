from uiautomation.uiautomation import (
    PaneControl,
    GroupControl,
)
from uiautomation import SetGlobalSearchTimeout, Click

SetGlobalSearchTimeout(5)


def get_error_message(window_group: GroupControl) -> dict[str, str]:
    """Retorna el mensaje de error si existe Periodo o Voucher"""

    # Patrones más específicos según lo que esperas
    patterns = (
        (r"^Voucher_Exis[\s\S]*", "VOUCHER"),  # Limitar longitud
        (r"^Periodo[\s\S]*", "PERIODO"),
    )

    for pattern, error_type in patterns:

        control: PaneControl = window_group.PaneControl(
            searchDepth=1, RegexName=pattern
        )

        if control.Exists():
            # Extraer información relevante
            rectangle = control.BoundingRectangle

            Click(x=rectangle.xcenter(), y=rectangle.ycenter() + 90)
            return {
                "error_type": error_type,
                "dialog_text": control.Name,
            }

    return {
        # empty dict
    }
