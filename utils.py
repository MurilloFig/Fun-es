import numpy as np
from sympy import sympify, lambdify
from config import x, FUNCOES


def obter_texto_funcao(escolha: str, custom_texto: str) -> str:
    expr = FUNCOES[escolha]
    if expr == "custom":
        texto = custom_texto.strip()
        if not texto:
            raise ValueError("Você selecionou função personalizada, mas não digitou a expressão.")
        return texto
    return expr


def criar_funcoes_numericas(texto1: str, texto2: str, operador: str):
    expressao1 = sympify(texto1)
    expressao2 = sympify(texto2)
    expressao_resultado = sympify(f"({texto1}) {operador} ({texto2})")

    f_num = lambdify(x, expressao1, "numpy")
    g_num = lambdify(x, expressao2, "numpy")
    w_num = lambdify(x, expressao_resultado, "numpy")

    return {
        "expressao1": expressao1,
        "expressao2": expressao2,
        "expressao_resultado": expressao_resultado,
        "f_num": f_num,
        "g_num": g_num,
        "w_num": w_num,
    }


def calcular_curvas(f_num, g_num, w_num, xmin: float, xmax: float, pontos: int = 1200):
    if xmin == xmax:
        xmax = xmin + 1

    if xmin > xmax:
        xmin, xmax = xmax, xmin

    x_vals = np.linspace(xmin, xmax, pontos)

    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        y_vals = np.array(f_num(x_vals), dtype=float)
        z_vals = np.array(g_num(x_vals), dtype=float)
        w_vals = np.array(w_num(x_vals), dtype=float)

    y_vals[~np.isfinite(y_vals)] = np.nan
    z_vals[~np.isfinite(z_vals)] = np.nan
    w_vals[~np.isfinite(w_vals)] = np.nan

    return x_vals, y_vals, z_vals, w_vals


def limites_y(y_vals, z_vals, w_vals):
    conjuntos = []

    if np.isfinite(y_vals).any():
        conjuntos.append(y_vals[np.isfinite(y_vals)])
    if np.isfinite(z_vals).any():
        conjuntos.append(z_vals[np.isfinite(z_vals)])
    if np.isfinite(w_vals).any():
        conjuntos.append(w_vals[np.isfinite(w_vals)])

    if not conjuntos:
        return -10, 10

    todos = np.concatenate(conjuntos)
    ymin = np.min(todos)
    ymax = np.max(todos)

    margem = (ymax - ymin) * 0.10 if ymax != ymin else 1
    return ymin - margem, ymax + margem


def funcoes_sao_iguais(y_vals, z_vals):
    return np.allclose(y_vals, z_vals, equal_nan=True)