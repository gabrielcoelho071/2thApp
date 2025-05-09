import flet as ft
from flet import *

class Livro():
    def __init__(self, livro, autor, categoria, descricao):
        self.livro = livro
        self.autor = autor
        self.categoria = categoria
        self.descricao = descricao

def main(page: ft.Page):
    # Configuração de página
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }

    listas = []

    def salvar_informacoes(e):
        if input_livro.value == "" or input_autor.value == "" or input_categoria.value == "" or input_descricao.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            obj_livro = Livro(
                livro=input_livro.value,
                autor=input_autor.value,
                categoria=input_categoria.value,
                descricao=input_descricao.value)
            listas.append(obj_livro)
            input_livro.value = ""
            input_autor.value = ""
            input_categoria.value = ""
            input_descricao.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()

    def exibir_lista(e):
        lv_livros.controls.clear()
        for livro in listas:
            lv_livros.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f"Livro: {livro.livro}"),
                    subtitle=ft.Text(f"Autor: {livro.autor}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="Detalhes", on_click=lambda _, l=livro: exibir_detalhes(l))
                        ],
                    )
                )
            )
        page.update()

    def exibir_detalhes(livro):
        txt_categoria.value = livro.categoria
        txt_descricao.value = livro.descricao
        page.go("/terceira")

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PRIMARY_CONTAINER),
                    input_livro,
                    input_autor,
                    input_categoria,
                    input_descricao,
                    ft.ElevatedButton(
                        text="Salvar",
                        on_click=lambda _: salvar_informacoes(e)
                    ),
                    ft.ElevatedButton(
                        text="Exibir Lista",
                        on_click=lambda _: page.go("/segunda"),
                    )
                ],
            )
        )
        if page.route == "/segunda" or page.route == "/terceira":
            exibir_lista(e)
            page.views.append(
                View(
                    "/segunda",
                    [
                        AppBar(title=Text("Lista de Livros"), bgcolor=Colors.SECONDARY_CONTAINER),
                        lv_livros
                    ],
                )
            )
        if page.route == "/terceira":
            page.views.append(
                View(
                    "/terceira",
                    [
                        AppBar(title=Text("Detalhes do Livro"), bgcolor=Colors.SECONDARY_CONTAINER),
                        ft.Text("Categoria:", font_family="RobotoSlab", size=15),
                        txt_categoria,
                        ft.Text("Descrição:", font_family="RobotoSlab", size=15),
                        txt_descricao,
                    ],
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Componentes
    msg_sucesso = ft.SnackBar(
        content=ft.Text("Livro salvo com sucesso!"),
        bgcolor=Colors.GREEN
    )
    msg_error = ft.SnackBar(
        content=ft.Text("Todos os campos são obrigatórios!"),
        bgcolor=Colors.RED
    )

    input_livro = ft.TextField(label="Nome do Livro")
    input_autor = ft.TextField(label="Autor")
    input_categoria = ft.TextField(label="Categoria")
    input_descricao = ft.TextField(label="Descrição", multiline=True)

    lv_livros = ft.ListView(
        height=500,
        spacing=1,
        divider_thickness=1
    )

    txt_categoria = ft.Text(
        "",
        size=15,
        font_family="RobotoSlab",
        weight=ft.FontWeight.W_400,
    )
    txt_descricao = ft.Text(
        "",
        size=15,
        font_family="RobotoSlab",
        weight=ft.FontWeight.W_400,
    )

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)

ft.app(main)