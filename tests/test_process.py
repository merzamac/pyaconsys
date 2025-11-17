from aconsys.views.login.window import LoginWindow


def test_go_to_compras_view(executable_file, username, password) -> None:
    login_window = LoginWindow(executable_file)
    main_window = login_window.login(username, password)
    main_window.register_purchase_one_by_one(
        "01",
        "20554144676",
        "01",
        "01",
        "11/02/2025",
        "CONCEPTO OC 429",
        "F001",
        "575",
        "4211103",
        "104.70",
        True,
        "001",
        "10/11/2025",
    )
