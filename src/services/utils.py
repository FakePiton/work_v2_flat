import flet as ft

def show_snackbar(page: ft.Page, text: str, color: ft.Colors):
    snackbar = ft.SnackBar(
        content=ft.Text(text),
        bgcolor=color,
        behavior=ft.SnackBarBehavior.FLOATING,
        open=True
    )
    page.overlay.append(snackbar)
    page.snack_bar = snackbar
    page.update()
