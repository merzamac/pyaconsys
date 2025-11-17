from uiautomation import WindowControl

LOGIN_WINDOW = WindowControl(searchDepth=1, Name="Acceso al Sistema")

_LOGIN_PANE = LOGIN_WINDOW.PaneControl(searchDepth=1, Name="")
_USER_GROUP = _LOGIN_PANE.GroupControl(searchDepth=1, Name="Información de Usuario")

USERNAME_EDIT = _USER_GROUP.EditControl(searchDepth=1, AutomationId="2")
PASSWORD_EDIT = _USER_GROUP.EditControl(searchDepth=1, AutomationId="3")
CONNECT_BUTTON = _LOGIN_PANE.ButtonControl(searchDepth=1, Name="Conectar")
