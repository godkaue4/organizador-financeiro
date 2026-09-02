import flet as ft
from models import banco_de_dados 
import flet_charts as fc
def main(page: ft.Page):
    page.title = "Organizador Financeiro"
    #page.bgcolor = "#1504D3" 
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        hint_color=ft.Colors.RED_200
    )
    banco=banco_de_dados()
    page.theme_mode=ft.ThemeMode.DARK   
    saldo_atual=banco.buscar_saldo()
    gastos = banco.buscar_gastos() 
    descricao=banco.buscar_descricao() 
    receita=banco.buscar_receita()
    def tela_principal():
        txt_saldo = ft.Text(f'Saldo atual: R${saldo_atual:.2f}', size=20, weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.START
                            )
        txt_gastos= ft.Text("Gastos:", size=20, weight=ft.FontWeight.BOLD)
        txt_receita=ft.Text(f"receita: R${receita:.2f}",size=20,weight=ft.FontWeight.BOLD)
        page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, 
        on_click=lambda e:mostrar_tela(add_dinheiro(e)),
        tooltip="Adicionar Saldo",
    )
        page.floating_action_button_location = ft.FloatingActionButtonLocation.END_DOCKED
        lista_gastos = ft.Column()
        def resetar_dados(e):
            nonlocal saldo_atual
            nonlocal receita
            nonlocal gastos
            banco.resetar_dados()
            saldo_atual=0.00
            receita=0.00
            gastos=[]
            mostrar_tela(tela_principal())
        def remover_gasto(e,id_gasto):
            nonlocal gastos
            nonlocal saldo_atual
            banco.remover_gasto(id_gasto)
            valor=[v['valor'] for v in gastos if v['id']== id_gasto]
            gastos=[g for g in gastos if g['id'] != id_gasto]
            
            saldo_atual += valor[0]
            
            mostrar_tela(tela_principal())
        for gasto in gastos:
            
            lista_gastos.controls.append(
                ft.Row([
                    ft.Text(f"- {gasto['onde']}: R${gasto['valor']:.2f} ({gasto['categoria']})"),
                    ft.IconButton(icon=ft.Icons.DELETE,on_click=lambda e:remover_gasto(e,gasto['id']))
                    
                    
                ])
                
            )
        return ft.Container(
            content=ft.Column([          
            txt_receita,
            txt_saldo,
            ft.TextButton('gerar estatisticas',style=ft.ButtonStyle(bgcolor='green',color='white'),icon=ft.Icons.BAR_CHART,on_click=lambda e: mostrar_tela(estatistica(e))),
            ft.Divider(color=ft.Colors.WHITE_24),
            txt_gastos ,
            ft.TextButton('add gastos',style=ft.ButtonStyle(bgcolor='green',color='white'),icon=ft.Icons.ADD,
                          on_click=lambda e: mostrar_tela(add_gasto(e)
                                                          )) ,
            lista_gastos,
            ft.TextButton('remover dados',style=ft.ButtonStyle(bgcolor='red',color='white'),icon=ft.Icons.DELETE,on_click=lambda e: resetar_dados(e))
            ],scroll=ft.ScrollMode.AUTO),
            expand=True,
            padding=20,
            )

    def mostrar_tela(nova_tela):

        page.clean()
        page.add(ft.SafeArea(content=nova_tela,expand=True))

        page.update()    

    mostrar_tela(tela_principal())
        
    def add_dinheiro(e): 
        
        valor_fild = ft.TextField(label="Quanto dinheiro você possui?",
                                  hint_text='R$'
                                  ,keyboard_type=ft.KeyboardType.NUMBER, label_style=ft.TextStyle(color=ft.Colors.WHITE))
        descricao_fild = ft.TextField(label="Descrição", label_style=ft.TextStyle(color=ft.Colors.WHITE))
        data_fild = ft.TextField(label="Data", label_style=ft.TextStyle(color=ft.Colors.WHITE), hint_text="dd/mm/aaaa")

        def adicionar_dinheiro(e):
            nonlocal saldo_atual
            nonlocal receita        
            valor=float(valor_fild.value.replace(',','.'))
            descricao=descricao_fild.value
            data=data_fild.value
            try:
                if valor_fild.value and descricao_fild.value:
                    
                    saldo_atual += float(valor_fild.value.replace(',','.'))
                    receita += float(valor_fild.value.replace(',','.'))
                    banco.atualizar_saldo(valor_fild.value)
                    banco.atualizar_receita(valor_fild.value)
                    banco.inserir_descricao(descricao,valor,data)
                    mostrar_tela(tela_principal())
                else:
                    raise ValueError
                
            except ValueError:
                page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um valor válido.")))
    
                page.update()
            
            
        return ft.Container(
            content=ft.Column([
            ft.Text("Adicionar Saldo", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            valor_fild,
            descricao_fild,
            data_fild,
            ft.FilledButton("Adicionar", on_click=adicionar_dinheiro),
            ft.TextButton("Cancelar", on_click=lambda e: mostrar_tela(tela_principal()))
        ]),
           expand=True,
           padding=20                 
    )
    def estatistica(e):
        # 1. Agrupar os gastos por categoria (soma total de cada uma)
        soma_por_categoria = {}
        for gasto in gastos:
            categoria = gasto['categoria']
            valor = gasto['valor']

            if categoria in soma_por_categoria:
                soma_por_categoria[categoria] += valor
            else:
                soma_por_categoria[categoria] = valor

        # 2. Caso não haja nenhum gasto ainda, evita erro e avisa o usuário
        if not soma_por_categoria:
            page.snack_bar = ft.SnackBar(ft.Text("Nenhum gasto registrado ainda."))
            page.snack_bar.open = True
            page.update()
            return tela_principal()

        # 3. Lista de cores para usar nas fatias (uma por categoria, repete se precisar)
        cores = [
            ft.Colors.RED,
            ft.Colors.BLUE,
            ft.Colors.GREEN,
            ft.Colors.ORANGE,
            ft.Colors.PURPLE,
            ft.Colors.YELLOW,
        ]

        # 4. Montar as seções do gráfico, calculando a porcentagem sobre a receita
        sections = []
        for i, (categoria, total_categoria) in enumerate(soma_por_categoria.items()):
            porcentagem = (total_categoria / receita) * 100 if receita > 0 else 0
            sections.append(
                fc.PieChartSection(
                    value=total_categoria,
                    title=f"{categoria}\n{porcentagem:.1f}%",
                    color=cores[i % len(cores)],
                    radius=100,
                    title_style=ft.TextStyle(size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                )
            )

        grafico = fc.PieChart(
            sections=sections,
            sections_space=2,
            center_space_radius=40,
            expand=True,
        )
        lista_descricao = ft.Column()
        for linha in descricao:
            lista_descricao.controls.append(ft.Row([
                ft.Text(f"Descrição: {linha['descricao']}, Valor: R${linha['valor']:.2f}, Data: {linha['data']}"),
                
            ]))
        # 5. Retornar a tela de estatísticas
        return ft.Container(content=ft.Column(
            [
                ft.Text("Estatísticas de Gastos", size=20, weight=ft.FontWeight.BOLD),
                grafico,
                lista_descricao,
                ft.TextButton("Voltar", on_click=lambda e: mostrar_tela(tela_principal())),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        padding=20  
    )
    def add_gasto(e):
        butonadd=ft.FilledButton("Adicionar", on_click=lambda e: adicionar_gasto(e),
                                 style=ft.ButtonStyle(
                                    bgcolor='green'
                                 ))          
        nome_f=ft.TextField(label="onde:")
        valor_f=ft.TextField(label="quanto dinheiro voce gastou?",
                               hint_text='R$'
                               ,keyboard_type=ft.KeyboardType.NUMBER)

        categoria_drop=ft.Dropdown(label="Categoria", options=[
                ft.dropdown.Option("Alimentação"),
                ft.dropdown.Option("Transporte"),
                ft.dropdown.Option("Moradia"),
                ft.dropdown.Option("Lazer"),
                ft.dropdown.Option("Saúde"),
                ft.dropdown.Option("outros")
                
            ],
                  
            )
        def adicionar_gasto(e):
            nonlocal saldo_atual  
            try:
                if not valor_f.value and not nome_f.value:
                    page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um inforamções  válidas.")))
                    page.update()
                    return
                valor=float(valor_f.value)
                categoria=categoria_drop.value
                if categoria is None:
                    page.show_dialog( ft.SnackBar(ft.Text("Por favor, selecione uma categoria.")))
        
                    page.update()
                    return
                if valor > saldo_atual:
                    page.show_dialog(ft.SnackBar(ft.Text('valor acima do saldo atual')))
                    
                    page.update()
                    return
                if categoria is not None and valor_f and nome_f:
                    saldo_atual -= valor
                    novo_id=banco.inserir_gastos(nome_f.value,valor,categoria)
                    gastos.append({
                        'id':novo_id,
                        'onde': nome_f.value,
                        'valor': valor,
                        'categoria': categoria
                    })
                    
                    mostrar_tela(tela_principal())

            except ValueError:
                page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um valor válido.")))
    
                page.update()
            
                
        return ft.Container(content=ft.Column([
                valor_f,
                nome_f,
                categoria_drop,
                butonadd,
                ft.TextButton("Cancelar", on_click=lambda e: mostrar_tela(tela_principal()))
         ]),
            padding=20,
            expand=True
    )

ft.app(target=main) 