import time
from datetime import date, datetime
from time import sleep

from uiautomation import SendKeys, WindowControl

from aconsys.base.window import TopLevelWindow
from aconsys.views.main.controls import MAIN_WINDOW
from aconsys.views.accounting_entry.window import AccountingEntry


class MainWindow(TopLevelWindow):
    """There are many elements here taht are only differentiated by AutomationId"""

    _window = MAIN_WINDOW

    # def __init__(self) -> None:
    #     self.change_work_period()

    def _navigate_to_menu_option(self, menu_name: str, option_name: str) -> None:
        """
        Opens a menu option (e.g. 'Tablas' - 'Centro de Costos') from the main window.
        It works for classic menus of ACONSYS.
        """
        self._window.SetActive()
        self._window.SetTopmost(True)

        menu_bar = self._window.MenuBarControl(searchDepth=1, AutomationId="MenuBar")

        menu_item = menu_bar.MenuItemControl(searchDepth=1, Name=menu_name)
        assert menu_item.GetInvokePattern().Invoke()

        menu_tables = self._window.MenuControl(searchDepth=1, Name=menu_name)

        option_item = menu_tables.MenuItemControl(searchDepth=1, Name=option_name)
        assert option_item.GetInvokePattern().Invoke()

    def accounting_entry_process_from_excel(
        self,
    ) -> AccountingEntry:
        self._navigate_to_menu_option("Procesos", "Asientos desde Excel")

        pane_work_area = self._window.PaneControl(searchDepth=1, Name="Área de trabajo")
        accounting_entry_process = pane_work_area.WindowControl(
            searchDepth=1, Name="Proceso de Importación del Excel 2003"
        )
        return AccountingEntry(accounting_entry_process)

    def change_work_period(self, date: date):
        """
        Abre 'Configuraciones -> Cambio Periodo de Trabajo' y selecciona el mes actual.
        """
        menu_name = "Configuraciones"
        option_name = "Cambio Periodo de Trabajo	Ctrl+I"

        self._window.SetActive()
        self._window.SetTopmost(True)

        menu_bar = self._window.MenuBarControl(searchDepth=1, AutomationId="MenuBar")

        menu_item = menu_bar.MenuItemControl(searchDepth=1, Name=menu_name)
        assert menu_item.GetInvokePattern().Invoke()

        tablas_menu = self._window.MenuControl(searchDepth=1, Name=menu_name)

        option_item = tablas_menu.MenuItemControl(searchDepth=1, Name=option_name)
        assert option_item.GetInvokePattern().Invoke()

        time.sleep(5)

        ventana_mes = self._window.WindowControl(
            searchDepth=1, Name="Cambio de Periodo de Trabajo"
        )

        panel_mes = ventana_mes.PaneControl(
            searchDepth=1, ClassName="ImFrame3DWndClass"
        )
        self._window.SetTopmost(True)
        cuadro_mes = panel_mes.GroupControl(searchDepth=1, ClassName="ThunderRT6Frame")

        rellenar_cuadro = cuadro_mes.EditControl(searchDepth=1, AutomationId="3")

        month_work_period = date.strftime("%m")
        year_work_period = date.strftime("%Y")

        rellenar_cuadro.GetValuePattern().SetValue(month_work_period)

        cuadro_año = cuadro_mes.EditControl(searchDepth=1, AutomationId="2")
        cuadro_año.GetValuePattern().SetValue(year_work_period)
        cuadro_año.SetFocus()
        time.sleep(0.3)

        SendKeys("{TAB}")
        time.sleep(0.5)
        SendKeys("{ENTER}")

        aceptar = ventana_mes.WindowControl(searchDepth=1, Name="ACONSYS")
        aceptar_boton = aceptar.ButtonControl(searchDepth=1, Name="Aceptar")
        assert aceptar_boton.GetInvokePattern().Invoke()

    def download_centro_costos_file(self, file_name: str) -> None:
        window = self._window.WindowControl(
            Name="Mantenimiento de Centro de Costos", searchDepth=1
        )

        panel = window.PaneControl(searchDepth=1, ClassName="ImFrame3DWndClass")

        print_button = panel.ButtonControl(searchDepth=1, Name="Imprimir")
        assert print_button.GetInvokePattern().Invoke()

        print_window = WindowControl(searchDepth=1, Name="Imprimir")

        print_panel = print_window.PaneControl(
            ClassName="SHELLDLL_DefView", searchDepth=1
        )

        select_box_pdf = print_panel.ListControl(
            Name="Vista de carpetas", searchDepth=1
        )

        item_pdf_click = select_box_pdf.ListItemControl(
            searchDepth=1, Name="Microsoft Print to PDF"
        )
        assert item_pdf_click.GetSelectionItemPattern()

        inner_print_button = print_window.ButtonControl(searchDepth=1, Name="Imprimir")
        assert inner_print_button.GetInvokePattern().Invoke()

        main_window = self._window.PaneControl(searchDepth=1, Name="Área de trabajo")

        window = main_window.WindowControl(searchDepth=1, ClassName="ThunderRT6FormDC")

        panel_window = window.PaneControl(searchDepth=1, Name="")

        main_bar = panel_window.TextControl(searchDepth=1, Name="")

        oficial_bar = main_bar.PaneControl(searchDepth=1, Name="")
        # Has many siblings
        toolbar = oficial_bar.ToolBarControl(
            searchDepth=1, AutomationId="203"
        )  # ID could change

        export_icon = toolbar.ButtonControl(searchDepth=1, Name="Exportar informe")
        assert export_icon.GetInvokePattern().Invoke()

        export_window = self._window.WindowControl(searchDepth=1, Name="Export")

        ok_export_button = export_window.ButtonControl(searchDepth=1, Name="OK")
        assert ok_export_button.GetInvokePattern().Invoke()

        export_options = self._window.WindowControl(
            searchDepth=1, Name="Export Options"
        )

        second_ok_export_button = export_options.ButtonControl(searchDepth=1, Name="OK")
        assert second_ok_export_button.GetInvokePattern().Invoke()

        save_window = self._window.WindowControl(
            searchDepth=1, Name="Choose export file"
        )

        pdf_name_chart = save_window.PaneControl(
            searchDepth=1, Name="RptTablasComunConta"
        )

        select_pdf_name = pdf_name_chart.ComboBoxControl(searchDepth=1, Name="Nombre:")

        input_pdf_name = select_pdf_name.EditControl(searchDepth=1, Name="Nombre:")

        input_pdf_name.GetValuePattern().SetValue(file_name)

        save_button = save_window.ButtonControl(searchDepth=1, Name="Guardar")
        assert save_button.GetInvokePattern().Invoke()

    def register_purchase_one_by_one(
        self,
        receipt_number: str,
        supplier_number: str,
        currency_type: str,
        receipt_type: str,
        issue_date: str,
        concept: str,
        serie: str,
        receipt_number_from_invoice: str,
        account_number: str,
        sale_value: str,
        has_detraction: bool,
        type_detraction: str | None,
        payment_date: str | None,
    ):
        self._navigate_to_menu_option("Movimientos", "Compras")

        _pane_work_area = self._window.PaneControl(
            searchDepth=1, Name="Área de trabajo"
        )
        _record_puerchase_window = _pane_work_area.WindowControl(
            searchDepth=1, Name="Registro de compras locales"
        )

        group_18 = _record_puerchase_window.GroupControl(
            searchDepth=1, AutomationId="18"
        )

        receipt_number_pane = group_18.PaneControl(
            searchDepth=1, AutomationId="3", foundIndex=3
        )
        receipt_number_edit = receipt_number_pane.EditControl(searchDepth=1, Name="")
        receipt_number_edit.SendKeys(receipt_number + "{ENTER}", interval=0.5)

        supplier_number_edit = group_18.EditControl(
            searchDepth=1, Name="", foundIndex=8
        )
        supplier_number_edit.GetValuePattern().SetValue(supplier_number)

        autocomplete_supplier_name_btn = group_18.ButtonControl(
            searchDepth=1, AutomationId="35"
        )
        autocomplete_supplier_name_btn.GetInvokePattern().Invoke()

        currency_type_pane = group_18.PaneControl(
            searchDepth=1, AutomationId="3", foundIndex=2
        )
        currency_type_edit = currency_type_pane.EditControl(searchDepth=1, Name="")
        currency_type_edit.SendKeys(currency_type + "{ENTER}", interval=0.5)

        receipt_type_pane = group_18.PaneControl(
            searchDepth=1, AutomationId="3", foundIndex=1
        )
        receipt_type_edit = receipt_type_pane.EditControl(searchDepth=1, Name="")
        receipt_type_edit.SendKeys(receipt_type + "{ENTER}", interval=0.5)

        issue_date_edit = group_18.EditControl(
            searchDepth=1, ClassName="ImDateWndClass", foundIndex=3
        )
        issue_date_edit.SendKeys(issue_date)

        due_date = date.today().strftime("%d/%m/%Y")
        due_date_edit = group_18.EditControl(
            searchDepth=1, ClassName="ImDateWndClass", foundIndex=1
        )
        due_date_edit.SendKeys(due_date)

        concept_type_pane = group_18.PaneControl(
            searchDepth=1, AutomationId="3", foundIndex=4
        )
        concept_type_edit = concept_type_pane.EditControl(searchDepth=1, Name="")
        concept_type_edit.GetValuePattern().SetValue("**")

        concept_edit = group_18.EditControl(
            searchDepth=1, ClassName="ImTextWndClass", foundIndex=5
        )
        concept_edit.GetValuePattern().SetValue(concept)

        serie_edit = group_18.EditControl(
            searchDepth=1, ClassName="ImMaskWndClass", foundIndex=1
        )
        serie_edit.SendKeys(serie)

        receipt_number_from_invoice_edit = group_18.EditControl(
            searchDepth=1, ClassName="ImMaskWndClass", foundIndex=2
        )
        receipt_number_from_invoice_edit.SendKeys(receipt_number_from_invoice)

        table_pane = _record_puerchase_window.PaneControl(
            searchDepth=1, AutomationId="1"
        )
        assert table_pane.SetFocus()
        table_pane.SendKeys("{SPACE}")

        edit_from_table = table_pane.EditControl(searchDepth=1, Name="")
        assert edit_from_table.SetFocus()
        edit_from_table.SendKeys(
            f"{account_number}"
            + "{TAB}"
            + f"{supplier_number}"
            + "{RIGHT}" * 5
            + f"{sale_value}"
            + "{ENTER}",
        )

        if has_detraction and type_detraction and payment_date:

            _tool_bar_pane_1 = _record_puerchase_window.PaneControl(
                searchDepth=1, ClassName="ToolbarWndClass", foundIndex=1
            )
            _tool_bar = _tool_bar_pane_1.ToolBarControl(searchDepth=1, Name="")
            button_spot = _tool_bar.ButtonControl(
                searchDepth=1, Name="Datos Comprobanteb SPOT"
            )
            assert button_spot.GetInvokePattern().Invoke()

            _datos_comprobante_spot_window = self._window.WindowControl(
                searchDepth=1, Name="Datos adicionales SPOT - Voucher No.-"
            )
            assert _datos_comprobante_spot_window.SetTopmost()

            _type_detraction_pane = _datos_comprobante_spot_window.PaneControl(
                searchDepth=1, AutomationId="3"
            )
            type_detraction_edit = _type_detraction_pane.EditControl(
                searchDepth=1, Name=""
            )
            type_detraction_edit.SendKeys(type_detraction)

            _reference_group = _datos_comprobante_spot_window.GroupControl(
                searchDepth=1, Name="Referencia"
            )

            deposit_date_edit = _reference_group.EditControl(
                searchDepth=1, ClassName="ImDateWndClass"
            )

            deposit_date_edit.SendKeys(payment_date + "{TAB}" * 2 + "{ENTER}")

        _tool_bar_pane_2 = _record_puerchase_window.PaneControl(
            searchDepth=1, ClassName="ToolbarWndClass", foundIndex=2
        )
        _tool_bar_to_save = _tool_bar_pane_2.ToolBarControl(
            searchDepth=1, ClassName="ToolbarWindow32"
        )
        save_button = _tool_bar_to_save.ButtonControl(
            searchDepth=1, Name="Grabar compra local"
        )
        assert save_button.GetInvokePattern().Invoke()

        clear_form_button = _tool_bar_to_save.ButtonControl(
            searchDepth=1, Name="Nueva compra local"
        )
        clear_form_button.GetInvokePattern().Invoke()
