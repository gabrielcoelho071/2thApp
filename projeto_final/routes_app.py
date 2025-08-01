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
    def get_info(endpoint):
        print(endpoint)
        url = f"http://10.135.235.26:5000/{endpoint}"
        print(url)

        resposta = requests.get(url)

        if resposta.status_code == 200:
            print("Info Livros:", resposta.json())
            return resposta.json()
        else:
            return resposta.json()


    # ------------------ CRUD DO LIVRO ------------------

    def post_livro(titulo, autor, ISBN, resumo):

        url = "http://10.135.235.26:5000/livros"
        livro = {
            "titulo": titulo,
            "autor": autor,
            "ISBN": ISBN,
            "resumo": resumo,
        }

        resposta = requests.post(url, json=livro)
        print("Status:", resposta.status_code)
        print("Texto bruto:", repr(resposta.text))
        try:
            print("JSON:", resposta.json())
        except Exception as e:
            print("Erro ao parsear JSON da resposta:", e)

    def put_livro(id_, titulo, autor, ISBN, resumo):
        url = f"http://10.135.235.26:5000/livros/{id_}"
        livro_atualizado = {
            "titulo": titulo,
            "autor": autor,
            "ISBN": ISBN,
            "resumo": resumo,
        }
        print(livro_atualizado)
        resposta = requests.put(url, json=livro_atualizado)
        print("Status:", resposta.status_code)
        try:
            print("JSON:", resposta.json())
        except Exception as e:
            print("Erro ao parsear JSON da resposta:", e)

    # Função para exibir detalhes do livro
    def livro_exibir_detalhes(livro):
        txt_ISBN.value = livro["ISBN"]
        txt_resumo.value = livro["resumo"]
        page.go("/livros_detalhes")

    def livro_exibir_editar(livro):
        print("valores:", livro["titulo"], livro["autor"], livro["ISBN"], livro["resumo"])
        txt_id.value = livro["id_livro"]
        input_titulo.value = livro["titulo"]
        input_autor.value = livro["autor"]
        input_ISBN.value = livro["ISBN"]
        input_resumo.value = livro["resumo"]
        page.go("/editar_livros")

    # Função para editar informações do livro
    def editar_livros(id):
        if input_titulo.value == "" or input_autor.value == "" or input_ISBN.value == "" or input_resumo.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            # Criando uma nova sessão
            session = create_session()

            try:
                print(id, input_titulo.value, input_autor.value, input_ISBN.value, input_resumo.value)
                put_livro(id, input_titulo.value, input_autor.value, input_ISBN.value, input_resumo.value)

                # Limpando os campos após salvar
                input_titulo.value = ""
                input_autor.value = ""
                input_ISBN.value = ""
                input_resumo.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()

            except Exception as e:
                print(f"Erro ao salvar as informações: {e}")
                session.rollback()
            finally:
                session.close()  # Fechar a sessão

    # Função para salvar informações do livro
    def salvar_livros(e):
        if input_titulo.value == "" or input_autor.value == "" or input_ISBN.value == "" or input_resumo.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            # Criando uma nova sessão
            session = create_session()

            try:
                post_livro(input_titulo.value, input_autor.value, input_ISBN.value, input_resumo.value)

                # Limpando os campos após salvar
                input_titulo.value = ""
                input_autor.value = ""
                input_ISBN.value = ""
                input_resumo.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()

            except Exception as e:
                print(f"Erro ao salvar as informações: {e}")
                session.rollback()
            finally:
                session.close()  # Fechar a sessão

    #Função para exibir o Livro
    def exibir_livro(e):
        lv_livros.controls.clear()

        # Criando uma nova sessão
        session = create_session()

        try:
            # Carregando os livros do banco de dados
            dados = get_info(endpoint="livros")

            for livro in dados:
                lv_livros.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK),
                        title=ft.Text(f"Título: {livro["titulo"]}"),
                        subtitle=ft.Text(f"Autor: {livro["autor"]}"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="Detalhes", on_click=lambda _, l=livro: livro_exibir_detalhes(l)),
                                ft.PopupMenuItem(text="editar", on_click=lambda _, l=livro: livro_exibir_editar(l)),
                            ],
                        )
                    )
                )
            page.update()

        except Exception as e:
            print(f"Erro ao exibir a lista de livros: {e}")
        finally:
            session.close()  # Fechar a sessão

    # ------------------ CRUD DO USUARIO ------------------

    # Funções para Usuário
    def post_usuario(nome, email, CPF, endereco):
        url = "http://192.168.0.19:5000/usuarios"
        print(nome, email, CPF, endereco)
        dados = {"nome": nome, "email": email, "CPF": CPF, "endereco": endereco}
        resposta = requests.post(url, json=dados)
        print(resposta.status_code, resposta.text)
        if resposta.status_code == 200:
            print("Info Livros:", resposta.json())
            return resposta.json()
        elif resposta.status_code == 422:
            page.overlay.append(msg_len_error)
            msg_len_error.open = True
            page.update()
            return resposta.json()
        elif resposta.status_code == 400:
            page.overlay.append(msg_integrity_error)
            msg_integrity_error.open = True
            page.update()
            return resposta.json()
        else:
            page.overlay.append(msg_idk_error)
            msg_idk_error.open = True
            page.update()
            return resposta.json()



    def put_usuario(id_, nome, email, CPF, endereco):
        url = f"http://192.168.0.19:5000/usuarios/{id_}"
        dados = {"nome": nome, "email": email, "CPF": CPF, "endereco": endereco}
        r = requests.put(url, json=dados);
        print(r.status_code, r.text)

    # Exibição e edição
    def usuario_exibir_detalhes(usuario):
        txt_user_cpf.value = usuario["CPF"]
        txt_user_endereco.value = usuario["endereco"]
        page.go("/usuario_detalhes")

    def usuario_exibir_editar(usuario):
        txt_user_id.value = usuario["id_usuario"]
        input_nome.value = usuario["nome"]
        input_email.value = usuario["email"]
        input_cpf.value = usuario["CPF"]
        input_endereco.value = usuario["endereco"]
        page.go("/editar_usuario")

    # Função para editar informações do usuario
    def editar_usuarios(id):
        if input_nome.value == "" or input_email.value == "" or input_cpf.value == "" or input_endereco.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            # Criando uma nova sessão
            session = create_session()

            try:
                print(id, input_nome.value, input_email.value, input_cpf.value, input_endereco.value)
                put_livro(id, input_nome.value, input_email.value, input_cpf.value, input_endereco.value)

                # Limpando os campos após salvar
                input_nome.value = ""
                input_email.value = ""
                input_cpf.value = ""
                input_endereco.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()

            except Exception as e:
                print(f"Erro ao salvar as informações: {e}")
                session.rollback()
            finally:
                session.close()  # Fechar a sessão

    # Função para salvar informações do usuario
    def salvar_usuarios(e):
        if input_nome.value == "" or input_email.value == "" or input_cpf.value == "" or input_endereco.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            # Criando uma nova sessão
            session = create_session()

            try:
                post_usuario(input_nome.value, input_email.value, input_cpf.value, input_endereco.value)

                # Limpando os campos após salvar
                input_nome.value = ""
                input_email.value = ""
                input_cpf.value = ""
                input_endereco.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()

            except Exception as e:
                print(f"Erro ao salvar as informações: {e}")
                session.rollback()
            finally:
                session.close()  # Fechar a sessão

    def exibir_usuarios(e):
        lv_usuarios.controls.clear()
        for usuario in get_info(endpoint="usuarios"):
            lv_usuarios.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f"{usuario['nome']}"),
                    subtitle=ft.Text(f"{usuario['email']}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="Detalhes", on_click=lambda _, usu=usuario: usuario_exibir_detalhes(usu)),
                            ft.PopupMenuItem(text="Editar", on_click=lambda _, usu=usuario: usuario_exibir_editar(usu)),
                        ],
                    )
                )
            )
        page.update()

    # ------------------ CRUD DO EMPRESTIMO ------------------

    # Funções para Empréstimo
    def post_emprestimo(id_usuario, id_livro, data_emprestimo, data_devolucao):
        url = "http://192.168.0.19:5000/emprestimos"
        dados = {
            "usuario_id": id_usuario,
            "livro_id": id_livro,
            "data_emprestimo": data_emprestimo,
            "data_devolucao": data_devolucao
        }
        r = requests.post(url, json=dados);
        print(r.status_code, r.text)

    # Exibição e edição
    def emprestimo_exibir_detalhes(e_):
        txt_emp_detalhes.value = f"Usuario: {e_['usuario_id']} — Livro: {e_['livro_id']} — De: {e_['data_emprestimo']} Até: {e_['data_devolucao']}"
        page.go("/emprestimos_detalhes")

    def exibir_emprestimos(e):
        lv_emprestimos.controls.clear()
        for em_ in get_info(endpoint="emprestimos"):
            lv_emprestimos.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SHOW_CHART),
                    title=ft.Text(f"Emp {em_['id_emprestimo']} Usu: {em_['usuario_id']} Liv: {em_['livro_id']}"),
                    subtitle=ft.Text(f"{em_['data_emprestimo']} → {em_['data_devolucao']}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="Detalhes", on_click=lambda _, e_=em_: emprestimo_exibir_detalhes(e)),
                            ft.PopupMenuItem(text="Editar", on_click=lambda _, e_=em_: emprestimo_exibir_editar(e)),
                        ],
                    )
                )
            )
        page.update()

    # Função para gerenciar rotas
    def gerencia_rotas(e):
        page.views.clear()

        # Tela Inicial
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Container(height=25),
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
                                ft.Text("Descubra, escolha.\ne Leia.", size=38, weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=20),
                                ft.CupertinoButton(
                                    text="Livros",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/livros")
                                ),
                                ft.CupertinoButton(
                                    text="Usuarios",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/usuarios")
                                ),
                                ft.CupertinoButton(
                                    text="Empréstimos",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/emprestimos")
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                ],
            )
        )
        if page.route == "/livros" or page.route == "/cadastrar_livros" or page.route == "/listar_livros":
            page.views.append(
                ft.View(
                    "/livros",
                    [
                        ft.AppBar(title=ft.Text("Página do Livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=10,
                            content=ft.Column(
                                [
                                    ft.Container(height=10),
                                    ft.Image(
                                        src=f"https://cdn-icons-png.flaticon.com/512/8832/8832880.png",
                                        width=168,
                                        height=168,
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                                    ft.Text("Livros", size=38, weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER),
                                    ft.Container(height=10),
                                    ft.CupertinoButton(
                                        text="Listar Livros",
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        width=320,
                                        on_click=lambda _: page.go("/listar_livros")),
                                    ft.CupertinoButton(
                                        text="Cadastrar Livros",
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        width=320,
                                        on_click=lambda _: page.go("/cadastrar_livros")),
                                ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                ],
            )
        )
        if page.route == "/cadastrar_livros":
            page.views.append(
                ft.View(
                    "/cadastrar_livros",
                    [
                        ft.AppBar(title=ft.Text("Cadastro de Livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Text("Cadastrar Livro", size=20, weight=ft.FontWeight.BOLD),
                        input_titulo,
                        input_autor,
                        input_ISBN,
                        input_resumo,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Salvar",
                                    on_click=lambda _: salvar_livros(e)
                                )
                            ]
                        )
                    ],
                )
            )
        if page.route == "/listar_livros" or page.route == "/editar_livros" or page.route == "/livros_detalhes":
            exibir_livro(e)
            page.views.append(
                ft.View(
                    "/listar_livros",
                    [
                        ft.AppBar(title=ft.Text("Lista de Livros"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        lv_livros
                    ],
                )
            )
        if page.route == "/editar_livros":
            page.views.append(
                ft.View(
                    "/editar_livros",
                    [
                        ft.AppBar(title=ft.Text("Editar livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Container(height=10),
                        ft.Row(spacing=-2,controls=[ft.Text("Editando o id Nº "),txt_id]),
                        ft.Container(height=10),
                        input_titulo,
                        input_autor,
                        input_ISBN,
                        input_resumo,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Salvar",
                                    on_click=lambda _: editar_livros(int(txt_id.value))
                                ),
                                ft.ElevatedButton(
                                    text="Exibir Lista",
                                    on_click=lambda _: page.go("/listar_livros")
                                )
                            ]
                        )
                    ],
                )
            )
        # Tela de Detalhes do usuario
        if page.route == "/livros_detalhes":
            page.views.append(
                ft.View(
                    "/livros_detalhes",
                    [
                        ft.AppBar(title=ft.Text("Detalhes do Livro"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Text("ISBN:", size=15),
                        txt_ISBN,
                        ft.Text("Resumo:", size=15),
                        txt_resumo,
                    ],
                )
            )
        if page.route == "/usuarios" or page.route == "/cadastrar_usuario" or page.route == "/listar_usuario":
            page.views.append(
                ft.View(
                    "/usuarios",
                    [
                        ft.AppBar(title=ft.Text("Página do Usuário"), bgcolor=ft.Colors.SECONDARY_CONTAINER),

                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=10,
                            content=ft.Column(
                                [
                                    ft.Image(
                                        src=f"https://cdn-icons-png.freepik.com/256/9055/9055398.png?semt=ais_hybrid",
                                        width=168,
                                        height=168,
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                                    ft.Text("Usuários", size=38, weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER),
                                    ft.Container(height=15),
                                    ft.CupertinoButton(
                                        text="Listar Usuários",
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        width=320,
                                        on_click=lambda _: page.go("/listar_usuario")),
                                    ft.CupertinoButton(
                                        text="Cadastrar Usuários",
                                        bgcolor=ft.Colors.BLACK,
                                        color=ft.Colors.WHITE,
                                        width=320,
                                        on_click=lambda _: page.go("/cadastrar_usuario")),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                ]
            )
        )
        if page.route == "/cadastrar_usuario":
            page.views.append(
                ft.View(
                    "/cadastrar_usuario",
                    [
                        ft.AppBar(title=ft.Text("Cadastro de Usuário"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Text("Cadastrar Usuário", size=20, weight=ft.FontWeight.BOLD),
                        input_nome,
                        input_email,
                        input_cpf,
                        input_endereco,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Salvar",
                                    on_click=lambda _: salvar_usuarios(e)
                                )
                            ]
                        )
                    ],
                )
            )
        if page.route == "/listar_usuario" or page.route == "/editar_usuario" or page.route == "/usuario_detalhes":
            exibir_usuarios(e)
            page.views.append(
                ft.View(
                    "/listar_usuario",
                    [
                        ft.AppBar(title=ft.Text("Lista de Usuário"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        lv_usuarios
                    ],
                )
            )
        if page.route == "/editar_usuario":
            page.views.append(
                ft.View(
                    "/editar_usuario",
                    [
                        ft.AppBar(title=ft.Text("Editar Usuário"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Container(height=10),
                        ft.Row(spacing=-2,controls=[ft.Text("Editando o id Nº "),txt_id]),
                        ft.Container(height=10),
                        input_nome,
                        input_email,
                        input_cpf,
                        input_endereco,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Salvar",
                                    on_click=lambda _: editar_usuarios(int(txt_id.value))
                                ),
                                ft.ElevatedButton(
                                    text="Exibir Lista",
                                    on_click=lambda _: page.go("/listar_usuario")
                                )
                            ]
                        )
                    ],
                )
            )
        # Tela de Detalhes do usuario
        if page.route == "/usuario_detalhes":
            page.views.append(
                ft.View(
                    "/usuario_detalhes",
                    [
                        ft.AppBar(title=ft.Text("Detalhes do Usuário"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Text("Cadastro de Pessoa Física:", size=15),
                        txt_user_cpf,
                        ft.Text("Endereço:", size=15),
                        txt_user_endereco,
                    ],
                )
            )
        if page.route == "/emprestimos":
            page.views.append(
                ft.View(
                    "/emprestimos",
                    [
                        ft.AppBar(title=ft.Text("Página de Empréstimos"), bgcolor=ft.Colors.SECONDARY_CONTAINER),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=10,
                            content=ft.Column(
                                [
                                ft.Container(height=5),
                                ft.Image(
                                    src=f"https://cdn-icons-png.flaticon.com/512/2417/2417791.png",
                                    width=168,
                                    height=168,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                ft.Text("Empréstimos", size=38, weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=20),
                                ft.CupertinoButton(
                                    text="Listar Empréstimos",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/home")),
                                ft.CupertinoButton(
                                    text="Cadastrar Empréstimos",
                                    bgcolor=ft.Colors.BLACK,
                                    color=ft.Colors.WHITE,
                                    width=320,
                                    on_click=lambda _: page.go("/home")),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                ],
            )
        )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # ---- CAMPOS E COMPONENTES LIVROS ----
    input_titulo = ft.TextField(label="Nome do Livro")
    input_autor = ft.TextField(label="Autor")
    input_ISBN = ft.TextField(label="ISBN")
    input_resumo = ft.TextField(label="Resumo", multiline=True)

    lv_livros = ft.ListView(height=300)
    txt_id = ft.Text("", visible=False)
    txt_ISBN = ft.Text("", size=15)
    txt_resumo = ft.Text("", size=15)

    # ---- CAMPOS E COMPONENTES USUÁRIOS ----
    input_nome = ft.TextField(label="Nome do Usuário")
    input_email = ft.TextField(label="Email")
    input_cpf = ft.TextField(label="Cadastro de Pessoa Física")
    input_endereco = ft.TextField(label="Endereço")

    lv_usuarios = ft.ListView(height=300)
    txt_user_id = ft.Text("", visible=False)
    txt_user_nome = ft.Text("", size=15)
    txt_user_email = ft.Text("", size=15)
    txt_user_cpf = ft.Text("", size=15)
    txt_user_endereco = ft.Text("", size=15)

    # ---- CAMPOS E COMPONENTES EMPRÉSTIMOS ----
    input_e_user = ft.TextField(label="ID do Usuário")
    input_e_livro = ft.TextField(label="ID do Livro")
    input_data_inicio = ft.TextField(label="Data Início (yyyy-mm-dd)")
    input_data_fim = ft.TextField(label="Data Fim (yyyy-mm-dd)")

    lv_emprestimos = ft.ListView(height=300)
    txt_emp_id = ft.Text("", visible=False)
    txt_emp_detalhes = ft.Text("", size=15)

    # ---- MENSAGENS GLOBAIS ----
    msg_sucesso = ft.SnackBar(content=ft.Text("Sucesso!"), bgcolor=ft.Colors.GREEN)
    msg_error = ft.SnackBar(content=ft.Text("Todos os campos são obrigatórios!"), bgcolor=ft.Colors.RED)
    msg_integrity_error = ft.SnackBar(content=ft.Text("Erro, CPF já está em uso!"), bgcolor=ft.Colors.RED)
    msg_len_error = ft.SnackBar(content=ft.Text("Erro, CPF digitado é invalido! (um CPF possui 11 dígitos)"), bgcolor=ft.Colors.RED)
    msg_idk_error = ft.SnackBar(content=ft.Text("Erro, algo inesperado ocorreu!"), bgcolor=ft.Colors.RED)

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)


# Iniciando o aplicativo Flet
ft.app(main)
