import flet as ft


def main(page: ft.Page):
    page.window.width = 400
    page.window.height = 600
    page.window.maximizable=False
    
    
    page.title = "Organizador Financeiro"
    page.bgcolor = "#1504D3" 
    page.theme_mode=ft.ThemeMode.DARK   
    saldo_atual=00.00
    gastos = []   
    def tela_principal():
        txt_saldo = ft.Text(f'Saldo atual: R${saldo_atual:.2f}', size=20, weight=ft.FontWeight.BOLD
                            )
        txt_gastos= ft.Text("Gastos:", size=20, weight=ft.FontWeight.BOLD)
        page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda e:mostrar_tela(add_dinheiro(e))
    )
        page.floating_action_button.location = ft.FloatingActionButtonLocation.END_DOCKED
        lista_gastos = ft.Column()
        for gasto in gastos:
            
            lista_gastos.controls.append(
                ft.Text(f"- {gasto['nome']}: R${gasto['valor']:.2f} ({gasto['categoria']})")
            )
           # remove=ft.TextButton('remover gastos',style=ft.ButtonStyle(alignment=ft.Alignment.BOTTOM_LEFT),on_click=lambda e:remover_gastos(gasto))
        return ft.Container(
            content=ft.Column([
            txt_saldo,
            ft.TextButton('gerar estatisticas',ft.TextButton('add gastos',style=ft.ButtonStyle(bgcolor='green',color='white'),on_click=lambda e: estatistica(e))),
            ft.Divider(color=ft.Colors.WHITE_24),
            txt_gastos ,
            ft.TextButton('add gastos',style=ft.ButtonStyle(bgcolor='green',color='white'),
                          on_click=lambda e: mostrar_tela(add_gasto(e)
                                                          )) ,
            lista_gastos
            ],scroll=ft.ScrollMode.AUTO),
            expand=True,
            alignment=ft.Alignment.CENTER,
            )

    def mostrar_tela(nova_tela):

        page.clean()
        page.add(nova_tela)

        page.update()    

    mostrar_tela(tela_principal())
        
    def add_dinheiro(e): 
        
        valor_fild = ft.TextField(label="Quanto dinheiro você possui?", hint_text='R$', keyboard_type=ft.KeyboardType.NUMBER, label_style=ft.TextStyle(color=ft.Colors.WHITE))
        descricao_fild = ft.TextField(label="Descrição", label_style=ft.TextStyle(color=ft.Colors.WHITE))
         
        def adicionar_dinheiro(e):
            nonlocal saldo_atual
            try:
                if valor_fild.value and descricao_fild.value:
                    
                    saldo_atual += float(valor_fild.value.replace(',','.'))
                    mostrar_tela(tela_principal())
                else:
                    raise ValueError
                
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, insira um valor válido."))
                page.snack_bar.open = True
                page.update()
            
            
        return ft.Column([
            ft.Text("Adicionar Saldo", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            valor_fild,
            descricao_fild,
            ft.FilledButton("Adicionar", on_click=adicionar_dinheiro),
            ft.TextButton("Cancelar", on_click=lambda e: mostrar_tela(tela_principal()))
        ])
    def estatistica(e):
        pass
    def add_gasto(e):
        butonadd=ft.FilledButton("Adicionar", on_click=lambda e: adicionar_gasto(e),
                                 style=ft.ButtonStyle(
                                    bgcolor='green'
                                 ))          
        nome_f=ft.TextField(label="nome:")
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
                    page.snack_bar = ft.SnackBar(ft.Text("Por favor, insira um inforamções  válidas."))
                    page.snack_bar.open = True
                    page.update()
                    return
                valor=float(valor_f.value)
                categoria=categoria_drop.value
                if categoria is None:
                    page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecione uma categoria."))
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if categoria is not None and valor_f and nome_f:
                    saldo_atual -= valor
                    gastos.append({
                        'nome': nome_f.value,
                        'valor': valor,
                        'categoria': categoria
                    })
                    mostrar_tela(tela_principal())
                if valor > saldo_atual:
                    page.snack_bar = ft.SnackBar(ft.Text('valor acima do saldo atual'))
                    page.snack_bar.open=True
                    page.update()
                    return
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, insira um valor válido."))
                page.snack_bar.open = True
                page.update()
            
                
        return ft.Column([
                valor_f,
                nome_f,
                categoria_drop,
                butonadd,
                ft.TextButton("Cancelar", on_click=lambda e: mostrar_tela(tela_principal()))
         ])
ft.app(target=main) 