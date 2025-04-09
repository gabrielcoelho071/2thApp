import flet as ft
from flet.core.app_bar import AppBar
from flet.core.colors import Colors
from flet.core.dropdown import Option
from flet.core.elevated_button import ElevatedButton
from flet.core.textfield import TextField

def main(page: ft.Page):
    page.title = "Aposentadoria"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 375
    page.window_height = 667

    resultado = ft.Text("", size=18, weight="bold", text_align="center")

    def alternar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    def calcular_aposentadoria(e):
        try:
            idade = int(input_idade.value)
            tempo = int(input_tempo.value)
            salario = float(input_salario.value)
            genero = input_genero.value
            categoria = input_categoria.value

            if genero == "Masc":
                if categoria == "idade" and idade >= 65 and tempo >= 15:
                    extra = max(0, tempo - 15) * 0.02
                    valor = salario * (0.6 + extra)
                    resultado.value = f"R$ {valor:.2f}"
                elif categoria == "tempo" and tempo >= 35:
                    extra = max(0, tempo - 15) * 0.02
                    valor = salario * (0.6 + extra)
                    resultado.value = f"R$ {valor:.2f}"
                else:
                    resultado.value = "Você ainda não atende aos critérios de aposentadoria."
            elif genero == "Fem":
                if categoria == "idade" and idade >= 62 and tempo >= 15:
                    extra = max(0, tempo - 15) * 0.02
                    valor = salario * (0.6 + extra)
                    resultado.value = f"R$ {valor:.2f}"
                elif categoria == "tempo" and tempo >= 30:
                    extra = max(0, tempo - 15) * 0.02
                    valor = salario * (0.6 + extra)
                    resultado.value = f"R$ {valor:.2f}"
                else:
                    resultado.value = "Você ainda não atende aos critérios de aposentadoria."
            else:
                resultado.value = "Gênero inválido."
        except ValueError:
            resultado.value = "Erro: Preencha todos os campos corretamente."

        page.go("/resultados")

    def voltar_para_home(e):
        page.go("/")

    def gerencia_rotas(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        AppBar(title=ft.Text("INSS"), bgcolor=Colors.PRIMARY_CONTAINER),
                        ft.Container(
                            alignment=ft.alignment.center,
                            expand=True,
                            content=ft.Column(
                                [
                                    ft.Image(src="INSS.png", width=120, height=120),
                                    ft.Text("Simulador de Aposentadoria", size=22, weight="bold", text_align="center"),
                                    ElevatedButton("Simular Aposentadoria", on_click=lambda _: page.go("/simulacao")),
                                    ElevatedButton("Ver Regras", on_click=lambda _: page.go("/regras")),
                                    ElevatedButton("Modo Claro/Escuro", icon=ft.icons.DARK_MODE, on_click=alternar_tema),
                                ],
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        )
                    ]
                )
            )

        elif page.route == "/regras":
            page.views.append(
                ft.View(
                    "/regras",
                    [
                        AppBar(title=ft.Text("Regras"), bgcolor=Colors.SECONDARY_CONTAINER),
                        ft.Container(
                            alignment=ft.alignment.center,
                            expand=True,
                            padding=20,
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Regras Básicas de Aposentadoria:\n\n"
                                        "• Por Idade:\n"
                                        "  - Homens: 65 anos + 15 anos contribuição\n"
                                        "  - Mulheres: 62 anos + 15 anos contribuição\n\n"
                                        "• Por Tempo:\n"
                                        "  - Homens: 35 anos\n"
                                        "  - Mulheres: 30 anos\n\n"
                                        "• Valor estimado:\n"
                                        "  60% da média + 2% por ano extra de contribuição.",
                                        size=14
                                    ),
                                    ElevatedButton("Voltar", on_click=voltar_para_home)
                                ],
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                    ]
                )
            )

        elif page.route == "/simulacao":
            page.views.append(
                ft.View(
                    "/simulacao",
                    [
                        AppBar(title=ft.Text("Simulação"), bgcolor=Colors.SECONDARY_CONTAINER),
                        ft.Container(
                            alignment=ft.alignment.center,
                            expand=True,
                            padding=20,
                            content=ft.Column(
                                [
                                    input_idade,
                                    input_genero,
                                    input_tempo,
                                    input_salario,
                                    input_categoria,
                                    ElevatedButton("Calcular", on_click=calcular_aposentadoria),
                                    ElevatedButton("Voltar", on_click=voltar_para_home),
                                ],
                                spacing=15,
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        )
                    ]
                )
            )

        elif page.route == "/resultados":
            page.views.append(
                ft.View(
                    "/resultados",
                    [
                        AppBar(title=ft.Text("Resultado"), bgcolor=Colors.SECONDARY_CONTAINER),
                        ft.Container(
                            alignment=ft.alignment.center,
                            expand=True,
                            padding=20,
                            content=ft.Column(
                                [
                                    resultado,
                                    ElevatedButton("Voltar ao Início", on_click=voltar_para_home)
                                ],
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        )
                    ]
                )
            )

        page.update()

    page.on_route_change = gerencia_rotas

    # Inputs com estilo
    input_idade = ft.Slider(min=0, max=100, divisions=100, label="Idade: {value}")
    input_genero = ft.Dropdown(
        label="Gênero",
        options=[Option(key="Masc", text="Masculino"), Option(key="Fem", text="Feminino")],
        width=300
    )
    input_tempo = TextField(label="Tempo de contribuição (anos)", hint_text="Ex: 20")
    input_salario = TextField(label="Média Salarial (R$)", hint_text="Ex: 2500.00")
    input_categoria = ft.Dropdown(
        label="Categoria",
        options=[
            Option(key="idade", text="Idade"),
            Option(key="tempo", text="Tempo de Contribuição")
        ],
        width=300
    )

    page.go(page.route)

ft.app(main)
