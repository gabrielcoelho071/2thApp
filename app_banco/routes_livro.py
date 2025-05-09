# app.py
import flet as ft
from models_livro import Livro, db_session  # Importando o modelo e a sessão
from sqlalchemy import select

def main(page: ft.Page):
    # Configuração da página
    page.title = "Gestão de Livros"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    # Função para salvar informações do livro
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
                descricao=input_descricao.value
            )
            obj_livro.save()  # Salva no banco
            input_livro.value = ""
            input_autor.value = ""
            input_categoria.value = ""
            input_descricao.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()


    def exibir_lista(e):
        lv_livros.controls.clear()
        livros = db_session.execute(select(Livro)).scalars().all()

        for livro in livros:
            lv_livros.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(f"Livro: {livro.livro}"),
                    subtitle=ft.Text(f"Autor: {livro.autor}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[ft.PopupMenuItem(text="Detalhes", on_click=lambda _, l=livro: exibir_detalhes(l))]
                    )
                )
            )
        page.update()

    # Função para exibir detalhes do livro
    def exibir_detalhes(livro):
        txt_categoria.value = livro.categoria
        txt_descricao.value = livro.descricao
        page.go("/detalhes")

    # Função para gerenciar rotas
    def gerencia_rotas(e):
        page.views.clear()

        # Tela Inicial
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Home"), bgcolor=ft.Colors.PRIMARY_CONTAINER),
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
                        on_click=lambda _: page.go("/livros")
                    )
                ],
            )
        )

        # Tela de Livros
        if page.route == "/livros":
            exibir_lista(e)
            page.views.append(
                ft.View(
                    "/livros",
                    [
                        ft.AppBar(title=ft.Text("Lista de Livros"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        lv_livros
                    ],
                )
            )

        # Tela de Detalhes do Livro
        if page.route == "/detalhes":
            page.views.append(
                ft.View(
                    "/detalhes",
                    [
                        ft.AppBar(title=ft.Text("Detalhes do Livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Text("Categoria:", size=15),
                        txt_categoria,
                        ft.Text("Descrição:", size=15),
                        txt_descricao,
                    ],
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Componentes de interface
    msg_sucesso = ft.SnackBar(content=ft.Text("Livro salvo com sucesso!"), bgcolor=ft.Colors.GREEN)
    msg_error = ft.SnackBar(content=ft.Text("Todos os campos são obrigatórios!"), bgcolor=ft.Colors.RED)

    input_livro = ft.TextField(label="Nome do Livro")
    input_autor = ft.TextField(label="Autor")
    input_categoria = ft.TextField(label="Categoria")
    input_descricao = ft.TextField(label="Descrição", multiline=True)

    lv_livros = ft.ListView(height=500, spacing=1, divider_thickness=1)

    txt_categoria = ft.Text("", size=15, weight=ft.FontWeight.W_400)
    txt_descricao = ft.Text("", size=15, weight=ft.FontWeight.W_400)

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)

# Iniciando o aplicativo Flet
ft.app(main)
