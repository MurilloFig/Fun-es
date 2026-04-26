import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.ticker import FuncFormatter

from config_porra import INTERVALO_INICIAL, ANIMACAO
from utils_da_desgraca import calcular_curvas, limites_y, funcoes_sao_iguais


class PlotadorDoCaralho:
    def __init__(self, f_num, g_num, w_num, expressao1, expressao2, expressao_resultado, operador):
        self.f_num = f_num
        self.g_num = g_num
        self.w_num = w_num
        self.expressao1 = expressao1
        self.expressao2 = expressao2
        self.expressao_resultado = expressao_resultado
        self.operador = operador

        self.ani = None
        self.fig = None
        self.ax = None
        self.line1 = None
        self.line2 = None
        self.line3 = None
        self.texto_animacao = None

        self.estado = {
            "x_vals": None,
            "y_vals": None,
            "z_vals": None,
            "w_vals": None,
            "funcoes_iguais": False,
            "atualizando": False,
        }

    def formatar_y(self, valor, _pos):
        valor_abs = abs(valor)

        if valor_abs >= 1_000_000_000:
            return f"{valor/1_000_000_000:.1f}B"
        if valor_abs >= 1_000_000:
            return f"{valor/1_000_000:.1f}M"
        if valor_abs >= 1_000:
            return f"{valor/1_000:.1f}k"
        if valor_abs >= 1:
            return f"{valor:.0f}"
        return f"{valor:.2f}"

    def recalcular_curvas_visiveis(self, xmin, xmax):
        x_vals, y_vals, z_vals, w_vals = calcular_curvas(
            self.f_num, self.g_num, self.w_num, xmin, xmax
        )

        self.estado["x_vals"] = x_vals
        self.estado["y_vals"] = y_vals
        self.estado["z_vals"] = z_vals
        self.estado["w_vals"] = w_vals
        self.estado["funcoes_iguais"] = funcoes_sao_iguais(y_vals, z_vals)

        ymin, ymax = limites_y(y_vals, z_vals, w_vals)
        self.ax_real.set_ylim(ymin, ymax)

        def normalizar(v):
            validos = v[np.isfinite(v)]
            if len(validos) == 0:
                return np.full_like(v, np.nan)

            vmax = np.max(np.abs(validos))
            if vmax == 0:
                return np.zeros_like(v)

            return v / vmax

        y_norm = normalizar(y_vals)
        z_norm = normalizar(z_vals)
        w_norm = normalizar(w_vals)

        self.estado["y_norm"] = y_norm
        self.estado["z_norm"] = z_norm
        self.estado["w_norm"] = w_norm

        self.ax_norm.set_ylim(-1.2, 1.2)

    def aplicar_estilo_legenda(self):
        if self.estado["funcoes_iguais"]:
            self.line1.set_linestyle("--")
            self.line1.set_linewidth(3.0)
            self.line1.set_label(f"f(x) = g(x) = {self.expressao1}")

            self.line2.set_alpha(0.0)
            self.line2.set_linewidth(0.0)
        else:
            self.line1.set_linestyle("-")
            self.line1.set_linewidth(2.5)
            self.line1.set_alpha(1.0)
            self.line1.set_label(f"f(x) = {self.expressao1}")

            self.line2.set_alpha(1.0)
            self.line2.set_linewidth(2.5)
            self.line2.set_label(f"g(x) = {self.expressao2}")

        self.line3.set_label(f"resultado = {self.expressao_resultado}")
        self.ax.legend()

    def init_animacao(self):
        self.line1.set_data([], [])
        self.line2.set_data([], [])
        self.line3.set_data([], [])

        self.line1_norm.set_data([], [])
        self.line2_norm.set_data([], [])
        self.line3_norm.set_data([], [])

        self.texto_animacao.set_text("")
        return (
            self.line1, self.line2, self.line3,
            self.line1_norm, self.line2_norm, self.line3_norm,
            self.texto_animacao
        )

    def pontos_ate_frame(self, frame_atual, total_frames_etapa):
        proporcao = min((frame_atual + 1) / total_frames_etapa, 1.0)
        qtd = max(1, int(len(self.estado["x_vals"]) * proporcao))
        return qtd

    def update_animacao(self, frame):
        x_vals = self.estado["x_vals"]
        y_vals = self.estado["y_vals"]
        z_vals = self.estado["z_vals"]
        w_vals = self.estado["w_vals"]
        y_norm = self.estado["y_norm"]
        z_norm = self.estado["z_norm"]
        w_norm = self.estado["w_norm"]
        funcoes_iguais = self.estado["funcoes_iguais"]

        frames_f1 = ANIMACAO["frames_f1"]
        pausa1 = ANIMACAO["pausa1"]
        frames_f2 = ANIMACAO["frames_f2"]
        pausa2 = ANIMACAO["pausa2"]
        frames_resultado = ANIMACAO["frames_resultado"]

        if frame < frames_f1:
            i = self.pontos_ate_frame(frame, frames_f1)

            self.line1.set_data(x_vals[:i], y_vals[:i])
            self.line1_norm.set_data(x_vals[:i], y_norm[:i])

            self.line2.set_data([], [])
            self.line2_norm.set_data([], [])

            self.line3.set_data([], [])
            self.line3_norm.set_data([], [])

            self.texto_animacao.set_text("Construindo f(x)...")

        elif frame < frames_f1 + pausa1:
            self.line1.set_data(x_vals, y_vals)
            self.line1_norm.set_data(x_vals, y_norm)

            self.line2.set_data([], [])
            self.line2_norm.set_data([], [])

            self.line3.set_data([], [])
            self.line3_norm.set_data([], [])

            self.texto_animacao.set_text("f(x) estabilizada")

        elif frame < frames_f1 + pausa1 + frames_f2:
            etapa_frame = frame - (frames_f1 + pausa1)
            j = self.pontos_ate_frame(etapa_frame, frames_f2)

            self.line1.set_data(x_vals, y_vals)
            self.line1_norm.set_data(x_vals, y_norm)

            if funcoes_iguais:
                self.line2.set_data([], [])
                self.line2_norm.set_data([], [])
            else:
                self.line2.set_data(x_vals[:j], z_vals[:j])
                self.line2_norm.set_data(x_vals[:j], z_norm[:j])

            self.line3.set_data([], [])
            self.line3_norm.set_data([], [])

            self.texto_animacao.set_text("Construindo g(x)...")

        elif frame < frames_f1 + pausa1 + frames_f2 + pausa2:
            self.line1.set_data(x_vals, y_vals)
            self.line1_norm.set_data(x_vals, y_norm)

            if funcoes_iguais:
                self.line2.set_data([], [])
                self.line2_norm.set_data([], [])
            else:
                self.line2.set_data(x_vals, z_vals)
                self.line2_norm.set_data(x_vals, z_norm)

            self.line3.set_data([], [])
            self.line3_norm.set_data([], [])

            self.texto_animacao.set_text("g(x) estabilizada")

        elif frame < frames_f1 + pausa1 + frames_f2 + pausa2 + frames_resultado:
            etapa_frame = frame - (frames_f1 + pausa1 + frames_f2 + pausa2)
            k = self.pontos_ate_frame(etapa_frame, frames_resultado)

            self.line1.set_data(x_vals, y_vals)
            self.line1_norm.set_data(x_vals, y_norm)

            if funcoes_iguais:
                self.line2.set_data([], [])
                self.line2_norm.set_data([], [])
            else:
                self.line2.set_data(x_vals, z_vals)
                self.line2_norm.set_data(x_vals, z_norm)

            self.line3.set_data(x_vals[:k], w_vals[:k])
            self.line3_norm.set_data(x_vals[:k], w_norm[:k])

            self.texto_animacao.set_text(f"Aplicando operação: f(x) {self.operador} g(x)")

        else:
            self.line1.set_data(x_vals, y_vals)
            self.line1_norm.set_data(x_vals, y_norm)

            if funcoes_iguais:
                self.line2.set_data([], [])
                self.line2_norm.set_data([], [])
            else:
                self.line2.set_data(x_vals, z_vals)
                self.line2_norm.set_data(x_vals, z_norm)

            self.line3.set_data(x_vals, w_vals)
            self.line3_norm.set_data(x_vals, w_norm)

            self.texto_animacao.set_text(f"Resultado final: f(x) {self.operador} g(x)")

        return (
            self.line1, self.line2, self.line3,
            self.line1_norm, self.line2_norm, self.line3_norm,
            self.texto_animacao
        )

    def iniciar_animacao(self):
        if self.ani is not None:
            try:
                self.ani.event_source.stop()
            except Exception:
                pass

        total_frames = (
            ANIMACAO["frames_f1"]
            + ANIMACAO["pausa1"]
            + ANIMACAO["frames_f2"]
            + ANIMACAO["pausa2"]
            + ANIMACAO["frames_resultado"]
            + ANIMACAO["pausa_final"]
        )

        self.init_animacao()
        self.ani = FuncAnimation(
            self.fig,
            self.update_animacao,
            frames=total_frames,
            init_func=self.init_animacao,
            interval=ANIMACAO["interval_ms"],
            blit=False,
            repeat=False,
        )
        self.fig.canvas.draw_idle()

    def redesenhar_sem_animacao(self):
        self.aplicar_estilo_legenda()

        self.line1.set_data(self.estado["x_vals"], self.estado["y_vals"])
        self.line1_norm.set_data(self.estado["x_vals"], self.estado["y_norm"])

        if self.estado["funcoes_iguais"]:
            self.line2.set_data([], [])
            self.line2_norm.set_data([], [])
        else:
            self.line2.set_data(self.estado["x_vals"], self.estado["z_vals"])
            self.line2_norm.set_data(self.estado["x_vals"], self.estado["z_norm"])

        self.line3.set_data(self.estado["x_vals"], self.estado["w_vals"])
        self.line3_norm.set_data(self.estado["x_vals"], self.estado["w_norm"])

        xmin, xmax = self.ax_real.get_xlim()
        self.texto_animacao.set_text(f"Visualizando intervalo: {xmin:.2f} até {xmax:.2f}")
        self.fig.canvas.draw_idle()

    def atualizar_intervalo_visivel(self):
        if self.estado["atualizando"]:
            return

        self.estado["atualizando"] = True
        try:
            xmin, xmax = self.ax.get_xlim()
            self.recalcular_curvas_visiveis(xmin, xmax)
            self.redesenhar_sem_animacao()
        finally:
            self.estado["atualizando"] = False

    def on_xlim_changed(self, _axes):
        self.atualizar_intervalo_visivel()

    def on_scroll(self, event):
        if event.inaxes != self.ax:
            return

        xmin, xmax = self.ax.get_xlim()
        xdata = event.xdata

        if xdata is None:
            xdata = (xmin + xmax) / 2

        largura_atual = xmax - xmin
        fator_zoom = 0.9 if event.button == "up" else 1.1
        nova_largura = max(largura_atual * fator_zoom, 0.001)

        proporcao_esquerda = (xdata - xmin) / largura_atual if largura_atual != 0 else 0.5
        proporcao_direita = 1 - proporcao_esquerda

        novo_xmin = xdata - nova_largura * proporcao_esquerda
        novo_xmax = xdata + nova_largura * proporcao_direita

        self.ax.set_xlim(novo_xmin, novo_xmax)
        self.fig.canvas.draw_idle()

    def resetar(self, _event):
        self.ax.set_xlim(*INTERVALO_INICIAL)
        self.recalcular_curvas_visiveis(*INTERVALO_INICIAL)
        self.iniciar_animacao()

    def mostrar(self):
        self.fig, (self.ax_real, self.ax_norm) = plt.subplots(
            2, 1, figsize=(10, 7), sharex=True
        )

        manager = self.fig.canvas.manager
        try:
            manager.window.state("zoomed")
        except Exception:
            pass
        self.fig.canvas.manager.set_window_title("Gráfico das Funções")
        plt.subplots_adjust(bottom=0.18, hspace=0.28)

        self.ax = self.ax_real  # mantém compatibilidade com o resto do código

        intervalo_inicial = (-10.0, 10.0)

        # -------- GRÁFICO REAL --------
        self.ax_real.set_title("Gráfico das Funções", fontsize=17, fontweight="bold")
        self.ax_real.set_ylabel("y real", fontsize=12)
        self.ax_real.grid(True, alpha=0.35)
        self.ax_real.axhline(0, linewidth=1, color="gray", alpha=0.8)
        self.ax_real.axvline(0, linewidth=1, color="gray", alpha=0.8)
        self.ax_real.set_xlim(*intervalo_inicial)
        self.ax_real.yaxis.set_major_formatter(FuncFormatter(self.formatar_y))

        # -------- GRÁFICO NORMALIZADO --------
        self.ax_norm.set_title("Comparação Visual Normalizada", fontsize=14, fontweight="bold")
        self.ax_norm.set_xlabel("x", fontsize=12)
        self.ax_norm.set_ylabel("y normalizado", fontsize=12)
        self.ax_norm.grid(True, alpha=0.35)
        self.ax_norm.axhline(0, linewidth=1, color="gray", alpha=0.8)
        self.ax_norm.axvline(0, linewidth=1, color="gray", alpha=0.8)
        self.ax_norm.set_xlim(*intervalo_inicial)

        self.line1, = self.ax_real.plot([], [], linewidth=2.5, label=f"f(x) = {self.expressao1}")
        self.line2, = self.ax_real.plot([], [], linewidth=2.5, label=f"g(x) = {self.expressao2}")
        self.line3, = self.ax_real.plot([], [], linewidth=3.0, label=f"resultado = {self.expressao_resultado}")

        self.line1_norm, = self.ax_norm.plot([], [], linewidth=2.5, label=f"f(x) = {self.expressao1}")
        self.line2_norm, = self.ax_norm.plot([], [], linewidth=2.5, label=f"g(x) = {self.expressao2}")
        self.line3_norm, = self.ax_norm.plot([], [], linewidth=3.0, label=f"resultado = {self.expressao_resultado}")

        self.texto_animacao = self.ax_real.text(
            0.02, 0.92,
            "",
            transform=self.ax_real.transAxes,
            fontsize=12,
            fontweight="bold",
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
        )

        self.recalcular_curvas_visiveis(*intervalo_inicial)
        self.aplicar_estilo_legenda()

        self.ax_real.callbacks.connect("xlim_changed", self.on_xlim_changed)
        self.fig.canvas.mpl_connect("scroll_event", self.on_scroll)

        ax_botao = plt.axes([0.40, 0.04, 0.20, 0.045])
        btn_reset = Button(ax_botao, "Reiniciar animação")
        btn_reset.on_clicked(self.resetar)

        self.iniciar_animacao()
        plt.show()