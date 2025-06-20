import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors
from models_livro import Livro, db_session  # Importando o modelo e a sessão
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import requests


# Função para criar uma nova sessão
def create_session():
    Session = sessionmaker(bind=db_session.bind)  # Usando o bind da sessão existente
    return Session()


def main(page: ft.Page):
    # Configuração da página
    page.title = "Gestão de Livros"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    # Função que retorna somente o JSON da rota
    def get_info():
        url = f"http://192.168.0.19:5000/livros"

        resposta = requests.get(url)

        if resposta.status_code == 200:
            print("Info Livros:", resposta.json())
            return resposta.json()
        else:
            return resposta.json()

    def post_info(livros, autor, categoria, descricao):

        url = "http://192.168.0.19:5000/livros"
        livro = {
            "livro": livros,
            "autor": autor,
            "categoria": categoria,
            "descricao": descricao,
        }

        resposta = requests.post(url, json=livro)
        print("Status:", resposta.status_code)
        print("Texto bruto:", repr(resposta.text))
        try:
            print("JSON:", resposta.json())
        except Exception as e:
            print("Erro ao parsear JSON da resposta:", e)

    def put_info(id_, livros, autor, categoria, descricao):
        url = f"http://192.168.0.19:5000/livros/{id_}"
        livro_atualizado = {
            "livro": livros,
            "autor": autor,
            "categoria": categoria,
            "descricao": descricao,
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

    def delete_info(id_):

        url = f"http://192.168.0.19:5000/livros/{id_}"

        resposta = requests.delete(url)

        if resposta.status_code == 200:
            print("Info Livros:", resposta.json())
            return resposta.json()
        else:
            return resposta.json()

    def excluir_livro(livro_id):
        delete_info(livro_id)
        exibir_lista(None)  # Atualiza a lista após excluir

    # Função para salvar informações do livro
    def editar_informacoes(id):
        if input_livro.value == "" or input_autor.value == "" or input_categoria.value == "" or input_descricao.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            # Criando uma nova sessão
            session = create_session()

            try:
                print("helloooo")
                print(id, input_livro.value, input_autor.value, input_categoria.value, input_descricao.value)
                put_info(id, input_livro.value, input_autor.value, input_categoria.value, input_descricao.value)

                # Limpando os campos após salvar
                input_livro.value = ""
                input_autor.value = ""
                input_categoria.value = ""
                input_descricao.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()

            except Exception as e:
                print(f"Erro ao salvar as informações: {e}")
                session.rollback()
            finally:
                session.close()  # Fechar a sessão

    # Função para salvar informações do livro
    def salvar_informacoes(e):
        if input_livro.value == "" or input_autor.value == "" or input_categoria.value == "" or input_descricao.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            # Criando uma nova sessão
            session = create_session()

            try:
                post_info(input_livro.value, input_autor.value, input_categoria.value, input_descricao.value)

                # Limpando os campos após salvar
                input_livro.value = ""
                input_autor.value = ""
                input_categoria.value = ""
                input_descricao.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()

            except Exception as e:
                print(f"Erro ao salvar as informações: {e}")
                session.rollback()
            finally:
                session.close()  # Fechar a sessão


    def exibir_lista(e):
        lv_livros.controls.clear()

        # Criando uma nova sessão
        session = create_session()

        try:
            # Carregando os livros do banco de dados
            dados = get_info()

            for livro in dados:
                lv_livros.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK),
                        title=ft.Text(f"Livro: {livro["livro"]}"),
                        subtitle=ft.Text(f"Autor: {livro["autor"]}"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="Detalhes", on_click=lambda _, l=livro: exibir_detalhes(l)),
                                ft.PopupMenuItem(text="editar", on_click=lambda _, l=livro: exibir_editar(l)),
                                ft.PopupMenuItem(text="Excluir", on_click=lambda _, l=livro: excluir_livro(l["id_livro"]))

                            ],
                        )
                    )
                )
            page.update()

        except Exception as e:
            print(f"Erro ao exibir a lista de livros: {e}")
        finally:
            session.close()  # Fechar a sessão

    # Função para exibir detalhes do livro
    def exibir_detalhes(livro):
        txt_categoria.value = livro["categoria"]
        txt_descricao.value = livro["descricao"]
        page.go("/detalhes")

    def exibir_editar(livro):
        print("valores:", livro["livro"], livro["autor"], livro["categoria"], livro["descricao"])
        txt_id.value = livro["id_livro"]
        input_livro.value = livro["livro"]
        input_autor.value = livro["autor"]
        input_categoria.value = livro["categoria"]
        input_descricao.value = livro["descricao"]
        page.go("/editar")


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
                        content=ft.Image(
                            src="https://cdn-icons-png.flaticon.com/256/9043/9043296.png",
                            # pode ser URL ou caminho local
                            width=300,
                            height=200,
                            fit=ft.ImageFit.CONTAIN
                        ),
                    ),
                    input_livro,
                    input_autor,
                    input_categoria,
                    input_descricao,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Salvar",
                                on_click=lambda _: salvar_informacoes(e)
                            ),
                            ft.ElevatedButton(
                                text="Exibir Lista",
                                on_click=lambda _: page.go("/livros")
                            )
                        ]
                    )

                ],
            )
        )

        # Tela de Livros
        if page.route == "/livros" or page.route == "/editar" or page.route == "/detalhes":
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

        if page.route == "/editar":
            page.views.append(
                ft.View(
                    "/editar",
                    [
                        ft.AppBar(title=ft.Text("Editar livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        txt_id,
                        input_livro,
                        input_autor,
                        input_categoria,
                        input_descricao,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Salvar",
                                    on_click=lambda _: editar_informacoes(int(txt_id.value))
                                ),
                                ft.ElevatedButton(
                                    text="Exibir Lista",
                                    on_click=lambda _: page.go("/livros")
                                )
                            ]
                        )
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

    txt_id = ft.Text("", size=15, weight=ft.FontWeight.W_400)
    txt_categoria = ft.Text("", size=15, weight=ft.FontWeight.W_400)
    txt_descricao = ft.Text("", size=15, weight=ft.FontWeight.W_400)

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)


# Iniciando o aplicativo Flet
ft.app(main)
