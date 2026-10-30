import itertools
import re
import pandas as pd
import streamlit as st
st.set_page_config(page_title="Calculadora Tabla de la Verdad", layout="centered")
st.title("🧮 Calculadora de Tabla de la Verdad")
st.subheader("GRUPO #3")
st.write("Integrantes 👨‍💻:")
st.write("Reyes Cruzatty Danny Moises, Ferrin Cornejo Luis Anthony y Gonzalez Sala Carlos Xavier")
st.write("▪️Calculadora de expresiones lógicas")
st.markdown("▪️Construye tu expresión haciendo clic. El resultado se mostrará exclusivamente en 0 y 1.")
# Estado de la sesión
if "expr" not in st.session_state:
    st.session_state.expr = ""
# Interfaz: constructor de expresión
st.subheader("🛠️ Constructor de Expresión")
cols = st.columns(6)
variables = ["A", "B", "C", "D", "E", "F"]
for e, v in enumerate(variables):
    with cols[e % 6]:
        if st.button(v, key=f"btn_{v}", use_container_width=True):
            st.session_state.expr += f" {v} "
st.markdown("---")
st.write("Operadores:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("(^) AND"):
        st.session_state.expr += " AND "
with col2:
    if st.button("(v) OR"):
        st.session_state.expr += " OR "
with col3:
    if st.button("(¬) NOT"):
        st.session_state.expr += " NOT "
with col4:
    if st.button("(⊕) XOR"):
        st.session_state.expr += " XOR "
col5, col6, col7, col8 = st.columns(4)
with col5:
    if st.button("(→) IMPLICA"):
        st.session_state.expr += " → "
with col6:
    if st.button("(↔) BICONDICIONAL"):
        st.session_state.expr += " ↔ "
# Paréntesis y botones para borrar
with col7:
    if st.button("(", use_container_width=True):
        st.session_state.expr += " ( "
with col8:
    if st.button(")", use_container_width=True):
        st.session_state.expr += " ) "
col9, col10 = st.columns(2)
with col9:
    if st.button("🗑️ Limpiar Todo", use_container_width=True):
        st.session_state.expr = ""
with col10:
    if st.button("⌫ Borrar Último", use_container_width=True):
        partes = st.session_state.expr.split()
        if partes:
            partes.pop()
        st.session_state.expr = " ".join(partes)
# Expresión actual
st.markdown("---")
st.write("Expresión actual:")
st.code(st.session_state.expr.strip() or "(vacío)", language="text")
st.markdown("---")
# Lógica central
def normalizar_expresion(expr: str) -> str:
    e = expr.strip().upper()
    e = re.sub(r"\bAND\b", " and ", e)
    e = re.sub(r"\bOR\b", " or ", e)
    e = re.sub(r"\bNOT\b", " not ", e)
    e = re.sub(r"\bXOR\b", " ^ ", e)
    # Implicación y bicondicional entre variables proposicionales.
    # La implicación P -> Q equivale a (not P or Q).
    # El bicondicional P <-> Q equivale a (P == Q).
    e = re.sub(r"\b([A-F])\s*<->\s*([A-F])\b", r"(\1 == \2)", e)
    e = re.sub(r"\b([A-F])\s*->\s*([A-F])\b", r"(not \1 or \2)", e)
    return re.sub(r"\s+", " ", e).strip()
def extraer_variables(expr: str) -> list:
    return sorted(set(re.findall(r"\b[A-F]\b", expr.upper())))
def generar_tabla(expr_raw: str):
    if not expr_raw.strip():
        return [], []
    expr_norm = normalizar_expresion(expr_raw)
    variables = extraer_variables(expr_raw)
    if not variables:
        return [], []
    tabla = []
    for valores in itertools.product([0, 1], repeat=len(variables)):
        entorno = {v: bool(val) for v, val in zip(variables, valores)}
        try:
            resultado = eval(expr_norm, {"__builtins__": {}}, entorno)
            fila = list(valores) + [int(bool(resultado))]
            tabla.append(fila)
        except Exception:
            return [], []
    return variables, tabla
# Ejecución
if st.button("🚀 Generar Tabla", type="primary", use_container_width=True):
    if not st.session_state.expr.strip():
        st.warning("⚠️ Ingresa o construye una expresión primero.")
    else:
        vars_, tabla = generar_tabla(st.session_state.expr)
        if not vars_:
            st.error("❌ Expresión inválida o con variables no detectadas. Revisa los operadores y el orden de la expresión.")
        else:
            cols_df = vars_ + ["Resultado"]
            df = pd.DataFrame(tabla, columns=cols_df)
            st.success(f"✅ Tabla generada para {len(vars_)} variable(s)")
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar CSV", csv, "tabla_verdad.csv", "text/csv")
