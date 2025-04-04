from tkinter.tix import Select

import flet as ft
from flet.core.app_bar import AppBar
from flet.core.colors import Colors
from flet.core.dropdown import Option
from flet.core.elevated_button import ElevatedButton
from flet.core.textfield import TextField


def main(page: ft.Page):
    page.title = "Aposentadoria"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    AppBar(title=ft.Text("INSS"), bgcolor=Colors.PRIMARY_CONTAINER),
                    ElevatedButton(text="Simular Aposentadoria", on_click=lambda _: page.go("/simulacao")),
                    ElevatedButton(text="Ver Regras", on_click=lambda _: page.go("/regras")),
                ],
            )
        )
        if page.route == "/regras":
            page.views.append(
                ft.View(
                    "/regras",
                    [
                        AppBar(title=ft.Text("Regras"), bgcolor=Colors.SECONDARY_CONTAINER),
                            ft.Text("Regras Básicas de Aposentadoria:\n\n"
                                    ".   Aposentadoria por Idade:\n\n"
                                    "     . Homens: 65 anos de idade e pelo menos 15 anos de contribuição.\n"
                                    "     . Mulheres: 62 anos de idade e pelo menos 15 anos de contribuição\n\n."
                                    "   Aposentadoria por Tempo de Contribuição:\n\n"
                                    "     . Homens: 35 anos de contribuição.\n"
                                    "     . Mulheres: 30 anos de contribuição.\n\n"
                                    "Valor Estimado do Benefício:\n\n"
                                    "       O valor da aposentadoria será uma média de 60% da média salarial informada,"
                                    "acrescido de 2% por ano que exceder o tempo mínimo de contribuição."
                                )
                    ],
                )
            )
        if page.route == "/simulacao":
            page.views.append(
                ft.View(
                    "/simulacao",
                    [
                        AppBar(title=ft.Text("Simulação Aposentadoria"), bgcolor=Colors.SECONDARY_CONTAINER),
                        input_idade,
                        input_genero,
                        input_tempo,
                        input_salario,
                        input_categoria,
                        ElevatedButton(text="submit", on_click=lambda _: page.go("/resultados")),
                        ElevatedButton(text="Ver Regras", on_click=lambda _: page.go("/regras")),

                    ],
                )
            )
        if page.route == "/resultados":
            page.views.append(
                ft.View(
                    "/resultados",
                    [
                        AppBar(title=ft.Text("Resultado"), bgcolor=Colors.SECONDARY_CONTAINER),
                        ft.Text(f"O valor da aposentadoria é {resultado}"),
                    ],
                )
            )

        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def aposentadoria(e):
        try:
            if input_genero.value == "masculino":
                if input_categoria.value == "":
                if int(input_idade.value) >= 65 and int(input_tempo.value) >= 15:
                if int(input_tempo.value) >= 35:
            else:

        except ValueError:
            txt_resultado.value = "Erro, Valor com formato inválido."
        page.update()


    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    txt_resultado = ft.Text(value="")
    input_idade = TextField(label="Idade atual",hint_text="Idade")
    input_genero = ft.Dropdown(label="Insira o Gênero", width=page.window.width,
                               fill_color=Colors.RED,
                               options=[Option(key="Masc", text="Masculino"),
                                        Option(key="Fem", text="Feminino")]
                               )
    input_tempo = TextField(label="Insira o tempo de contribuição", hint_text="Tempo")
    input_salario = TextField(label="Insira a sua média de salário", hint_text="Salário")
    input_categoria = TextField(label="Insira a categoria", hint_text="categoria")

    page.go(page.route)

ft.app(main)