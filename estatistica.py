import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Aprendendo Estatística com Python", layout="wide")

st.title("📊 Aprendendo Estatística com Python")
st.markdown("""
Este app foi criado para você que quer entender os conceitos básicos de estatística de forma simples e visual.
Você poderá digitar seus próprios números e aprender, com gráficos modernos e interativos, o que significam média, mediana, moda, variância, desvio padrão e percentis.
""")

# Entrada de dados
st.sidebar.header("Digite seus números")
st.sidebar.success(' ✅ Fique à vontade para modificar os números abaixo e explorar como os conceitos mudam.')
entrada = st.sidebar.text_area(
    "Informe números separados por vírgula (exemplo: 3, 5, 2, 5, 8, 10, 3)",
    value="3, 5, 2, 5, 8, 10, 3"
)

def processa_entrada(txt):
    try:
        lista = [float(x.strip()) for x in txt.split(",") if x.strip() != '']
        if len(lista) == 0:
            return None
        return lista
    except:
        return None

numeros = processa_entrada(entrada)

if numeros is None:
    st.error("Por favor, digite números válidos separados por vírgula.")
    st.stop()

df = pd.DataFrame({"Valores": numeros})
df_ordenado = df.sort_values(by="Valores").reset_index(drop=True)

st.subheader("Seus números")
st.write(df["Valores"].to_list())

# Estatísticas
def calcula_media(nums): return sum(nums) / len(nums)
def calcula_mediana(nums):
    n = len(nums)
    s = sorted(nums)
    if n % 2 == 1:
        return s[n//2]
    else:
        return (s[n//2 - 1] + s[n//2]) / 2
def calcula_moda(nums):
    c = Counter(nums)
    freq_max = max(c.values())
    modas = [k for k,v in c.items() if v==freq_max]
    if freq_max == 1:
        return []
    return modas
def calcula_variancia(nums):
    m = calcula_media(nums)
    return sum((x - m)**2 for x in nums) / (len(nums)-1)
def calcula_desvio_padrao(nums):
    return np.sqrt(calcula_variancia(nums))
def calcula_percentil(nums,p):
    return np.percentile(nums,p)

media = calcula_media(numeros)
mediana = calcula_mediana(numeros)
moda = calcula_moda(numeros)
variancia = calcula_variancia(numeros)
desvio = calcula_desvio_padrao(numeros)
p25 = calcula_percentil(numeros,25)
p50 = calcula_percentil(numeros,50)
p75 = calcula_percentil(numeros,75)

# ---- Média ----
st.markdown("---")
st.header("Média")

formula_media = r"\text{Média} = \frac{\text{soma dos valores}}{\text{quantidade de valores}}"
valores_str = " + ".join(str(int(n)) if n.is_integer() else str(n) for n in numeros)
formula_caso = fr"\frac{{{valores_str}}}{{{len(numeros)}}} = {media:.2f}"

st.markdown("A **média** é o valor obtido somando todos os números e dividindo pelo total de números.")
st.latex(formula_media)
st.markdown("No seu caso:")
st.latex(formula_caso)
st.markdown("""
**Interpretando:**  
A média é um valor que representa o "centro" dos seus dados, mas ela pode ser influenciada por números muito grandes ou muito pequenos (outliers).
""")

fig = px.histogram(df, x="Valores", nbins=20, title="Histograma com linha da Média", color_discrete_sequence=["CornflowerBlue"])
fig.add_vline(x=media, line_dash="dash", line_color="black", annotation_text="Média", annotation_position="top right")
st.plotly_chart(fig, use_container_width=True)

# ---- Mediana ----
st.markdown("---")
st.header("Mediana")

st.markdown(f"""
A **mediana** é o número que fica no meio quando colocamos os dados em ordem crescente.

Se a quantidade de números for ímpar, a mediana é o número central.  
Se for par, é a média dos dois números centrais.

Seus números ordenados:  
{df_ordenado["Valores"].to_list()}

Como você tem {len(numeros)} números, a mediana é: **{mediana:.2f}**

**Por que usar mediana?**  
Porque a mediana não é afetada por números muito altos ou muito baixos (outliers), diferente da média.
""")

fig = px.histogram(df, x="Valores", nbins=20, title="Histograma com linha da Mediana", color_discrete_sequence=["PowderBlue"])
fig.add_vline(x=mediana, line_dash="dash", line_color="green", annotation_text="Mediana", annotation_position="top right")
st.plotly_chart(fig, use_container_width=True)

# ---- Moda ----
st.markdown("---")
st.header("Moda")

if len(moda) == 0:
    st.write("Não há moda, pois todos os números aparecem a mesma quantidade de vezes.")
else:
    st.write(f"A **moda** é o(s) valor(es) que aparece(m) com maior frequência.")
    st.write(f"No seu caso, moda(s): {moda}")

fig = px.histogram(df, x="Valores", nbins=20, title="Histograma com linha(s) da Moda", color_discrete_sequence=["DarkGray"])
for m in moda:
    fig.add_vline(x=m, line_dash="dash", line_color="blue", annotation_text="Moda", annotation_position="top right")
st.plotly_chart(fig, use_container_width=True)

# ---- Variância e Desvio Padrão ----
st.markdown("---")
st.header("Variância e Desvio Padrão")

st.markdown("**Variância** mede o quanto os números estão espalhados em torno da média.")
st.markdown("É calculada pela média dos quadrados das diferenças entre cada número e a média:")

st.latex(r"\text{Variância} = \frac{\sum (x_i - \bar{x})^2}{n - 1}")

st.markdown(r"""onde:

- \(x_i\) são os valores individuais  
- \(\{x}\) é a média dos valores  
- \(n\) é o número total de valores  
""")

st.markdown("**Exemplo no seu caso:**")

exemplo_variancia = []
for x in numeros:
    diff = x - media
    diff2 = diff**2
    exemplo_variancia.append((x, diff, diff2))
df_var = pd.DataFrame(exemplo_variancia, columns=["Valor", "Diferença para Média", "Diferença²"])
st.write(df_var)
st.markdown(f"Somatório das diferenças²: {df_var['Diferença²'].sum():.2f}")
st.markdown(f"Dividido por n-1 = {len(numeros)-1} resulta na variância: **{variancia:.2f}**")

st.markdown(f"""
O **desvio padrão** é a raiz quadrada da variância, que volta para a mesma unidade dos dados.

No seu caso, o desvio padrão é: **{desvio:.2f}**

**Interpretando:**  
- Desvio padrão pequeno significa que os dados estão próximos da média.  
- Desvio padrão grande significa que os dados estão bem espalhados.
""")

fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(len(numeros))), y=sorted(numeros), mode='markers',
                         marker=dict(size=12, color='#a6d854'), name="Valores Ordenados"))
fig.add_shape(type="line", x0=0, y0=media, x1=len(numeros)-1, y1=media,
              line=dict(color="red", dash="dash"), name="Média")
fig.add_trace(go.Scatter(x=[0, len(numeros)-1], y=[media-desvio, media-desvio],
                         mode='lines', line=dict(color='red', width=0), showlegend=False))
fig.add_trace(go.Scatter(x=[0, len(numeros)-1], y=[media+desvio, media+desvio],
                         mode='lines', line=dict(color='red', width=0), fill='tonexty',
                         fillcolor='rgba(255,0,0,0.2)', showlegend=True, name="± 1 desvio padrão"))
fig.update_layout(title="Números ordenados com média e desvio padrão (área vermelha)",
                  xaxis_title="Posição", yaxis_title="Valor")
st.plotly_chart(fig, use_container_width=True)

# ---- Percentis (quartis) ----
st.markdown("---")
st.header("Percentis (incluindo quartis)")

st.markdown(f"""
Percentis dividem seus números em 100 partes iguais.

- O 25º percentil (Q1) é o valor que separa os 25% menores dados: **{p25:.2f}**  
- O 50º percentil (Q2) é a mediana: **{p50:.2f}**  
- O 75º percentil (Q3) é o valor que separa os 25% maiores dados: **{p75:.2f}**

Eles ajudam a entender como os dados estão distribuídos, especialmente se há muitos valores pequenos ou grandes.
""")

# Boxplot interativo com anotações claras
fig = go.Figure()

fig.add_trace(go.Box(x=df["Valores"], boxpoints='outliers', marker_color='#66c2a5', name="Valores"))

# Adicionando anotações para Q1, mediana e Q3
fig.add_annotation(x=p25, y=0.85, text="Q1 (25%)", showarrow=True, arrowhead=2, arrowsize=1,
                   arrowcolor="black", ax=0, ay=-40)
fig.add_annotation(x=p50, y=0.85, text="Mediana (50%)", showarrow=True, arrowhead=2, arrowsize=1,
                   arrowcolor="green", ax=0, ay=-40, font=dict(color="green"))
fig.add_annotation(x=p75, y=0.85, text="Q3 (75%)", showarrow=True, arrowhead=2, arrowsize=1,
                   arrowcolor="black", ax=0, ay=-40)

# Se tiver muitos outliers, o gráfico mostra todos de forma automática, plotly é ótimo nisso.

fig.update_layout(title="Boxplot — mediana, quartis e outliers",
                  yaxis=dict(showticklabels=False),
                  height=400)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.write("""
---
### Recapitulando:

| Conceito         | O que é?                                               | Quando usar?                                     |
|------------------|--------------------------------------------------------|-------------------------------------------------|
| **Média**        | Soma dos valores dividido pela quantidade              | Para dados simétricos e sem valores extremos    |
| **Mediana**      | Valor do meio quando dados ordenados                   | Para dados com valores extremos (outliers)      |
| **Moda**         | Valor que aparece mais vezes                            | Para dados categóricos ou quando quer saber valor mais comum |
| **Variância**    | Média dos quadrados das diferenças em relação à média  | Para medir dispersão dos dados                    |
| **Desvio Padrão**| Raiz quadrada da variância                              | Medida mais intuitiva de dispersão                |
| **Percentis**    | Valores que dividem os dados em partes iguais          | Para entender a posição relativa de um valor no conjunto |
""")

