import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
from datetime import datetime

# BANCO LEAO DO NORTE
# Interface grafica integrada ao funcionamento do banco.py original.
# Aplicativo de estudo: os dados ficam somente na memoria enquanto o programa estiver aberto.

NAVY = "#071B2E"
NAVY_DARK = "#041322"
PANEL = "#0D2B45"
PANEL_LIGHT = "#123A59"
GOLD = "#F6BD3B"
GOLD_DARK = "#D99B17"
WHITE = "#F5F7FA"
MUTED = "#A9BFD2"
GREEN = "#24B987"
RED = "#E85C5C"
BORDER = "#1E4664"

# Lista de usuarios do codigo original.
usuarios = [
    {
        "nome": "Alex Leonardo Clarindo de Lima",
        "email": "alexclarindo@hotmail.com",
        "telefone": "81 999083372",
        "cpf": "06986115431",
        "conta": "01074029-4",
        "agencia": "3295",
        "saldo": 7500.00,
    },
    {
        "nome": "Carolina  Vieira Andrade",
        "email": "caroleleli@outlook.com",
        "telefone": "81 994562226",
        "cpf": "06986115728",
        "conta": "01089029-9",
        "agencia": "3294",
        "saldo": 3500.00,
    },
    {
        "nome": "Ryhan Naubert",
        "email": "Ryhan Naubert@outlook.com",
        "telefone": "81 984679731",
        "cpf": "02786245769",
        "conta": "01069015-3",
        "agencia": "3287",
        "saldo": 4500.00,
    },
]

# Prepara saldo e extrato para cada usuario.
for usuario in usuarios:
    usuario["saldo"] = Decimal(str(usuario["saldo"]))
    usuario.setdefault("extrato", [])

def formatar_dinheiro(valor):
    """Transforma um valor numerico em formato brasileiro: R$ 1.234,56."""
    valor = Decimal(str(valor))
    numero = f"{abs(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    sinal = "- " if valor < 0 else ""
    return f"{sinal}R$ {numero}"


def converter_valor(texto):
    """Aceita valores como 25,90; 25.90; e 1.250,90."""
    texto = texto.strip().replace("R$", "").replace(" ", "")
    if not texto:
        raise InvalidOperation
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return Decimal(texto)


class BancoLeaoDoNorte:
    def __init__(self, janela):
        self.janela = janela
        self.usuario_atual = usuarios[0]
        self.saldo_visivel = True
        self.pagina_atual = "Início"
        self.nav_buttons = {}

        self.janela.title("Leão do Norte | Banco")
        self.janela.geometry("1180x780")
        self.janela.minsize(980, 650)
        self.janela.configure(bg=NAVY)

        self._configurar_estilos()
        self._montar_layout()
        self.mostrar_pagina("Início")

    def _configurar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TCombobox", padding=8, font=("Segoe UI", 10))

    def _montar_layout(self):
        # Barra superior
        cabecalho = tk.Frame(self.janela, bg=NAVY_DARK, padx=22, pady=13)
        cabecalho.pack(side="top", fill="x")

        marca = tk.Frame(cabecalho, bg=NAVY_DARK)
        marca.pack(side="left")
        selo = tk.Frame(marca, bg=GOLD, width=43, height=43)
        selo.pack(side="left")
        selo.pack_propagate(False)
        tk.Label(selo, text="LN", bg=GOLD, fg=NAVY,
                 font=("Georgia", 15, "bold")).pack(expand=True)
        texto_marca = tk.Frame(marca, bg=NAVY_DARK)
        texto_marca.pack(side="left", padx=10)
        tk.Label(texto_marca, text="LEÃO DO NORTE", bg=NAVY_DARK, fg=GOLD,
                 font=("Georgia", 16, "bold")).pack(anchor="w")
        tk.Label(texto_marca, text="BANCO  •  TRADIÇÃO QUE MOVE SEUS SONHOS",
                 bg=NAVY_DARK, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w")

        self.lbl_usuario_topo = tk.Label(cabecalho, text="Conta de Alex",
                                         bg=NAVY_DARK, fg=WHITE,
                                         font=("Segoe UI", 10, "bold"))
        self.lbl_usuario_topo.pack(side="right", padx=(12, 0))
        tk.Label(cabecalho, text="●  PROTÓTIPO DE ESTUDO", bg=NAVY_DARK, fg=GREEN,
                 font=("Segoe UI", 8, "bold")).pack(side="right", pady=8)

        corpo = tk.Frame(self.janela, bg=NAVY)
        corpo.pack(fill="both", expand=True)

        # Menu lateral
        self.sidebar = tk.Frame(corpo, bg=NAVY_DARK, width=225, padx=13, pady=20)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="MENU PRINCIPAL", bg=NAVY_DARK, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=10, pady=(0, 12))

        itens_menu = [
            ("Início", "⌂"),
            ("Transferências", "⇄"),
            ("Sacar", "↓"),
            ("Depositar", "↑"),
            ("Pagamentos", "▤"),
            ("Extrato", "≡"),
            ("Cartões", "▭"),
            ("Meu perfil", "♙"),
            ("Trocar usuário", "⇆"),
        ]
        for pagina, icone in itens_menu:
            botao = tk.Button(
                self.sidebar, text=f"  {icone}   {pagina}", anchor="w",
                command=lambda p=pagina: self.mostrar_pagina(p),
                bg=NAVY_DARK, fg=WHITE, activebackground=PANEL_LIGHT,
                activeforeground=GOLD, relief="flat", bd=0, cursor="hand2",
                font=("Segoe UI", 10), padx=10, pady=10
            )
            botao.pack(fill="x", pady=2)
            self.nav_buttons[pagina] = botao

        tk.Label(self.sidebar, text="Versão 1.0 • Python/Tkinter\nDados temporários neste protótipo",
                 bg=NAVY_DARK, fg=MUTED, justify="left",
                 font=("Segoe UI", 8)).pack(side="bottom", anchor="w", padx=8, pady=5)

        # Area central com canvas para que o conteudo possa rolar em janelas menores.
        self.area_principal = tk.Frame(corpo, bg=NAVY)
        self.area_principal.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(self.area_principal, bg=NAVY, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.area_principal, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.conteudo = tk.Frame(self.canvas, bg=NAVY, padx=28, pady=24)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.conteudo, anchor="nw")
        self.conteudo.bind("<Configure>", self._atualizar_scroll)
        self.canvas.bind("<Configure>", self._ajustar_largura_conteudo)

    def _atualizar_scroll(self, _evento=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _ajustar_largura_conteudo(self, evento):
        self.canvas.itemconfigure(self.canvas_window, width=evento.width)

    def _limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def _titulo(self, titulo, descricao=""):
        tk.Label(self.conteudo, text=titulo, bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 24, "bold")).pack(anchor="w")
        if descricao:
            tk.Label(self.conteudo, text=descricao, bg=NAVY, fg=MUTED,
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 18))
        else:
            tk.Frame(self.conteudo, bg=NAVY, height=15).pack()

    def _card(self, pai, bg=PANEL, **kwargs):
        return tk.Frame(pai, bg=bg, highlightbackground=BORDER,
                        highlightthickness=1, **kwargs)

    def _botao(self, pai, texto, comando, principal=True, **kwargs):
        return tk.Button(
            pai, text=texto, command=comando,
            bg=GOLD if principal else PANEL_LIGHT,
            fg=NAVY if principal else WHITE,
            activebackground=GOLD_DARK if principal else PANEL,
            activeforeground=NAVY if principal else WHITE,
            relief="flat", bd=0, font=("Segoe UI", 10, "bold"),
            cursor="hand2", padx=16, pady=10, **kwargs
        )

    def _label(self, pai, texto, **kwargs):
        opcoes = {"bg": NAVY, "fg": WHITE, "font": ("Segoe UI", 10)}
        opcoes.update(kwargs)
        return tk.Label(pai, text=texto, **opcoes)

    def _formatar_saldo(self):
        if not self.saldo_visivel:
            return "R$ ••••••"
        return formatar_dinheiro(self.usuario_atual["saldo"])

    def _registrar(self, usuario, texto):
        usuario["extrato"].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} • {texto}")

    def mostrar_pagina(self, pagina):
        self.pagina_atual = pagina
        self._limpar_conteudo()
        for nome, botao in self.nav_buttons.items():
            botao.configure(bg=PANEL_LIGHT if nome == pagina else NAVY_DARK,
                            fg=GOLD if nome == pagina else WHITE)

        self.lbl_usuario_topo.configure(text=f"Conta de {self.usuario_atual['nome'].split()[0]}")
        self.canvas.yview_moveto(0)

        rotas = {
            "Início": self._pagina_inicio,
            "Transferências": self._pagina_transferencias,
            "Sacar": self._pagina_saque,
            "Depositar": self._pagina_deposito,
            "Pagamentos": self._pagina_pagamentos,
            "Extrato": self._pagina_extrato,
            "Cartões": self._pagina_cartoes,
            "Meu perfil": self._pagina_perfil,
            "Trocar usuário": self._pagina_trocar_usuario,
        }
        rotas.get(pagina, self._pagina_inicio)()

    def _pagina_inicio(self):
        usuario = self.usuario_atual
        self._titulo(f"Olá, {usuario['nome'].split()[0]}!", "Acompanhe sua conta e faça operações do menu.")

        saldo_card = tk.Frame(self.conteudo, bg=PANEL, padx=24, pady=21)
        saldo_card.pack(fill="x", pady=(0, 18))
        tk.Label(saldo_card, text="SALDO DISPONÍVEL", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        linha = tk.Frame(saldo_card, bg=PANEL)
        linha.pack(fill="x", pady=(5, 8))
        tk.Label(linha, text=self._formatar_saldo(), bg=PANEL, fg=GOLD,
                 font=("Segoe UI", 28, "bold")).pack(side="left")
        tk.Button(linha, text="◉", command=self._alternar_saldo, bg=PANEL, fg=WHITE,
                  activebackground=PANEL, relief="flat", bd=0,
                  cursor="hand2", font=("Segoe UI", 15)).pack(side="left", padx=12)
        tk.Label(saldo_card, text=f"Agência {usuario['agencia']}   •   Conta {usuario['conta']}",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w")

        self._label(self.conteudo, "Acesso rápido", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(3, 10))
        acoes = tk.Frame(self.conteudo, bg=NAVY)
        acoes.pack(fill="x")
        atalhos = [
            ("Transferir", "⇄", "Transferências"),
            ("Sacar", "↓", "Sacar"),
            ("Depositar", "↑", "Depositar"),
            ("Ver extrato", "≡", "Extrato"),
        ]
        for nome, icone, pagina in atalhos:
            bloco = tk.Frame(acoes, bg=PANEL, padx=13, pady=14)
            bloco.pack(side="left", fill="both", expand=True, padx=(0, 8))
            tk.Label(bloco, text=icone, bg=PANEL, fg=GOLD,
                     font=("Segoe UI", 23, "bold")).pack(anchor="w")
            tk.Button(bloco, text=nome, command=lambda p=pagina: self.mostrar_pagina(p),
                      bg=PANEL, fg=WHITE, activebackground=PANEL_LIGHT,
                      relief="flat", bd=0, cursor="hand2",
                      font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 0))

        cabecalho = tk.Frame(self.conteudo, bg=NAVY)
        cabecalho.pack(fill="x", pady=(23, 10))
        self._label(cabecalho, "Movimentações recentes", font=("Segoe UI", 15, "bold")).pack(side="left")
        tk.Button(cabecalho, text="Ver extrato completo →", command=lambda: self.mostrar_pagina("Extrato"),
                  bg=NAVY, fg=GOLD, activebackground=NAVY, relief="flat", bd=0,
                  cursor="hand2", font=("Segoe UI", 9, "bold")).pack(side="right")
        self._lista_extrato(limite=4)

    def _alternar_saldo(self):
        self.saldo_visivel = not self.saldo_visivel
        self.mostrar_pagina(self.pagina_atual)

    def _lista_extrato(self, limite=None):
        caixa = self._card(self.conteudo, bg=PANEL)
        caixa.pack(fill="x")
        movimentacoes = self.usuario_atual["extrato"]
        if limite is not None:
            movimentacoes = movimentacoes[-limite:]
        if not movimentacoes:
            tk.Label(caixa, text="Nenhuma movimentação realizada nesta sessão.", bg=PANEL,
                     fg=MUTED, font=("Segoe UI", 10), padx=16, pady=22).pack(anchor="w")
            return
        for movimentacao in reversed(movimentacoes):
            linha = tk.Frame(caixa, bg=PANEL, padx=14, pady=11)
            linha.pack(fill="x")
            tk.Label(linha, text="↔", bg=PANEL, fg=GOLD,
                     font=("Segoe UI", 16, "bold")).pack(side="left", padx=(0, 12))
            tk.Label(linha, text=movimentacao, bg=PANEL, fg=WHITE,
                     font=("Segoe UI", 10), anchor="w", justify="left", wraplength=650).pack(side="left", fill="x", expand=True)
            tk.Frame(caixa, bg=BORDER, height=1).pack(fill="x")

    def _campo(self, pai, rotulo, largura=42):
        tk.Label(pai, text=rotulo, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(11, 5))
        campo = tk.Entry(pai, width=largura, bg="#092238", fg=WHITE,
                         insertbackground=WHITE, relief="flat", bd=0,
                         font=("Segoe UI", 11))
        campo.pack(fill="x", ipady=9)
        return campo

    def _cartao_formulario(self, pagina, descricao):
        self._titulo(pagina, descricao)
        form = tk.Frame(self.conteudo, bg=PANEL, padx=22, pady=20)
        form.pack(fill="x", anchor="n")
        return form

    def _valor_do_campo(self, campo):
        try:
            valor = converter_valor(campo.get())
        except (InvalidOperation, ValueError):
            messagebox.showerror("Valor inválido", "Digite um valor válido. Exemplo: 150,50")
            return None
        if valor <= 0:
            messagebox.showerror("Valor inválido", "O valor deve ser maior que zero.")
            return None
        return valor

    def _pagina_saque(self):
        form = self._cartao_formulario("Saque", "Retire um valor da conta selecionada.")
        tk.Label(form, text=f"Titular: {self.usuario_atual['nome']}", bg=PANEL, fg=WHITE,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(form, text=f"Saldo atual: {formatar_dinheiro(self.usuario_atual['saldo'])}",
                 bg=PANEL, fg=GOLD, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(6, 0))
        campo = self._campo(form, "Valor do saque (R$)")

        def confirmar():
            valor = self._valor_do_campo(campo)
            if valor is None:
                return
            if valor > self.usuario_atual["saldo"]:
                messagebox.showerror("Saldo insuficiente", "O valor do saque é maior que o saldo disponível.")
                return
            if not messagebox.askyesno("Confirmar saque", f"Sacar {formatar_dinheiro(valor)}?"):
                return
            self.usuario_atual["saldo"] -= valor
            self._registrar(self.usuario_atual, f"Saque: - {formatar_dinheiro(valor)}")
            messagebox.showinfo("Saque realizado", f"Saque registrado. Saldo atual: {formatar_dinheiro(self.usuario_atual['saldo'])}")
            self.mostrar_pagina("Início")

        self._botao(form, "Confirmar saque", confirmar).pack(anchor="w", pady=(20, 0))

    def _pagina_deposito(self):
        form = self._cartao_formulario("Depósito", "Adicione um valor ao saldo demonstrativo da conta selecionada.")
        tk.Label(form, text=f"Titular: {self.usuario_atual['nome']}", bg=PANEL, fg=WHITE,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        campo = self._campo(form, "Valor do depósito (R$)")

        def confirmar():
            valor = self._valor_do_campo(campo)
            if valor is None:
                return
            if not messagebox.askyesno("Confirmar depósito", f"Adicionar {formatar_dinheiro(valor)} ao saldo?"):
                return
            self.usuario_atual["saldo"] += valor
            self._registrar(self.usuario_atual, f"Depósito: + {formatar_dinheiro(valor)}")
            messagebox.showinfo("Depósito realizado", f"Saldo atual: {formatar_dinheiro(self.usuario_atual['saldo'])}")
            self.mostrar_pagina("Início")

        self._botao(form, "Confirmar depósito", confirmar).pack(anchor="w", pady=(20, 0))

    def _pagina_transferencias(self):
        form = self._cartao_formulario("Pix e transferências", "Transfira entre os usuários cadastrados neste protótipo.")
        tk.Label(form, text=f"Origem: {self.usuario_atual['nome']}  •  Saldo: {formatar_dinheiro(self.usuario_atual['saldo'])}",
                 bg=PANEL, fg=WHITE, font=("Segoe UI", 10, "bold"), wraplength=650,
                 justify="left").pack(anchor="w")
        tk.Label(form, text="Destinatário", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(15, 5))
        self.destinatarios = [u for u in usuarios if u is not self.usuario_atual]
        nomes = [f"{u['nome']} — Agência {u['agencia']} / Conta {u['conta']}" for u in self.destinatarios]
        destinatario_var = tk.StringVar(value=nomes[0] if nomes else "")
        combo = ttk.Combobox(form, textvariable=destinatario_var, values=nomes,
                             state="readonly", font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=5)
        campo_valor = self._campo(form, "Valor da transferência (R$)")
        campo_descricao = self._campo(form, "Descrição (opcional)")

        def confirmar():
            valor = self._valor_do_campo(campo_valor)
            if valor is None:
                return
            if not self.destinatarios or combo.current() < 0:
                messagebox.showerror("Destinatário inválido", "Escolha um destinatário.")
                return
            if valor > self.usuario_atual["saldo"]:
                messagebox.showerror("Saldo insuficiente", "O valor é maior que o saldo disponível.")
                return
            destinatario = self.destinatarios[combo.current()]
            descricao = campo_descricao.get().strip()
            resumo = f"Transferir {formatar_dinheiro(valor)} para {destinatario['nome']}?"
            if descricao:
                resumo += f"\nDescrição: {descricao}"
            if not messagebox.askyesno("Confirmar transferência", resumo):
                return

            # Mantem a regra original: debita o remetente, credita o destinatario,
            # e registra as duas movimentacoes nos extratos separados.
            self.usuario_atual["saldo"] -= valor
            destinatario["saldo"] += valor
            texto_descricao = f" ({descricao})" if descricao else ""
            self._registrar(self.usuario_atual,
                            f"Transferência enviada para {destinatario['nome']}: - {formatar_dinheiro(valor)}{texto_descricao}")
            self._registrar(destinatario,
                            f"Transferência recebida de {self.usuario_atual['nome']}: + {formatar_dinheiro(valor)}{texto_descricao}")
            messagebox.showinfo("Transferência concluída", "Transferência simulada registrada com sucesso.\nNenhum dinheiro real foi movimentado.")
            self.mostrar_pagina("Início")

        self._botao(form, "Confirmar transferência", confirmar).pack(anchor="w", pady=(20, 0))

    def _pagina_extrato(self):
        self._titulo("Extrato da conta", f"Movimentações de {self.usuario_atual['nome']}.")
        resumo = self._card(self.conteudo, bg=PANEL, padx=18, pady=15)
        resumo.pack(fill="x", pady=(0, 14))
        tk.Label(resumo, text="SALDO ATUAL", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(resumo, text=formatar_dinheiro(self.usuario_atual["saldo"]),
                 bg=PANEL, fg=GOLD, font=("Segoe UI", 23, "bold")).pack(anchor="w", pady=(4, 0))
        self._lista_extrato()

    def _pagina_trocar_usuario(self):
        self._titulo("Escolher usuário", "Selecione uma das contas cadastradas no seu código original.")
        form = tk.Frame(self.conteudo, bg=PANEL, padx=22, pady=22)
        form.pack(fill="x")
        tk.Label(form, text="Conta selecionada", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 7))
        nomes = [f"{u['nome']}  |  Agência {u['agencia']}  |  Conta {u['conta']}" for u in usuarios]
        selecionado = tk.StringVar(value=nomes[usuarios.index(self.usuario_atual)])
        combo = ttk.Combobox(form, textvariable=selecionado, values=nomes,
                             state="readonly", font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=5)
        tk.Label(form, text="Nota: esta seleção é para testes locais, não é um login seguro.",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 9), wraplength=650,
                 justify="left").pack(anchor="w", pady=(13, 0))

        def aplicar():
            indice = combo.current()
            if indice < 0:
                messagebox.showerror("Seleção necessária", "Escolha um usuário.")
                return
            self.usuario_atual = usuarios[indice]
            self.saldo_visivel = True
            self.mostrar_pagina("Início")

        self._botao(form, "Abrir conta selecionada", aplicar).pack(anchor="w", pady=(18, 0))

    def _pagina_perfil(self):
        usuario = self.usuario_atual
        self._titulo("Meu perfil", "Dados do cadastro que está selecionado.")
        dados = [
            ("Nome completo", usuario["nome"]),
            ("E-mail", usuario["email"]),
            ("Telefone", usuario["telefone"]),
            ("CPF", usuario["cpf"]),
            ("Agência", usuario["agencia"]),
            ("Conta", usuario["conta"]),
        ]
        for rotulo, valor in dados:
            caixa = self._card(self.conteudo, bg=PANEL, padx=16, pady=12)
            caixa.pack(fill="x", pady=4)
            tk.Label(caixa, text=rotulo.upper(), bg=PANEL, fg=MUTED,
                     font=("Segoe UI", 8, "bold")).pack(anchor="w")
            tk.Label(caixa, text=valor, bg=PANEL, fg=WHITE,
                     font=("Segoe UI", 11)).pack(anchor="w", pady=(3, 0))

    def _pagina_pagamentos(self):
        self._titulo("Pagamentos", "Área visual para uma futura função de pagamento de contas.")
        card = self._card(self.conteudo, bg=PANEL, padx=22, pady=22)
        card.pack(fill="x")
        tk.Label(card, text="Pagamentos ainda não fazem parte do código bancário original.",
                 bg=PANEL, fg=WHITE, font=("Segoe UI", 12, "bold"), wraplength=650,
                 justify="left").pack(anchor="w")
        tk.Label(card, text="Para não alterar seu saldo sem uma regra implementada, esta tela é somente informativa. Nenhum boleto ou conta será pago.",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 10), wraplength=650,
                 justify="left").pack(anchor="w", pady=(9, 17))
        self._botao(card, "Voltar ao início", lambda: self.mostrar_pagina("Início"), principal=False).pack(anchor="w")

    def _pagina_cartoes(self):
        self._titulo("Cartões", "Cartão ilustrativo — sem conexão com uma operadora ou banco real.")
        cartao = tk.Frame(self.conteudo, bg=GOLD, padx=25, pady=22, height=220)
        cartao.pack(fill="x", pady=(0, 18))
        cartao.pack_propagate(False)
        tk.Label(cartao, text="♛  LEÃO DO NORTE", bg=GOLD, fg=NAVY,
                 font=("Georgia", 20, "bold")).pack(anchor="w")
        tk.Label(cartao, text="BANCO", bg=GOLD, fg=NAVY,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(cartao, text="••••  ••••  ••••  1234", bg=GOLD, fg=NAVY,
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(27, 9))
        nome = self.usuario_atual["nome"].upper()
        tk.Label(cartao, text=f"{nome[:32]}     CARTÃO ILUSTRATIVO", bg=GOLD, fg=NAVY,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self._botao(self.conteudo, "Simular bloqueio do cartão", lambda: messagebox.showinfo(
            "Demonstração", "Este protótipo não está conectado a um cartão real; nada foi bloqueado."), principal=False).pack(anchor="w", pady=4)
        self._botao(self.conteudo, "Ver fatura (demonstração)", lambda: messagebox.showinfo(
            "Fatura", "Ainda não existe uma função de fatura no código original."), principal=False).pack(anchor="w", pady=4)


if __name__ == "__main__":
    janela = tk.Tk()
    aplicativo = BancoLeaoDoNorte(janela)
    janela.mainloop()
