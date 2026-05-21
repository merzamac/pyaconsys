from uiautomation import WindowControl

SELECTION_WINDOW = WindowControl(searchDepth=1, Name="Seleccione Empresa")
_AREA_SELECTION = SELECTION_WINDOW.GroupControl(
    searchDepth=2, Name="Relación de empresas"
)
