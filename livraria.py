import flet as ft
from flet.core.app_bar import AppBar
from flet.core.colors import Colors
from flet.core.elevated_button import ElevatedButton
from flet.core.textfield import TextField


def main(page: ft.Page):
    page.title = "Livraria"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    AppBar(title=ft.Text("Home"), bgcolor=Colors.PRIMARY_CONTAINER),
                    input_title,
                    input_subtitle,
                    input_category,
                    input_author,
                    ElevatedButton(text="Adicionar", on_click=lambda _: page.go("/segunda")),
                ],
            )

        )
        if page.route == "/segunda":
            page.views.append(
                ft.View(
                    "/segunda",
                    [
                        AppBar(title=ft.Text("Segunda tela"), bgcolor=Colors.SECONDARY_CONTAINER),
                        ft.Text(value=f"Livro: {input_title.value}!"),
                        ft.Text(value=f"Descrição: {input_subtitle.value}!"),
                        ft.Text(value=f"Categoria: {input_category.value}!"),
                        ft.Text(value=f"Nome do autor: {input_author.value}!"),
                    ],
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    input_title = TextField(label="Insira o título do livro",hint_text="Título")
    input_subtitle = TextField(label="Insira a descrição", hint_text="Descrição")
    input_category = TextField(label="Insira a categoria", hint_text="Categoria")
    input_author = TextField(label="Insira o autor", hint_text="Nome do autor")
    

    page.go(page.route)

ft.app(main)