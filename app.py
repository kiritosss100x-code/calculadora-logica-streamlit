import itertools
import re

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Lógica Lab | Tablas de verdad",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# ESTILO VISUAL: VERDE SALVIA, CREMA Y NARANJA SUAVE
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Nunito:wght@500;600;700;800;900&display=swap');

:root {
    --cream: #F7F5EE;
    --paper: #FFFEFA;
    --sage: #A8BFA3;
    --sage-dark: #536B55;
    --forest: #34483A;
    --orange: #E6A36B;
    --ink: #28352C;
    --muted: #718071;
    --line: #E3E7DC;
}

.stApp {
    background:
        radial-gradient(circle at 8% 2%,
            rgba(168,191,163,.22), transparent 27%),
        radial-gradient(circle at 95% 15%,
            rgba(230,163,107,.13), transparent 24%),
        var(--cream);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(247,245,238,.86);
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    max-width: 1120px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label,
[data-testid="stMarkdownContainer"] {
    color: var(--ink);
}

.hero {
    text-align: center;
    padding: 1.1rem 0 1.55rem;
    animation: appear .65s ease both;
}

.hero-kicker {
    display: inline-block;
    background: #E7EDE2;
    color: var(--sage-dark);
    border: 1px solid #D6E0D1;
    border-radius: 999px;
    padding: .42rem .85rem;
    font-size: .75rem;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Nunito', sans-serif;
    font-size: clamp(2.3rem, 5vw, 3.65rem);
    font-weight: 900;
    line-height: 1.1;
    margin: .75rem 0 .35rem;
    color: var(--forest);
}

.hero-title span {
    color: var(--sage-dark);
}

.hero-subtitle {
    color: var(--muted);
    font-size: 1.02rem;
    margin: 0 auto;
    max-width: 650px;
}

.panel {
    background: rgba(255,254,250,.94);
    border: 1px solid var(--line);
    border-radius: 23px;
    padding: 1.3rem 1.4rem;
    box-shadow:
        0 9px 26px rgba(52,72,58,.07),
        0 2px 5px rgba(52,72,58,.035);
    margin-bottom: 1.1rem;
    animation: rise .45s ease both;
}

.section-heading {
    font-family: 'Nunito', sans-serif;
    font-size: 1.25rem;
    font-weight: 900;
    color: var(--forest);
    margin: .1rem 0 1rem;
}

.expression-label {
    color: var(--sage-dark);
    font-size: .76rem;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-weight: 900;
    margin: .35rem 0 .6rem;
}

.expression-box {
    background: #F4F5EF;
    border: 1px dashed #B8C8B2;
    border-radius: 15px;
    padding: 1rem 1.1rem;
    min-height: 3.2rem;
    color: var(--forest);
    font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
    font-size: 1.04rem;
    font-weight: 700;
    overflow-wrap: anywhere;
}

div.stButton > button,
div.stDownloadButton > button {
    border: 1px solid #D9E2D5;
    border-radius: 14px;
    min-height: 2.75rem;
    background: #F2F5EF;
    color: #3D5942;
    font-weight: 800;
    transition:
        transform .16s ease,
        box-shadow .16s ease,
        background .16s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: #9DB69A;
    background: #E7EEE3;
    color: #2E4B34;
    box-shadow: 0 6px 14px rgba(52,72,58,.10);
    transform: translateY(-2px);
}

div.stButton > button:active {
    transform: translateY(0);
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(110deg, #607C61, #3F6045);
    color: #fffdf7;
    border: 0;
    border-radius: 15px;
    min-height: 3.25rem;
    font-size: 1rem;
    letter-spacing: .015em;
    box-shadow: 0 8px 18px rgba(63,96,69,.20);
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(110deg, #6E896D, #4C6D51);
    box-shadow: 0 10px 22px rgba(63,96,69,.24);
}

div[data-testid="stDataFrame"] {
    border: 1px solid #DDE5D8;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 5px 16px rgba(52,72,58,.05);
}

div[data-testid="stMetric"] {
    background: #FFFEFA;
    border: 1px solid #E2E8DD;
    border-radius: 17px;
    padding: .8rem 1rem;
    box-shadow: 0 5px 14px rgba(52,72,58,.045);
}

div[data-testid="stMetricLabel"] p {
    color: #718071 !important;
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    color: #34483A !important;
}

div[data-testid="stAlert"] {
    border-radius: 15px;
}

details {
    background: #FFFEFA;
    border: 1px solid #E2E8DD;
    border-radius: 15px;
    padding: .25rem .6rem;
}

hr {
    border-color: #E3E7DC;
}

.small-note {
    color: var(--muted);
    font-size: .88rem;
    line-height: 1.55;
}

.footer {
    color: #849080;
    text-align: center;
    font-size: .8rem;
    margin-top: 2.2rem;
}

.pill {
    display: inline-block;
    border-radius: 999px;
    padding: .28rem .65rem;
    background: #E8EFE4;
    color: #4B674D;
    font-size: .78rem;
    font-weight: 800;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(7px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes rise {
    from {
        opacity: 0;
        transform: translateY(5px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-kicker">
        Grupo # 3
        🌱 Laboratorio interactivo de lógica proposicional
    </div>
    <div class="hero-title">
        LÓGICA <span>LAB</span> ✳
    </div>
    <div class="hero-subtitle">
        Arma tu expresión, juega con los operadores
        y deja que la tabla de verdad haga el resto.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# ESTADO DE LA SESIÓN
# ============================================================

if "expr" not in st.session_state:
    st.session_state.expr = ""

if "tabla_generada" not in st.session_state:
    st.session_state.tabla_generada = None

if "error_expr" not in st.session_state:
    st.session_state.error_expr = ""

# ============================================================
# CONSTRUCTOR DE EXPRESIONES
# ============================================================

st.markdown(
    '<div class="panel">',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-heading">'
    '🧩 Constructor de expresiones</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="expression-label">'
    '01 · Elige tus variables</div>',
    unsafe_allow_html=True,
)

variables_disponibles = ["A", "B", "C", "D", "E", "F"]
cols = st.columns(6)

for i, variable in enumerate(variables_disponibles):
    with cols[i]:
        if st.button(
            f"🔤 {variable}",
            key=f"btn_var_{variable}",
            use_container_width=True,
        ):
            st.session_state.expr += f" {variable} "
            st.session_state.tabla_generada = None
            st.session_state.error_expr = ""

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    '<div class="expression-label">'
    '02 · Añade un operador lógico</div>',
    unsafe_allow_html=True,
)

operadores = ["AND", "OR", "NOT", "XOR", "->", "<->"]

iconos_operadores = {
    "AND": " (∧) "
    "OR": " (∨) "
    "NOT": " (¬) "
    "XOR": " (⊕) "
    "->": " (→) "
    "<->": " (↔) "
}

cols = st.columns(6)

for i, operador in enumerate(operadores):
    with cols[i]:
        if st.button(
            f"{iconos_operadores[operador]}  {operador}",
            key=f"btn_op_{operador}",
            use_container_width=True,
        ):
            st.session_state.expr += f" {operador} "
            st.session_state.tabla_generada = None
            st.session_state.error_expr = ""

st.markdown(
    '<div class="expression-label">'
    '03 · Agrupa o corrige tu expresión</div>',
    unsafe_allow_html=True,
)

cols = st.columns([1, 1, 1, 1, 2])

with cols[0]:
    if st.button(
        "( Abrir",
        key="btn_paren_open",
        use_container_width=True,
    ):
        st.session_state.expr += " ( "
        st.session_state.tabla_generada = None
        st.session_state.error_expr = ""

with cols[1]:
    if st.button(
        "Cerrar )",
        key="btn_paren_close",
        use_container_width=True,
    ):
        st.session_state.expr += " ) "
        st.session_state.tabla_generada = None
        st.session_state.error_expr = ""

with cols[2]:
    if st.button(
        "⌫ Borrar",
        key="btn_borrar",
        use_container_width=True,
    ):
        elementos = st.session_state.expr.split()
        if elementos:
            elementos.pop()

        st.session_state.expr = " ".join(elementos)
        st.session_state.tabla_generada = None
        st.session_state.error_expr = ""

with cols[3]:
    if st.button(
        "🧹 Limpiar",
        key="btn_limpiar",
        use_container_width=True,
    ):
        st.session_state.expr = ""
        st.session_state.tabla_generada = None
        st.session_state.error_expr = ""

with cols[4]:
    st.markdown(
        '<div class="small-note">'
        'Consejo: usa paréntesis para indicar qué operaciones '
        'van juntas.</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="expression-label">'
    'Tu expresión actual</div>',
    unsafe_allow_html=True,
)

# Escapamos caracteres especiales para que se muestren como texto.
expresion_visible = (
    st.session_state.expr.strip()
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
)

st.markdown(
    f'<div class="expression-box">'
    f'{expresion_visible or "Pulsa los botones para empezar…"}'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# LÓGICA: TOKENIZADOR Y ANALIZADOR DE EXPRESIONES
#
# Precedencia:
# 1. Paréntesis
# 2. NOT
# 3. AND
# 4. XOR
# 5. OR
# 6. Implicación ->
# 7. Bicondicional <->
# ============================================================

def extraer_variables(expr: str) -> list:
    """Obtiene las variables A, B, C, D, E y F usadas."""
    return sorted(
        set(re.findall(r"\b[A-F]\b", expr.upper()))
    )


def tokenizar(expr: str) -> list:
    """Divide la expresión en variables, operadores y paréntesis."""
    patron = re.compile(
        r"\s*(<->|->|AND\b|OR\b|NOT\b|XOR\b|[A-F]\b|[()])",
        re.IGNORECASE,
    )

    tokens = []
    pos = 0

    while pos < len(expr):
        if expr[pos:].strip() == "":
            break

        coincidencia = patron.match(expr, pos)

        if not coincidencia:
            fragmento = expr[pos:pos + 12]
            raise ValueError(
                f"Símbolo no reconocido cerca de: {fragmento}"
            )

        tokens.append(coincidencia.group(1).upper())
        pos = coincidencia.end()

    if not tokens:
        raise ValueError("La expresión está vacía.")

    return tokens


def evaluar_tokens(tokens: list, entorno: dict) -> bool:
    """Evalúa la expresión respetando la precedencia lógica."""
    pos = 0

    def bicondicional():
        nonlocal pos

        izquierda = implicacion()

        while pos < len(tokens) and tokens[pos] == "<->":
            pos += 1
            derecha = implicacion()
            izquierda = izquierda == derecha

        return izquierda

    def implicacion():
        nonlocal pos

        izquierda = disyuncion()

        if pos < len(tokens) and tokens[pos] == "->":
            pos += 1
            derecha = implicacion()
            return (not izquierda) or derecha

        return izquierda

    def disyuncion():
        nonlocal pos

        izquierda = xor_expr()

        while pos < len(tokens) and tokens[pos] == "OR":
            pos += 1
            derecha = xor_expr()
            izquierda = izquierda or derecha

        return izquierda

    def xor_expr():
        nonlocal pos

        izquierda = conjuncion()

        while pos < len(tokens) and tokens[pos] == "XOR":
            pos += 1
            derecha = conjuncion()
            izquierda = izquierda != derecha

        return izquierda

    def conjuncion():
        nonlocal pos

        izquierda = negacion()

        while pos < len(tokens) and tokens[pos] == "AND":
            pos += 1
            derecha = negacion()
            izquierda = izquierda and derecha

        return izquierda

    def negacion():
        nonlocal pos

        if pos < len(tokens) and tokens[pos] == "NOT":
            pos += 1
            return not negacion()

        return primario()

    def primario():
        nonlocal pos

        if pos >= len(tokens):
            raise ValueError("La expresión está incompleta.")

        token = tokens[pos]

        if token == "(":
            pos += 1
            valor = bicondicional()

            if pos >= len(tokens) or tokens[pos] != ")":
                raise ValueError(
                    "Falta un paréntesis de cierre."
                )

            pos += 1
            return valor

        if token == ")":
            raise ValueError(
                "Hay un paréntesis de cierre sin abrir."
            )

        if token in entorno:
            pos += 1
            return entorno[token]

        raise ValueError(
            f"Se esperaba una variable o un paréntesis, no {token}."
        )

    resultado = bicondicional()

    if pos != len(tokens):
        raise ValueError(
            "Sobran símbolos o falta un operador entre ellos."
        )

    return bool(resultado)


def generar_tabla(expr_raw: str):
    """Genera todas las combinaciones de la tabla de verdad."""
    variables = extraer_variables(expr_raw)

    if not variables:
        raise ValueError(
            "Incluye al menos una variable entre A y F."
        )

    tokens = tokenizar(expr_raw)
    tabla = []

    for valores in itertools.product(
        [0, 1],
        repeat=len(variables),
    ):
        entorno = {
            variable: bool(valor)
            for variable, valor in zip(variables, valores)
        }

        resultado = evaluar_tokens(tokens, entorno)

        tabla.append(
            list(valores) + [int(resultado)]
        )

    return variables, tabla

# ============================================================
# GENERACIÓN Y PRESENTACIÓN DE RESULTADOS
# ============================================================

st.markdown(
    '<div class="section-heading">'
    '📊 Tu tabla de verdad</div>',
    unsafe_allow_html=True,
)

if st.button(
    "🌿 Generar tabla de verdad",
    type="primary",
    use_container_width=True,
):
    if not st.session_state.expr.strip():
        st.session_state.tabla_generada = None
        st.session_state.error_expr = (
            "Primero arma una expresión con los botones de arriba."
        )
    else:
        try:
            vars_, tabla = generar_tabla(
                st.session_state.expr
            )

            st.session_state.tabla_generada = (
                vars_,
                tabla,
            )
            st.session_state.error_expr = ""

        except ValueError as error:
            st.session_state.tabla_generada = None
            st.session_state.error_expr = str(error)

if st.session_state.error_expr:
    st.error(
        f"No pude construir la tabla: "
        f"{st.session_state.error_expr}"
    )

if st.session_state.tabla_generada:
    vars_, tabla = st.session_state.tabla_generada

    df = pd.DataFrame(
        tabla,
        columns=vars_ + ["Resultado"],
    )

    resultados = df["Resultado"].tolist()
    total = len(df)
    verdaderas = sum(resultados)
    falsas = total - verdaderas

    c1, c2, c3 = st.columns(3)

    c1.metric("🧮 Combinaciones", total)
    c2.metric("🌱 Verdaderas (1)", verdaderas)
    c3.metric("🍂 Falsas (0)", falsas)

    if verdaderas == total:
        st.success(
            "¡Tautología! El resultado es verdadero "
            "en todas las combinaciones."
        )

    elif falsas == total:
        st.info(
            "Contradicción: el resultado es falso "
            "en todas las combinaciones."
        )

    else:
        st.info(
            "Contingencia: el resultado cambia según "
            "los valores de las variables."
        )

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading">'
        '🧾 Tabla de verdad</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<span class="pill">'
        'Verde = verdadero (1)</span> &nbsp; '
        '<span class="pill" '
        'style="background:#F8E7DF;color:#8A4939;">'
        'Coral = falso (0)</span>',
        unsafe_allow_html=True,
    )

    def colorear_filas(fila):
        if fila["Resultado"] == 1:
            estilo = (
                "background-color: #E5F0E1; "
                "color: #2F5135; font-weight: 600;"
            )
        else:
            estilo = (
                "background-color: #F8E7DF; "
                "color: #804638; font-weight: 600;"
            )

        return [estilo] * len(fila)

    tabla_estilizada = df.style.apply(
        colorear_filas,
        axis=1,
    )

    st.dataframe(
        tabla_estilizada,
        use_container_width=True,
        hide_index=True,
    )

    csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "📥 Descargar tabla en CSV",
        data=csv,
        file_name="tabla_verdad.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# GUÍA DE OPERADORES
# ============================================================

with st.expander("💡 Guía rápida de operadores"):
    st.markdown("""
    - **AND (∧) — Conjunción:** es verdadera cuando ambas
      proposiciones son verdaderas.
    - **OR (∨) — Disyunción:** es verdadera cuando al menos
      una proposición es verdadera.
    - **NOT (¬) — Negación:** invierte el valor de verdad.
    - **XOR (⊕) — Disyunción exclusiva:** es verdadera cuando
      los valores son diferentes.
    - **-> (→) — Implicación:** solo es falsa cuando el
      antecedente es verdadero y el consecuente es falso.
    - **<-> (↔) — Bicondicional:** es verdadera cuando ambos
      lados tienen el mismo valor.

    **Orden de evaluación:** paréntesis, NOT, AND, XOR, OR,
    implicación y bicondicional. Usa paréntesis cuando quieras
    dejar clara la agrupación.
    """)

st.markdown(
    '<div class="footer">'
    'LÓGICA LAB · Calculadora de tablas de verdad · '
    'Hecha para pensar con estilo 🌿'
    '</div>',
    unsafe_allow_html=True,
)
