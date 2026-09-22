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
    descricoes=banco.buscar_descricao() 
    receita=banco.buscar_receita()
    metas=banco.buscar_metas()
    mensais=banco.buscar_mensal()
    indice_atual=0
    
    cursos=[{'titulo':'MÓDULO 1 — ORÇAMENTO NA PRÁTICA','indice':0,'texto':'''
    Objetivo

Aprender a organizar o dinheiro, identificar os gastos e planejar como utilizar a renda.

    O que é renda?

Renda é todo dinheiro que uma pessoa recebe. Pode vir de mesada, salário, bolsa de estudos ou pequenos serviços.

Exemplo:
João recebe R$ 400 por mês:

Mesada: R$ 250
Pequenos serviços: R$ 150

Total: R$ 400

Saber quanto dinheiro entra é o primeiro passo para organizar as finanças.

 Gasto fixo e gasto variável

Gasto fixo: Despesa que costuma se repetir e pode manter um valor semelhante.

Exemplos: plano de celular, mensalidade de curso e parcelas.

Gasto variável: Despesa cujo valor ou frequência pode mudar.

Exemplos: lanches, passeios, roupas e compras em jogos.

Exemplo prático:
Pedro recebe R$ 300:

Celular: R$ 30
Lanches: R$ 80
Passeio: R$ 50
Acessório: R$ 40

Total de gastos: R$ 200

Saldo restante: R$ 100

    Regra 50/30/20

A regra 50/30/20 é uma forma de dividir a renda:

50% — Necessidades: alimentação, transporte e moradia.
30% — Desejos: lazer, roupas e passeios.
20% — Futuro financeiro: reserva e metas.

Essa regra é apenas uma referência e pode ser adaptada à realidade de cada pessoa.

Exemplo com R$ 500:

Necessidades: R$ 250
Desejos: R$ 150
Reserva e metas: R$ 100
    
    Pratique no aplicativo

Registre sua renda e seus gastos no Organizador Financeiro. Observe quanto dinheiro sobra e pense em como você poderia utilizá-lo.

💡 Lembre-se: Organizar o dinheiro não significa deixar de aproveitar a vida, mas aprender a fazer escolhas conscientes.'''},{'titulo':'MÓDULO 2 — GASTO, DÍVIDA E INVESTIMENTO','indice':1,'texto':""""
    Objetivo
Entender a diferença entre gastos, dívidas e investimentos e conhecer os riscos do uso inadequado do crédito.

    O que é um gasto?

Gasto é o dinheiro utilizado para comprar um produto ou serviço.

Exemplos:

Comprar um lanche.
Pagar transporte.
Comprar material escolar.
Adquirir um jogo.

Um gasto não é necessariamente ruim. É importante verificar se ele cabe no orçamento.

    O que é uma dívida?

Dívida é uma obrigação de pagamento que ficou pendente, geralmente por causa de uma compra parcelada, empréstimo ou uso de crédito.

Exemplo:
Lucas compra um celular de R$ 1.200 em 12 parcelas de R$ 100.

Ele assume o compromisso de pagar R$ 100 por mês, considerando que não existam encargos adicionais.

Antes de parcelar, é importante verificar o custo total e se as parcelas cabem no orçamento.

    Dívidas com diferentes finalidades

Algumas dívidas podem contribuir para objetivos pessoais, como um financiamento de estudos. Outras podem causar problemas quando envolvem juros elevados ou falta de planejamento.

Exemplo:

Crédito para um curso: pode ajudar na formação, mas precisa ser pago.
Cartão de crédito rotativo: pode aumentar o valor da dívida devido aos encargos.

Nenhuma dívida deve ser considerada automaticamente boa ou ruim. É necessário analisar as condições e a capacidade de pagamento.

    Cuidado com o cartão de crédito

Quando uma pessoa não paga integralmente a fatura do cartão, podem ser cobrados juros e outros encargos.

Isso pode fazer uma dívida crescer e comprometer a renda dos meses seguintes.

Dicas:

Confira o valor da fatura.
Evite compras que não cabem no orçamento.
Conheça os juros e as condições do crédito.
Procure orientação de um responsável quando necessário.
📱 Pratique no aplicativo

Imagine que você quer comprar um celular de R$ 1.000.

Você pode comparar diferentes formas de pagamento e analisar como cada escolha afetaria seu orçamento.

💡 Lembre-se: Antes de assumir uma dívida, entenda quanto você terá que pagar e se conseguirá cumprir o compromisso."""}]
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
        def fechar_drawer():
            if drawer in page._dialogs.controls:
                page._dialogs.controls.remove(drawer)
                page._dialogs.update()
        async def handle_show_drawer():
            if drawer in page._dialogs.controls:
                page._dialogs.controls.remove(drawer)
                page._dialogs.update()
            else:
                page.show_dialog(drawer)
        def handle_dismissal(e: ft.Event[ft.NavigationDrawer]):
                print('Drawer dismissed')
                fechar_drawer()
        async def handle_change(e:ft.Event[ft.NavigationDrawer]):
                print(f"Selected Index changed: {e.control.selected_index}")
                fechar_drawer()
                if e.control.selected_index==0:
                    mostrar_tela(tela_principal(),True)
                elif e.control.selected_index == 1:
                   mostrar_tela(curso())
                page.update()
        drawer=ft.NavigationDrawer(
                on_dismiss=handle_dismissal,
                on_change=handle_change,
                tile_padding=ft.Padding(top=10),
                controls=[ft.Container(height=12),
                          ft.NavigationDrawerDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    label="pagina incial",
                               ),
                            ft.NavigationDrawerDestination(
                                    icon=ft.Icons.ATTACH_MONEY_OUTLINED,
                                    label="mini curso de educação fincanceira",
                                                         )
                          
                          ]
            )
        app_bar=ft.AppBar(leading=ft.IconButton(ft.Icons.MENU,on_click=handle_show_drawer)
                          )
        page.appbar=app_bar
        def resetar_dados(e):
            nonlocal saldo_atual
            nonlocal receita
            nonlocal gastos
            nonlocal metas
            banco.resetar_dados()
            saldo_atual=0.00
            receita=0.00
            gastos=[]
            metas=[]
            mostrar_tela(tela_principal(),True)
        def remover_gasto(e,id_gasto):
            nonlocal gastos
            nonlocal saldo_atual
            banco.remover_gasto(id_gasto)
            valor=[v['valor'] for v in gastos if v['id']== id_gasto]
            gastos=[g for g in gastos if g['id'] != id_gasto]
            
            saldo_atual += valor[0]
            
            mostrar_tela(tela_principal(),True)
        for gasto in gastos:
            
            lista_gastos.controls.append(
                ft.Column([                
                        ft.Row([
                            ft.Divider(height=1, color=ft.Colors.WHITE_24),
                            ft.Text(f"- {gasto['onde']}: R${gasto['valor']:.2f} ({gasto['categoria']})",
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                size=16,
                                expand=True),
                    
                            ft.IconButton(icon=ft.Icons.DELETE,on_click=lambda e:remover_gasto(e,gasto['id']))
                    
                    
                ],expand=True)])

          
            )
            
        return ft.Container(
            content=ft.Column([      
            txt_receita,
            txt_saldo,
            ft.TextButton('gerar estatisticas',style=ft.ButtonStyle(bgcolor='green',color='white'),icon=ft.Icons.BAR_CHART,on_click=lambda e: mostrar_tela(estatistica(e))),
            ft.TextButton('adicionar meta',style=ft.ButtonStyle(bgcolor='blue',color='white'),icon=ft.Icons.ADD,on_click=lambda e: mostrar_tela(add_meta(e))),
            ft.TextButton('ver metas',style=ft.ButtonStyle(bgcolor='blue',color='black'),on_click=lambda e: mostrar_tela(ver_metas(e))),
            ft.Divider(color=ft.Colors.WHITE_24),
            txt_gastos ,
            ft.TextButton('add gastos',style=ft.ButtonStyle(bgcolor='green',color='white'),icon=ft.Icons.ADD,
                          on_click=lambda e: mostrar_tela(add_gasto(e)
                                                          )) ,
            
            lista_gastos,
            ft.Divider(color=ft.Colors.WHITE_24),

            ft.TextButton('remover dados',style=ft.ButtonStyle(bgcolor='red',color='white'),icon=ft.Icons.DELETE,on_click=lambda e: resetar_dados(e))
            ],scroll=ft.ScrollMode.AUTO),
            expand=True,
            padding=20,
            )

    def mostrar_tela(nova_tela,e_principal=False):
        if e_principal:
            pass
        else:
            page.floating_action_button = None
        page.clean()
        page.add(ft.SafeArea(content=nova_tela,expand=True))

        page.update()    

    mostrar_tela(tela_principal(),True)
        
    def add_dinheiro(e): 
        
        valor_fild = ft.TextField(label="Quanto dinheiro você possui?",
                                  hint_text='R$'
                                  ,keyboard_type=ft.KeyboardType.NUMBER, label_style=ft.TextStyle(color=ft.Colors.WHITE),
                                    input_filter=ft.InputFilter(
                                                    allow=True,
                                                    regex_string=r"^\d*\.?\d*$",
                                                    replacement_string=""
                                                ),
                                    on_change=lambda e: (
                                        setattr(e.control, 'value', e.control.value.replace(",", ".")),
                                        e.page.update()))
        descricao_fild = ft.TextField(label="Descrição", label_style=ft.TextStyle(color=ft.Colors.WHITE))
        data_fild = ft.TextField(label="Data", label_style=ft.TextStyle(color=ft.Colors.WHITE), hint_text="dd/mm/aaaa")
        
        def adicionar_dinheiro(e):
            if not valor_fild:
                    page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um valor(R$) válido.")))
                    page.update()
                    return
            elif not descricao_fild:
                    page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira uma descrição válida.")))
                    page.update()
                    return
            elif not data_fild:
                    page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira uma data válida.")))
                    page.update()
                    return
            elif not isinstance(valor_fild.value, (int, float)) <= 0:
                    page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um valor(R$) válido.")))
                    page.update()
                    return
                
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
                    descricoes.append({'id':banco.cursor.lastrowid,
                                     'descricao':descricao,
                                     'valor':valor,
                                     'data':data})
                    mostrar_tela(tela_principal(),True)

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
            ft.TextButton("Cancelar", on_click=lambda e: mostrar_tela(tela_principal(),True))
        ]),
           expand=True,
           padding=20                 
    )
    def curso():
        lista_modulo=ft.Column()

        nonlocal indice_atual
        list_curso=cursos
        for modulo in list_curso:
            if indice_atual == modulo['indice']:
                indice_atual=modulo['indice']
                lista_modulo.controls.append(
                    ft.Container(content=ft.Column([
                        ft.Text(f'{modulo['titulo']} \n {modulo['texto']}')
                        ]))
                    )
        def proximo(e):
            nonlocal indice_atual
            indice_atual +=1
            lista_modulo.controls.clear()
            return mostrar_tela(curso())
        def anterior(e):
            nonlocal indice_atual
            indice_atual -=1
            lista_modulo.controls.clear()
            return mostrar_tela(curso())
        return ft.Container(content=ft.Column([lista_modulo,
            ft.Row([
                ft.TextButton('próximo',on_click=lambda e:proximo(e) ),
                ft.TextButton('anterior',on_click=lambda e: anterior(e))
            ])
        ],scroll=ft.ScrollMode.AUTO),expand=True)
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
            page.show_dialog(ft.SnackBar(ft.Text("Nenhum gasto registrado ainda.")))
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
                    radius=150,
                    title_style=ft.TextStyle(size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                )
            )

        grafico = fc.PieChart(
            sections=sections,
            sections_space=2,
            center_space_radius=40,
            
            expand=True,
        )
        lista_descricao = ft.Column()
        for linha in descricoes:
            lista_descricao.controls.append(ft.Row([
                ft.Text(f"Descrição: {linha['descricao']}, Valor: R${linha['valor']:.2f}, Data: {linha['data']}"),
                
            ]))
        # 5. Retornar a tela de estatísticas
        return ft.Container(content=ft.Column(
            [
                ft.Text("Estatísticas de Gastos", size=20, weight=ft.FontWeight.BOLD),
                grafico,
                lista_descricao,
                ft.TextButton("Voltar", on_click=lambda e: mostrar_tela(tela_principal(),True)),
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
                               ,keyboard_type=ft.KeyboardType.NUMBER,
                                input_filter=ft.InputFilter(
                                            allow=True,
                                            regex_string=r"^\d*(,\d{0,2})?$",
                                            replacement_string=""
                                                ),
                                    on_change=lambda e: (
                                        setattr(e.control, 'value', e.control.value.replace(",", ".")),
                                        e.page.update()))

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
            if not valor_f.value or not nome_f.value:
                page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um inforamções  válidas.")))
                page.update()
                return
            elif not categoria_drop.value:
                page.show_dialog( ft.SnackBar(ft.Text("Por favor, selecione uma categoria.")))
                page.update()
                return
            elif isinstance(valor_f.value,(int,float)) and float(valor_f.value.replace(',','.')) <= 0:
                page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um valor válido.")))
                page.update()
                return
            elif float(valor_f.value.replace(',','.')) > saldo_atual:
                page.show_dialog( ft.SnackBar(ft.Text("Saldo insuficiente para este gasto.")))
                page.update()
                return
            try:
                valor=float(valor_f.value)
                categoria=categoria_drop.value
                if categoria is not None and valor_f and nome_f:
                    saldo_atual -= valor
                    novo_id=banco.inserir_gastos(nome_f.value,valor,categoria)
                    gastos.append({
                        'id':novo_id,
                        'onde': nome_f.value,
                        'valor': valor,
                        'categoria': categoria
                    })
                    
                    mostrar_tela(tela_principal(),True)

            except ValueError:
                page.show_dialog( ft.SnackBar(ft.Text("Por favor, insira um valor válido.")))
    
                page.update()
            
                
        return ft.Container(content=ft.Column([
                valor_f,
                nome_f,
                categoria_drop,
                butonadd,
                ft.TextButton("Cancelar", on_click=lambda e: mostrar_tela(tela_principal(),True))
         ]),
            padding=20,
            expand=True
    )
    def add_meta(e):
        obj_f=ft.TextField(label='objetivo da meta:',animate_cursor_opacity=True)
        valor_f=ft.TextField(label='quantia que deseja arrecadar?',hint_text='R$',keyboard_type=ft.KeyboardType.NUMBER,
                             input_filter=ft.InputFilter(
                                            allow=True,
                                            regex_string=r"^\d*(,\d{0,2})?$",
                                            replacement_string=""
                                                ),
                                    on_change=lambda e: (
                                        setattr(e.control, 'value', e.control.value.replace(",", ".")),
                                        e.page.update()))
        valorm_f= ft.TextField(label='quantos deseja guardar por mês?',hint_text='R$',keyboard_type=ft.KeyboardType.NUMBER)
        def adicionar_meta(e):
            global valor_mensal
            objetivo=obj_f.value
            valor=float(valor_f.value)
            valor_mensal=float(valorm_f.value)
            tempo=valor/valor_mensal
            banco.inserir_metas(objetivo,valor,tempo,tempo,valor_mensal,valor)
            metas.append({'id':banco.cursor.lastrowid,
                          'meta':objetivo,
                          'valor':valor,
                          'tempo_inicial':tempo,
                          'tempo':tempo,
                          'valor_mensal':valor_mensal,
                          'valor_inicial':valor})
            return mostrar_tela(tela_principal(),True)       
        return ft.Container(content=ft.Column([
                obj_f,
                valor_f,
                valorm_f,
                ft.FilledButton("adicionar", on_click=lambda e: adicionar_meta(e)),
                ft.TextButton("cancelar", on_click= lambda e: mostrar_tela(tela_principal(),True))
            ]))
    #função que serve para ver as metas cadastradas e o progresso de cada uma delas, mostrando o tempo restante para atingir a meta e o valor que falta arrecadar.
    def guardar_valor(e,id):
        nonlocal metas
        meta_atual=[m for m in metas if m['id']==id]
        valor_f=ft.TextField(label='quanto deseja guardar?',hint_text='R$',keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
                                            allow=True,
                                            regex_string=r"^\d*(,\d{0,2})?$",
                                            replacement_string=""
                                                ),
                                    on_change=lambda e: (
                                        setattr(e.control, 'value', e.control.value.replace(",", ".")),
                                        e.page.update()))
        mes_f=ft.TextField(label='de qual mês é o valor que deseja guardar?',hint_text='ex: janeiro',keyboard_type=ft.KeyboardType.TEXT)
        def guardar(e):

            nonlocal metas
            nonlocal saldo_atual
            nonlocal mensais
            try:
                valor=float(valor_f.value)
                if valor > saldo_atual:
                    page.show_dialog(ft.SnackBar(ft.Text("Saldo insuficiente para guardar esse valor.")))
                    page.update()
                    return
                if valor == meta_atual[0]['valor_mensal']:
                    tempo_restante=meta_atual[0]['tempo']-1
                else:
                    tempo_restante=meta_atual[0]['tempo']-(valor/meta_atual[0]['valor_mensal'])
                
                banco.inserir_mensal(valor,tempo_restante,mes_f.value)
                mensais.append({'id':banco.cursor.lastrowid,
                                'valor':valor,
                                'tempo_restante':tempo_restante,
                                'mes':mes_f.value})
                saldo_atual -= valor
                banco.atualizar_saldo(-valor)
                banco.atualizar_meta(id,meta_atual[0]['valor']-valor,tempo_restante)
                banco.inserir_gastos(f'poupança para {meta_atual[0]['meta']}',valor,'poupança')
                gastos.append({
                    'id':banco.cursor.lastrowid,
                    'onde': f'poupança para {meta_atual[0]["meta"]}',
                    'valor': valor,
                    'categoria': 'poupança'
                })
                meta_atual[0]['valor'] -= valor
                meta_atual[0]['tempo'] = tempo_restante
                #metas[metas.index(meta_atual[0])]['tempo'] = tempo_restante

                if meta_atual[0]['valor'] <= 0:
                    meta_atual[0]['valor'] = 0
                    meta_atual[0]['tempo'] = 0
                    mensais[meta_atual[0]['id']]['tempo_restante'] = 0
                    banco.atualizar_meta(id,0,0)
                    banco.atualizar_mensal(id, 0)
                    page.show_dialog(ft.AlertDialog(title=ft.Text("Parabéns! Você atingiu sua meta!")))
                else:
                    for m in metas:
                        if m['id'] == id:
                            m['valor'] = meta_atual[0]['valor']
                            break
                mostrar_tela(ver_metas(e))
            except ValueError:
                page.show_dialog(ft.SnackBar(ft.Text("Por favor, insira um valor válido.")))
                page.update()
                
        return ft.Container(content=ft.Column([
            ft.Text(f"guaradar valor para a meta{meta_atual[0]['meta']} "),
            valor_f,
            mes_f,
            ft.FilledButton("guardar", on_click=lambda e: guardar(e) ),
            ft.TextButton("cancelar", on_click= lambda e: mostrar_tela(ver_metas(e))),
        ]))
    # função que serve para ver as metas ja existentes e progresso
    def ver_metas(e):
        nonlocal metas
        lista_metas=ft.Column()
        for meta in metas:
            valor_maximo=meta['valor_inicial']
            progresso=0
            barra=ft.ProgressBar(width=300, height=20, bgcolor=ft.Colors.WHITE_24, color=ft.Colors.GREEN)
            if valor_maximo > 0:
                progresso = ((meta['valor_inicial'] - meta['valor']) / meta['valor_inicial'])
                barra.value = progresso
            else:
                barra.value = 100
            if progresso >= 100:
                barra.color = ft.Colors.GREEN
            elif progresso >= 50:
                barra.color = ft.Colors.YELLOW
            else:
                barra.color = ft.Colors.RED
            if meta is None:
                return ft.Container(content=ft.Column([
                    ft.Text('sem metas até o momento'),
                    ft.TextButton('add meta',icon=ft.icons.ADD,on_click=lambda e: mostrar_tela(add_meta(e))),
                    ft.TextButton("Voltar", on_click=lambda e: mostrar_tela(tela_principal(),True))    
                ]))
            controle_de_meta=[]
            controle_de_meta.append(ft.Text(f" Meta: {meta['meta']}\n Valor: R${meta['valor']:.2f} \n Tempo estimado : {meta['tempo_inicial']:.0f} meses\n Tempo restante: {meta['tempo']:.0f} meses",size=16))
            if meta['valor'] > 0:
                controle_de_meta.append(ft.TextButton("guardar valor", style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),on_click=lambda e,id_meta=meta['id']: mostrar_tela(guardar_valor(e,id_meta))))
            controle_de_meta.append(ft.Divider(height=1, color=ft.Colors.WHITE_24))
            lista_metas.controls.append(
                ft.Column([
                    barra,
                    ft.Text(f"Progresso: {progresso*100:.2f}%", size=16, color=ft.Colors.WHITE),
                    ft.Row(controle_de_meta
                ),
                    ft.Divider(height=1, color=ft.Colors.WHITE_24)
                ])

                
            )
        return ft.Container(content=ft.Column([
            ft.Text("Metas cadastradas:", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=1, color=ft.Colors.WHITE_24),
            lista_metas,
            ft.TextButton("Voltar", on_click=lambda e: mostrar_tela(tela_principal(),True)),
        ]))
ft.app(target=main) 