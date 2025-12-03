from pathlib import Path
from uiautomation.uiautomation import (
    PaneControl,
    EditControl,
    GroupControl,
    CheckBoxControl,
)
from uiautomation import WindowControl, Click
from datetime import date
from time import sleep


class AccountingEntry:
    def __init__(self, accounting_entry_window: WindowControl):
        self.pane_group1: PaneControl = accounting_entry_window.PaneControl(
            searchDepth=1,
        )
        self.pane_group2: PaneControl = accounting_entry_window.PaneControl(
            searchDepth=1,
            foundIndex=2,
        )

    def _set_date(self, _date: date, group_control: GroupControl) -> None:
        month_edit = group_control.EditControl(searchDepth=1)
        date_edit = group_control.EditControl(searchDepth=1, foundIndex=2)
        year_select = group_control.PaneControl(searchDepth=1).EditControl(
            searchDepth=1
        )

        month_edit.SendKeys(f"{_date.month:02d}")
        date_edit.SendKeys(_date.strftime("%d%m%Y"))
        year_select.SendKeys(str(_date.year))
        if not (year_select.GetValuePattern().Value.strip() == str(_date.year)):
            raise ValueError("The year you are trying to select does not exist.")

    def set_date_and_type_operation(self, _date: date, type_operation: str) -> None:
        # AutomationId:	"22"

        group_setting: GroupControl = self.pane_group2.GroupControl(
            searchDepth=1, foundIndex=2
        )
        self._set_date(_date, group_setting)
        # type operation
        type_operation_select = group_setting.PaneControl(
            searchDepth=1, foundIndex=2
        ).EditControl(searchDepth=1)
        type_operation_select.SendKeys(type_operation)

        if not (
            type_operation_select.GetValuePattern().Value.strip() == type_operation
        ):
            raise ValueError("Type of operation does not exist.")

    def get_validation(self) -> None:
        """el boton se accion por referencia en las coordenadas ya que no se logra conseguir el boton en uiautomatition
        Para lograrlo, se captura primero el Checkbox de reemplazar y de alli se calculan las coordenadas para los botones de validacion y procesar
        """
        check_box_reference: CheckBoxControl = self.pane_group2.CheckBoxControl(
            searchDepth=1, foundIndex=1
        )

        rectangle = check_box_reference.BoundingRectangle
        # validar: y debe ser ese valor  mas 55
        # procesar: y debe ser ese valor  mas 125

        Click(x=rectangle.xcenter(), y=rectangle.ycenter() + 55)
        # se gestiona la  validacion

    def get_process_result(self) -> None:
        """se calcula la coordenadas del rectangulo de reemplazar y luego se calcula el boton de porcesar"""
        check_box_reference: CheckBoxControl = self.pane_group2.CheckBoxControl(
            searchDepth=1, foundIndex=1
        )

        rectangle = check_box_reference.BoundingRectangle

        Click(x=rectangle.xcenter(), y=rectangle.ycenter() + 125)
        ## se obtienen el resultado

    def set_file_path(self, file_path: str | Path) -> None:
        if isinstance(file_path, Path):
            file_path = str(file_path.resolve())

        dir_edit: EditControl = self.pane_group1.GroupControl(
            searchDepth=1, foundIndex=2
        ).EditControl(searchDepth=1)
        assert dir_edit.GetValuePattern().SetValue(file_path)


# ClassName:	"ImDateWndClass"
# ClassName:	"ImMaskWndClass"
