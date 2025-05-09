import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors
from models_profissao import *
from sqlalchemy.orm import sessionmaker


# Função para criar uma nova sessão
def create_session():
    Session = sessionmaker(bind=engine)
    return Session()


# Função principal do Flet
def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Listas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }

    # Funções de interação
    def salvar_informacoes(e):
        if input_nome.value == "" or input_profissao.value == "" or input_salario.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            # Criação de uma nova sessão
            session = create_session()

            try:
                # Criando e salvando no banco de dados
                obj_user = User(
                    nome=input_nome.value,
                    salario=input_salario.value,
                    emprego=input_profissao.value
                )

                session.add(obj_user)  # Adiciona o objeto à sessão
                session.commit()  # Salva no banco de dados

                # Limpando os campos após salvar
                input_nome.value = ""
                input_profissao.value = ""
                input_salario.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()

            except Exception as e:
                print(f"Erro ao salvar as informações: {e}")
                session.rollback()
            finally:
                session.close()  # Fechar a sessão

    def exibir_lista(e):
        lv_profissao.controls.clear()

        # Criando uma nova sessão
        session = create_session()

        try:
            # Carregando os usuários do banco de dados
            usuarios = session.query(User).all()
            for user in usuarios:
                lv_profissao.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON),
                        title=ft.Text(f"Nome - {user.nome}"),
                        subtitle=ft.Text(f"Profissão - {user.emprego}"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="detalhes", on_click=lambda _, u=user: exibir_detalhes(u)),
                                ft.PopupMenuItem(text="excluir", on_click=lambda _, u=user: excluir_usuario(u, e))
                            ],
                        )
                    )
                )
            page.update()
        except Exception as e:
            print(f"Erro ao exibir a lista de usuários: {e}")
        finally:
            session.close()  # Fechar a sessão

    def exibir_detalhes(user):
        # Exibindo os detalhes do usuário
        txt_profissao.value = user.emprego
        txt_salario.value = user.salario
        page.go("/terceira")

    def excluir_usuario(usuario, e):
        # Criando uma nova sessão
        session = create_session()

        try:
            session.delete(usuario)  # Exclui o usuário do banco de dados
            session.commit()  # Confirma a exclusão no banco de dados
            exibir_lista(e)  # Atualiza a lista na interface após a exclusão
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            session.rollback()
        finally:
            session.close()  # Fechar a sessão

    def gerencia_rotas(e):
        page.views.clear()

        # Tela inicial com campos para inserir os dados
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PRIMARY_CONTAINER),
                    input_nome,
                    input_profissao,
                    input_salario,
                    ft.Button(
                        text="Salvar",
                        on_click=lambda _: salvar_informacoes(e)
                    ),
                    ft.Button(
                        text="Exibir Lista",
                        on_click=lambda _: page.go("/segunda"),
                    )
                ],
            )
        )

        # Tela com a lista de usuários
        if page.route == "/segunda" or page.route == "/terceira":
            exibir_lista(e)
            page.views.append(
                View(
                    "/segunda",
                    [
                        AppBar(title=Text("Segunda tela"), bgcolor=Colors.SECONDARY_CONTAINER),
                        lv_profissao
                    ],
                )
            )

        # Tela de detalhes do usuário
        if page.route == "/terceira":
            page.views.append(
                View(
                    "/terceira",
                    [
                        AppBar(title=Text("Terceira tela"), bgcolor=Colors.SECONDARY_CONTAINER),
                        ft.Text("Profissão:"),
                        txt_profissao,
                        ft.Text("Salário:"),
                        txt_salario,
                    ],
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Componentes de interface
    msg_sucesso = ft.SnackBar(
        content=ft.Text("Valor Salvo com Sucesso"),
        bgcolor=Colors.GREEN
    )
    msg_error = ft.SnackBar(
        content=ft.Text("O valor não pode estar vazio"),
        bgcolor=Colors.RED
    )
    input_profissao = ft.TextField(label="Digite sua Profissão")
    input_salario = ft.TextField(label="Digite seu salário")
    input_nome = ft.TextField(label="Digite seu nome")

    lv_profissao = ft.ListView(
        height=500
    )

    txt_profissao = ft.Text("", size=15, font_family="RobotoSlab", weight=ft.FontWeight.W_400)
    txt_salario = ft.Text("", size=15, font_family="RobotoSlab", weight=ft.FontWeight.W_400)

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar

    # Começar pela tela inicial
    page.go(page.route)


# Comando que executa o aplicativo
ft.app(main)
