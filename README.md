# Calculadora de Funções com Gráfico Animado

Este projeto é uma aplicação em Python com interface gráfica feita em Tkinter. O objetivo do programa é permitir que o usuário escolha duas funções matemáticas, selecione uma operação entre elas e visualize o resultado em gráficos animados.

A aplicação permite trabalhar com funções pré-definidas e também com funções personalizadas digitadas pelo próprio usuário.

## Funcionalidades

- Interface gráfica adaptável ao tamanho da tela.
- Escolha de duas funções matemáticas.
- Suporte a funções personalizadas.
- Operações entre funções:
  - Soma `+`
  - Subtração `-`
  - Multiplicação `*`
  - Divisão `/`
- Geração de gráfico animado.
- Exibição de gráfico real e gráfico normalizado.
- Zoom com o scroll do mouse.
- Botão para reiniciar a animação.
- Tratamento de erros para expressões inválidas.

## Estrutura do Projeto

O projeto está dividido nos seguintes arquivos:

```text
main.py
interface.py
plotador.py
utils.py
config.py
pyproject.toml
README.md
main.py

Arquivo principal do projeto. Ele inicia a janela Tkinter e carrega a interface da aplicação.

interface.py

Contém a classe responsável pela interface gráfica. Neste arquivo ficam os botões, campos de entrada, seleção das funções e escolha da operação matemática.

plotador.py

Contém a classe responsável por criar e animar os gráficos usando Matplotlib.

utils.py

Contém funções auxiliares para transformar expressões matemáticas em funções numéricas, calcular os pontos dos gráficos e definir os limites do eixo Y.

config.py

Contém as configurações principais do projeto, como:

funções pré-definidas;
operadores disponíveis;
intervalo inicial do gráfico;
configurações da animação.
Requisitos

Para executar o projeto, é necessário ter Python instalado.

As principais bibliotecas utilizadas são:

tkinter
numpy
sympy
matplotlib

O tkinter normalmente já vem instalado junto com o Python.

As demais dependências podem ser instaladas com:

pip install numpy sympy matplotlib

Caso esteja usando uv, execute:

uv sync
Como Executar

Abra o terminal dentro da pasta do projeto e execute:

python main.py

Ao executar o programa, será aberta uma janela com a calculadora de funções.

Como Usar

A interface possui três partes principais:

Escolha da primeira função.
Escolha da segunda função.
Escolha da operação entre elas.

Depois de selecionar as funções e a operação desejada, clique no botão:

Plotar gráfico animado

O sistema abrirá uma nova janela com os gráficos animados.

Funções Pré-Definidas

O programa possui algumas funções prontas para uso:

x²
x³
sen(x)
cos(x)
e^x
ln(x)
1/x

Essas opções podem ser selecionadas diretamente pelos botões da interface.

Como Usar Funções Personalizadas

Também é possível escrever uma função manualmente usando a opção:

Personalizada

Ao selecionar essa opção, o campo de texto será habilitado.

Nesse campo, a função deve ser escrita em formato reconhecido pelo Python/SymPy.

Exemplos de funções personalizadas
x**2 - 1

Representa:

x² - 1
x**3 + 2*x

Representa:

x³ + 2x
sin(x)

Representa:

sen(x)
cos(x)

Representa:

cos(x)
exp(x)

Representa:

e^x
log(x)

Representa:

ln(x)
1/x

Representa:

1 dividido por x
Atenção Sobre Potência

Para escrever potência, o recomendado é usar dois asteriscos:

x**2

Isso representa:

x²

Portanto, para escrever a função:

x² - 1

digite:

x**2 - 1

Algumas pessoas escrevem potência como:

x^2 - 1

Porém, em Python, o símbolo ^ não é o operador padrão de potência. Por isso, para evitar erro ou interpretação incorreta, utilize sempre:

x**2 - 1
Exemplos de Operações

Se a primeira função for:

f(x) = x**2

E a segunda função for:

g(x) = x

Com a operação +, o resultado será:

x**2 + x

Com a operação -, o resultado será:

x**2 - x

Com a operação *, o resultado será:

x**2 * x

Com a operação /, o resultado será:

x**2 / x
Observações Importantes
Use * para multiplicação.
Use ** para potência.
Use sin(x) para seno.
Use cos(x) para cosseno.
Use exp(x) para exponencial.
Use log(x) para logaritmo natural.
Evite dividir por zero, pois isso pode gerar pontos indefinidos no gráfico.
Caso a função tenha valores inválidos em certos pontos, o sistema tenta ignorar esses pontos no gráfico.
Exemplos Válidos
x**2 + 3*x - 1
sin(x) + cos(x)
exp(x) - x
log(x)
1/(x + 2)
(x**2 - 1)/(x + 1)