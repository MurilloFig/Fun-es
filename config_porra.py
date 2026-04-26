from sympy import symbols

x = symbols("x")

FUNCOES = {
    "x²": "x**2",
    "x³": "x**3",
    "sen(x)": "sin(x)",
    "cos(x)": "cos(x)",
    "e^x": "exp(x)",
    "ln(x)": "log(x)",
    "1/x": "1/x",
    "Personalizada": "custom"
}

OPERADORES = ["+", "-", "*", "/"]

INTERVALO_INICIAL = (-10.0, 10.0)

ANIMACAO = {
    "interval_ms": 100,
    "frames_f1": 12,
    "pausa1": 5,
    "frames_f2": 12,
    "pausa2": 5,
    "frames_resultado": 12,
    "pausa_final": 4,
}