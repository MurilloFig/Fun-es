import tkinter as tk
from tkinter import messagebox

from config_porra import FUNCOES, OPERADORES
from utils_da_desgraca import obter_texto_funcao, criar_funcoes_numericas
from plotador_do_caralho import PlotadorDoCaralho


class InterfaceFudida:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Funções")
        self.root.configure(bg="#f4f4f4")

        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        largura_janela = int(largura_tela * 0.90)
        altura_janela = int(altura_tela * 0.85)

        pos_x = int((largura_tela - largura_janela) / 2)
        pos_y = int((altura_tela - altura_janela) / 2)

        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.root.minsize(700, 500)

        self.funcao1_var = tk.StringVar(value="x²")
        self.funcao2_var = tk.StringVar(value="x²")
        self.operador_var = tk.StringVar(value="+")
        self.custom1_var = tk.StringVar()
        self.custom2_var = tk.StringVar()

        self.criar_interface()
        self.atualizar_estado_entries()

    def criar_interface(self):
        self.canvas = tk.Canvas(self.root, bg="#f4f4f4", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)

        self.frame_principal = tk.Frame(self.canvas, bg="#f4f4f4")

        self.frame_principal.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.janela_canvas = self.canvas.create_window(
            (0, 0),
            window=self.frame_principal,
            anchor="n"
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.janela_canvas,
                width=event.width
            )
        )

        titulo = tk.Label(
            self.frame_principal,
            text="Operações com Funções",
            font=("Arial", 24, "bold"),
            bg="#f4f4f4"
        )
        titulo.pack(pady=20)

        frame1 = tk.LabelFrame(
            self.frame_principal,
            text="Primeira função",
            font=("Arial", 13, "bold"),
            padx=15,
            pady=15,
            bg="#f4f4f4"
        )
        frame1.pack(fill="x", padx=20, pady=10)

        self.criar_botoes_funcao(frame1, self.funcao1_var)

        self.entry1 = tk.Entry(
            frame1,
            textvariable=self.custom1_var,
            font=("Arial", 14),
            justify="center"
        )
        self.entry1.pack(pady=10, fill="x", padx=20)

        frame2 = tk.LabelFrame(
            self.frame_principal,
            text="Segunda função",
            font=("Arial", 13, "bold"),
            padx=15,
            pady=15,
            bg="#f4f4f4"
        )
        frame2.pack(fill="x", padx=20, pady=10)

        self.criar_botoes_funcao(frame2, self.funcao2_var)

        self.entry2 = tk.Entry(
            frame2,
            textvariable=self.custom2_var,
            font=("Arial", 14),
            justify="center"
        )
        self.entry2.pack(pady=10, fill="x", padx=20)

        frame_op = tk.LabelFrame(
            self.frame_principal,
            text="Operação",
            font=("Arial", 13, "bold"),
            padx=15,
            pady=15,
            bg="#f4f4f4"
        )
        frame_op.pack(fill="x", padx=20, pady=10)

        op_container = tk.Frame(frame_op, bg="#f4f4f4")
        op_container.pack(fill="x")

        for indice, op in enumerate(OPERADORES):
            rb = tk.Radiobutton(
                op_container,
                text=op,
                variable=self.operador_var,
                value=op,
                indicatoron=False,
                height=2,
                font=("Arial", 18, "bold"),
                bg="white",
                relief="raised",
                bd=2,
                selectcolor="#d9ead3"
            )
            rb.grid(row=0, column=indice, padx=8, pady=8, sticky="nsew")
            op_container.grid_columnconfigure(indice, weight=1)

        frame_acao = tk.Frame(self.frame_principal, bg="#f4f4f4")
        frame_acao.pack(fill="x", padx=20, pady=25)

        botao_plotar = tk.Button(
            frame_acao,
            text="Plotar gráfico animado",
            font=("Arial", 15, "bold"),
            height=2,
            bg="#4CAF50",
            fg="white",
            activebackground="#3d9140",
            activeforeground="white",
            command=self.plotar_animado
        )
        botao_plotar.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        botao_limpar = tk.Button(
            frame_acao,
            text="Limpar personalizados",
            font=("Arial", 15, "bold"),
            height=2,
            bg="#d9534f",
            fg="white",
            activebackground="#b52b27",
            activeforeground="white",
            command=self.limpar
        )
        botao_limpar.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        frame_acao.grid_columnconfigure(0, weight=1)
        frame_acao.grid_columnconfigure(1, weight=1)

    def criar_botoes_funcao(self, parent, variable):
        frame_botoes = tk.Frame(parent, bg="#f4f4f4")
        frame_botoes.pack(fill="x")

        quantidade_colunas = 4

        for indice, nome in enumerate(FUNCOES):
            linha = indice // quantidade_colunas
            coluna = indice % quantidade_colunas

            rb = tk.Radiobutton(
                frame_botoes,
                text=nome,
                variable=variable,
                value=nome,
                indicatoron=False,
                height=2,
                font=("Arial", 12, "bold"),
                command=self.atualizar_estado_entries,
                bg="white",
                relief="raised",
                bd=2,
                selectcolor="#d9ead3"
            )

            rb.grid(row=linha, column=coluna, padx=8, pady=8, sticky="nsew")

        for coluna in range(quantidade_colunas):
            frame_botoes.grid_columnconfigure(coluna, weight=1)

    def atualizar_estado_entries(self):
        self.entry1.config(
            state="normal" if self.funcao1_var.get() == "Personalizada" else "disabled"
        )
        self.entry2.config(
            state="normal" if self.funcao2_var.get() == "Personalizada" else "disabled"
        )

    def limpar(self):
        self.custom1_var.set("")
        self.custom2_var.set("")

    def plotar_animado(self):
        try:
            texto1 = obter_texto_funcao(self.funcao1_var.get(), self.custom1_var.get())
            texto2 = obter_texto_funcao(self.funcao2_var.get(), self.custom2_var.get())
            operador = self.operador_var.get()

            pacote = criar_funcoes_numericas(texto1, texto2, operador)

            plotador = PlotadorDoCaralho(
                pacote["f_num"],
                pacote["g_num"],
                pacote["w_num"],
                pacote["expressao1"],
                pacote["expressao2"],
                pacote["expressao_resultado"],
                operador
            )
            plotador.mostrar()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")