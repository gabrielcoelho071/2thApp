import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors
from models_livro import Livro, Usuario, Emprestimo, local_session  # Importando o modelo e a sessão
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import requests


# Função para criar uma nova sessão
def create_session():
    Session = sessionmaker(bind=local_session.bind)  # Usando o bind da sessão existente
    return Session()

def main(page: ft.Page):
    # Configuração da página
    page.title = "Gestão de Livros"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    # Função que retorna somente o JSON da rota
    def get_livro():
        url = f"http://192.168.0.19:5000/livros"

        resposta = requests.get(url)

        if resposta.status_code == 200:
            print("Info Livros:", resposta.json())
            return resposta.json()
        else:
            return resposta.json()

    def post_livro(titulo, autor, ISBN, resumo):

        url = "http://192.168.0.19:5000/livros"
        livro = {
            "titulo": titulo,
            "autor": autor,
            "categoria": ISBN,
            "descricao": resumo,
        }

        resposta = requests.post(url, json=livro)
        print("Status:", resposta.status_code)
        print("Texto bruto:", repr(resposta.text))
        try:
            print("JSON:", resposta.json())
        except Exception as e:
            print("Erro ao parsear JSON da resposta:", e)

    def put_livro(id_, titulo, autor, ISBN, resumo):
        url = f"http://192.168.0.19:5000/livros/{id_}"
        livro_atualizado = {
            "titulo": titulo,
            "autor": autor,
            "ISBN": ISBN,
            "resumo": resumo,
        }
        print(livro_atualizado)
        antigo = requests.get(url)
        resposta = requests.put(url, json=livro_atualizado)
        print("Status:", resposta.status_code)
        print("Texto bruto:", repr(resposta.text))
        try:
            print("JSON:", resposta.json())
        except Exception as e:
            print("Erro ao parsear JSON da resposta:", e)

    # Função para gerenciar rotas
    def gerencia_rotas(e):
        page.views.clear()

        # Tela Inicial
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Home"), bgcolor=ft.Colors.PRIMARY_CONTAINER),
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=10,
                        content=ft.Column(
                            [
                                ft.Image(
                                    src="https://cdn-icons-png.flaticon.com/256/9043/9043296.png",
                                    # pode ser URL ou caminho local
                                    width=300,
                                    height=200,
                                    fit=ft.ImageFit.CONTAIN
                                ),
                                ft.Text("Descubra, escolha.\ne Leia.", size=38, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                ft.Container(height=80),
                                ft.CupertinoButton(
                                    text="Livros",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/sign_in")
                                ),
                                ft.CupertinoButton(
                                    text="Usuarios",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/sign_in")
                                ),
                                ft.CupertinoButton(
                                    text="Empréstimos",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/sign_in")
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                ],
            )
        )

        # # Tela de Livros
        # if page.route == "/livros" or page.route == "/editar" or page.route == "/detalhes":
        #     exibir_lista(e)
        #     page.views.append(
        #         ft.View(
        #             "/livros",
        #             [
        #                 ft.AppBar(title=ft.Text("Lista de Livros"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
        #                 lv_livros
        #             ],
        #         )
        #     )
        #
        # if page.route == "/editar":
        #     page.views.append(
        #         ft.View(
        #             "/editar",
        #             [
        #                 ft.AppBar(title=ft.Text("Editar livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
        #                 txt_id,
        #                 input_livro,
        #                 input_autor,
        #                 input_categoria,
        #                 input_descricao,
        #                 ft.Row(
        #                     controls=[
        #                         ft.ElevatedButton(
        #                             text="Salvar",
        #                             on_click=lambda _: editar_informacoes(int(txt_id.value))
        #                         ),
        #                         ft.ElevatedButton(
        #                             text="Exibir Lista",
        #                             on_click=lambda _: page.go("/livros")
        #                         )
        #                     ]
        #                 )
        #             ],
        #         )
        #     )
        #
        # # Tela de Detalhes do Livro
        # if page.route == "/detalhes":
        #     page.views.append(
        #         ft.View(
        #             "/detalhes",
        #             [
        #                 ft.AppBar(title=ft.Text("Detalhes do Livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
        #                 ft.Text("Categoria:", size=15),
        #                 txt_categoria,
        #                 ft.Text("Descrição:", size=15),
        #                 txt_descricao,
        #             ],
        #         )
        #     )
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

    txt_id = ft.Text("", size=15, weight=ft.FontWeight.W_400)
    txt_categoria = ft.Text("", size=15, weight=ft.FontWeight.W_400)
    txt_descricao = ft.Text("", size=15, weight=ft.FontWeight.W_400)

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)

# Iniciando o aplicativo Flet
ft.app(main)
