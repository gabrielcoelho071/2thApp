import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors

class User():
    def __init__(self, nome, salario, emprego):
        self.nome = nome
        self.salario = salario
        self.emprego = emprego


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Listas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }

    # Funções
    lista = []

    def salvar_informacoes(e):
        if input_nome.value == "" or input_profissao.value == "" or input_salario.value == "":
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            obj_user = User(
                nome=input_nome.value,
                salario=input_salario.value,
                emprego=input_profissao.value)
            lista.append(obj_user)
            input_nome.value = ""
            input_profissao.value = ""
            input_salario.value = ""
            page.overlay.append(msg_sucesso)
            msg_sucesso.open = True
            page.update()

    def exibir_lista(e):
        lv_profissao.controls.clear()
        for user in lista:
            lv_profissao.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(f"Nome - {user.nome}"),
                    subtitle=ft.Text(f"Profissão - {user.emprego}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                          ft.PopupMenuItem(text="detalhes", on_click=lambda _, u=user: exibir_detalhes(u))
                        ],
                    )
                )
            )
        page.update()

    def exibir_detalhes(user):
        txt_profissao.value = user.emprego
        txt_salario.value = user.salario
        page.go("/terceira")


    def gerencia_rotas(e):
        page.views.clear()
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
        if page.route == "/terceira":
            exibir_lista(e)
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


    # Componentes
    msg_sucesso = ft.SnackBar(
        content=ft.Text("Valor Salvo com Sucesso"),
        bgcolor=Colors.GREEN
    )
    msg_error = ft.SnackBar(
        content=ft.Text("O valor não pode estar vazio"),
        bgcolor=Colors.RED
    )
    input_profissao = ft.TextField(label="Qual sua profissão?")
    input_salario = ft.TextField(label="Qual o seu salario?")
    input_nome = ft.TextField(label="Qual o seu nome?")

    lv_profissao = ft.ListView(
        height=500
    )

    txt_profissao = ft.Text("",size=15,
        font_family="RobotoSlab",
        weight=ft.FontWeight.W_400,)
    txt_salario = ft.Text("",size=15,
        font_family="RobotoSlab",
        weight=ft.FontWeight.W_400,)

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar

    page.go(page.route)

# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)