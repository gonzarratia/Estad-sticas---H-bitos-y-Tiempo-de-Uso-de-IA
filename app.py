from __future__ import annotations

from pathlib import Path
import math

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="IA en perspectiva | Dashboard estadístico",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = {
    "edad",
    "herramienta_ia",
    "nivel_experiencia",
    "frecuencia_semanal",
    "tiempo_uso",
}
EXPERIENCE_ORDER = ["Básico", "Intermedio", "Avanzado"]
LEVEL_COLORS = {
    "Básico": "#A9C9F5",
    "Intermedio": "#4F83D1",
    "Avanzado": "#173E78",
}
DATA_FILE = Path(__file__).resolve().parent / "datos_limpios_ia.csv"


st.markdown(
    """
    <style>
    :root {
      --ink:#17243b; --muted:#63718a; --blue:#3563e9; --mint:#13a98b;
      --paper:#f3f6fb; --line:#e2e9f3;
    }
    html, body, [class*="css"] { font-family:Inter,"DM Sans",Arial,sans-serif; }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
      background:var(--paper); color:var(--ink);
    }
    [data-testid="stHeader"] {
      height:0 !important; min-height:0 !important; background:var(--paper) !important;
      visibility:hidden; border:0;
    }
    [data-testid="stDecoration"], #MainMenu, footer { display:none !important; }
    .block-container { max-width:1480px; padding-top:.55rem !important; padding-bottom:3rem; }
    [data-testid="stSidebar"] { background:#101a30; }
    [data-testid="stSidebar"] > div:first-child {
      background:linear-gradient(180deg,#101a30 0%,#172440 100%);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color:#edf3ff !important; }
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color:#bdc9dc !important; }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
      color:#edf3ff !important; background:rgba(255,255,255,.055);
      border:1px solid rgba(255,255,255,.15); border-radius:14px; padding:8px;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] * { color:#edf3ff !important; }
    [data-testid="stSidebar"] [data-testid="stFileUploaderFileName"] { color:#fff !important; }
    [data-testid="stSidebar"] [data-testid="stExpander"] {
      border:1px solid rgba(255,255,255,.24); border-radius:14px;
      background:rgba(255,255,255,.075);
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary * {
      color:#ffffff !important; font-weight:700;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stCaptionContainer"] * {
      color:#e1eaff !important;
    }
    .sidebar-brand { padding:8px 0 18px; }
    .sidebar-brand .brand-mark {
      color:#9dbaff; font-size:10px; font-weight:800; letter-spacing:.18em;
      text-transform:uppercase; margin-bottom:8px;
    }
    .sidebar-brand .brand-title {
      color:#fff; font:800 21px/1.2 Inter,"DM Sans",sans-serif; letter-spacing:-.03em;
    }
    .sidebar-brand .brand-copy { color:#bdc9dc; font-size:12px; line-height:1.55; margin-top:7px; }
    .hero {
      position:relative; overflow:hidden; padding:30px 34px; margin:0 0 22px;
      border-radius:24px; color:#fff;
      background:linear-gradient(115deg,#142544 0%,#203c73 57%,#3563e9 100%);
      box-shadow:0 18px 42px rgba(26,54,105,.18);
    }
    .hero:after {
      content:''; position:absolute; right:-70px; top:-150px; width:390px; height:390px;
      border:1px solid rgba(255,255,255,.12); border-radius:50%;
      box-shadow:0 0 0 35px rgba(255,255,255,.035),0 0 0 75px rgba(255,255,255,.025);
    }
    .hero-kicker { position:relative; z-index:1; color:#a9c5ff; font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; margin-bottom:9px; }
    .hero-title { position:relative; z-index:1; font:800 clamp(26px,3vw,39px)/1.13 Inter,"DM Sans",sans-serif; letter-spacing:-.045em; margin:0 0 10px; color:#fff; }
    .hero-copy { position:relative; z-index:1; max-width:800px; color:#d7e2f7; font-size:14px; line-height:1.65; margin:0; }
    .hero-chips { position:relative; z-index:1; display:flex; flex-wrap:wrap; gap:9px; margin-top:18px; }
    .hero-chip { display:inline-flex; padding:7px 12px; border-radius:999px; color:#edf3ff; font-size:10px; font-weight:800; letter-spacing:.035em; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.15); }
    .section-heading { margin:18px 0 12px; }
    .section-kicker { color:var(--blue); font-size:10px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; margin-bottom:4px; }
    .section-title { color:var(--ink); font:800 21px/1.25 Inter,"DM Sans",sans-serif; letter-spacing:-.025em; margin:0; }
    .section-copy { color:var(--muted); font-size:13px; line-height:1.6; margin:6px 0 0; }
    [data-testid="stMetric"] { min-height:108px; padding:16px 18px; border:1px solid var(--line); border-radius:17px; background:#fff; box-shadow:0 8px 22px rgba(31,55,91,.055); }
    [data-testid="stMetricLabel"] p { color:#64728a !important; font-size:11px !important; font-weight:700 !important; }
    [data-testid="stMetricValue"] { color:#17243b !important; font:800 24px Inter,"DM Sans",sans-serif !important; }
    [data-testid="stMetricDelta"] { font-size:11px !important; }
    [data-testid="stTabs"] [role="tablist"] { gap:8px; border-bottom:1px solid #dce4f0; }
    [data-testid="stTabs"] button[role="tab"] { padding:11px 16px; border-radius:12px 12px 0 0; color:#64728a; font-weight:700; }
    [data-testid="stTabs"] button[aria-selected="true"] { color:#244fcb; background:#e7edff; }
    div[data-testid="stDataFrame"] { overflow:hidden; border:1px solid var(--line); border-radius:15px; box-shadow:0 8px 22px rgba(31,55,91,.045); }
    [data-testid="stPlotlyChart"] { overflow:hidden; border:1px solid var(--line); border-radius:18px; background:#fff; box-shadow:0 8px 22px rgba(31,55,91,.045); padding:5px 8px 0; }
    div[data-testid="stAlert"] { border-radius:14px; }
    [data-testid="stExpander"] { border:1px solid var(--line); border-radius:14px; background:rgba(255,255,255,.7); }
    hr { border-color:var(--line); }
    @media (max-width:700px) {
      .block-container { padding:0 .9rem 2rem !important; }
      .hero { padding:23px 20px; border-radius:19px; }
      .hero:after { right:-220px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_number(value, digits: int = 2) -> str:
    """Coma decimal, precisión fija y sin separador de miles."""
    if value is None or pd.isna(value):
        return "No disponible"
    return f"{float(value):.{digits}f}".replace(".", ",")


def format_boundary(value) -> str:
    """Muestra límites enteros sin decimales y límites no enteros con dos."""
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return format_number(number)


def parse_boolean(value):
    if pd.isna(value):
        return pd.NA
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "sí", "si", "yes", "verdadero"}:
        return True
    if normalized in {"false", "0", "no", "falso"}:
        return False
    return pd.NA


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    if not DATA_FILE.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo requerido '{DATA_FILE.name}' en la carpeta de la aplicación ({DATA_FILE.parent})."
        )
    data = pd.read_csv(DATA_FILE, encoding="utf-8-sig")

    missing = sorted(REQUIRED_COLUMNS - set(data.columns))
    if missing:
        raise ValueError(
            "El archivo datos_limpios_ia.csv no contiene las columnas requeridas: "
            + ", ".join(missing)
            + "."
        )
    purpose_columns = [column for column in data.columns if column.startswith("finalidad_")]
    if not purpose_columns:
        raise ValueError("El CSV debe incluir al menos una columna de finalidad_ (por ejemplo, finalidad_estudio).")

    for column in ["edad", "frecuencia_semanal", "tiempo_uso"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    for column in ["nivel_experiencia", "herramienta_ia"]:
        data[column] = data[column].astype("string").str.strip()
    return data


def format_mode(series: pd.Series) -> str:
    values = series.dropna()
    if values.empty:
        return "No disponible"
    counts = values.value_counts()
    top_frequency = int(counts.max())
    modes = counts[counts == top_frequency].index.tolist()
    if top_frequency == 1:
        return "Sin moda (todos aparecen una vez)"

    def value_text(value):
        if isinstance(value, (int, np.integer)) or (
            isinstance(value, (float, np.floating)) and float(value).is_integer()
        ):
            return str(int(value))
        if isinstance(value, (float, np.floating)):
            return format_number(value)
        return str(value)

    labels = [value_text(value) for value in modes]
    if len(labels) == 1:
        return f"{labels[0]} (f = {top_frequency})"
    if len(labels) == 2:
        return f"{labels[0]} y {labels[1]} (bimodal, f = {top_frequency})"
    return f"{', '.join(labels[:-1])} y {labels[-1]} (multimodal, f = {top_frequency})"


def frequency_distribution(series: pd.Series):
    """Tabla agrupada: k=ceil(1+log2(n)); A=ceil(rango/k); último intervalo cerrado."""
    values = pd.to_numeric(series, errors="coerce").dropna().astype(float).to_numpy()
    if len(values) == 0:
        return pd.DataFrame(), np.array([]), [], []

    n = len(values)
    minimum = float(values.min())
    maximum = float(values.max())
    value_range = maximum - minimum
    k = max(1, int(math.ceil(1 + math.log2(n))))
    amplitude = max(1, int(math.ceil(value_range / k)))
    number_of_bins = max(1, int(math.ceil(value_range / amplitude)))
    edges = minimum + np.arange(number_of_bins + 1, dtype=float) * amplitude
    if edges[-1] < maximum:
        edges = np.append(edges, edges[-1] + amplitude)
        number_of_bins += 1

    # Los intervalos son [L_i, L_s), salvo el último, que incluye el máximo.
    bin_index = np.searchsorted(edges, values, side="right") - 1
    bin_index = np.clip(bin_index, 0, number_of_bins - 1)
    frequencies = np.bincount(bin_index, minlength=number_of_bins).astype(int)
    relative = frequencies / n
    cumulative = np.cumsum(frequencies)
    cumulative_relative = np.cumsum(relative)
    midpoints = (edges[:-1] + edges[1:]) / 2
    modal_frequency = int(frequencies.max())
    modal_rows = [i for i, frequency in enumerate(frequencies) if frequency == modal_frequency]

    labels = []
    for i in range(number_of_bins):
        left = format_boundary(edges[i])
        right = format_boundary(edges[i + 1])
        closing = "]" if i == number_of_bins - 1 else ")"
        labels.append(f"[{left}, {right}{closing}")

    table = pd.DataFrame(
        {
            "Intervalo": labels,
            "Marca de clase (xᵢ)": midpoints,
            "Frecuencia absoluta (fᵢ)": frequencies,
            "Frecuencia relativa (nᵢ)": relative,
            "Frecuencia acumulada (Fᵢ)": cumulative,
            "Frecuencia relativa acumulada (Nᵢ)": cumulative_relative,
        }
    )
    return table, edges, modal_rows, frequencies.tolist()


def frequency_display_table(table: pd.DataFrame) -> pd.io.formats.style.Styler:
    display = pd.DataFrame(
        {
            "Intervalo": table["Intervalo"].tolist() + ["Total"],
            "Marca de clase (xᵢ)": [format_number(x) for x in table["Marca de clase (xᵢ)"]] + ["—"],
            "Frecuencia absoluta (fᵢ)": [str(int(x)) for x in table["Frecuencia absoluta (fᵢ)"]] + [str(int(table["Frecuencia absoluta (fᵢ)"].sum()))],
            "Frecuencia relativa (nᵢ)": [format_number(x, 4) for x in table["Frecuencia relativa (nᵢ)"]] + ["1,0000"],
            "Frecuencia acumulada (Fᵢ)": [str(int(x)) for x in table["Frecuencia acumulada (Fᵢ)"]] + [str(int(table["Frecuencia absoluta (fᵢ)"].sum()))],
            "Frecuencia relativa acumulada (Nᵢ)": [format_number(x, 4) for x in table["Frecuencia relativa acumulada (Nᵢ)"]] + ["1,0000"],
        }
    )
    modal_rows, total_row = set(table.attrs.get("modal_rows", [])), len(display) - 1

    def row_style(row):
        if row.name == total_row:
            return ["background-color:#e8eef9;color:#17243b;font-weight:800"] * len(row)
        if row.name in modal_rows:
            return ["background-color:#e9f4ff;color:#173e78;font-weight:700"] * len(row)
        return [""] * len(row)

    return (
        display.style
        .set_table_styles([
            {"selector": "th", "props": [("background-color", "#f1f5fb"), ("color", "#17243b"), ("font-weight", "700")]},
            {"selector": "td", "props": [("background-color", "#ffffff"), ("color", "#17243b")]},
        ])
        .set_properties(**{"background-color": "#ffffff", "color": "#17243b"})
        .set_properties(subset=display.columns[1:], **{"text-align": "right"})
        .set_properties(subset=[display.columns[0]], **{"text-align": "left"})
        .apply(row_style, axis=1)
        .hide(axis="index")
    )


def style_plain_table(display: pd.DataFrame):
    return (
        display.style
        .set_table_styles([
            {"selector": "th", "props": [("background-color", "#f1f5fb"), ("color", "#17243b"), ("font-weight", "700")]},
            {"selector": "td", "props": [("background-color", "#ffffff"), ("color", "#17243b")]},
        ])
        .set_properties(**{"background-color": "#ffffff", "color": "#17243b"})
        .set_properties(subset=display.columns[1:], **{"text-align": "right"})
        .set_properties(subset=[display.columns[0]], **{"text-align": "left"})
        .hide(axis="index")
    )


def numeric_summary(series: pd.Series) -> dict:
    values = pd.to_numeric(series, errors="coerce").dropna().astype(float)
    if values.empty:
        return {"values": values, "mean": np.nan, "median": np.nan, "mode": "No disponible",
                "q1": np.nan, "q2": np.nan, "q3": np.nan, "d9": np.nan, "range": np.nan,
                "mad": np.nan, "variance": np.nan, "std": np.nan, "cv": np.nan, "skew": np.nan}
    mean = values.mean()
    std = values.std(ddof=1) if len(values) > 1 else np.nan
    variance = values.var(ddof=1) if len(values) > 1 else np.nan
    cv = (std / abs(mean) * 100) if pd.notna(std) and mean != 0 else np.nan
    return {
        "values": values,
        "mean": mean,
        "median": values.median(),
        "mode": format_mode(values),
        "q1": values.quantile(0.25, interpolation="linear"),
        "q2": values.quantile(0.50, interpolation="linear"),
        "q3": values.quantile(0.75, interpolation="linear"),
        "d9": values.quantile(0.90, interpolation="linear"),
        "range": values.max() - values.min(),
        "mad": (values - mean).abs().mean(),
        "variance": variance,
        "std": std,
        "cv": cv,
        "skew": values.skew(),
    }


def central_position_table(age: dict, time: dict) -> pd.DataFrame:
    measures = [
        ("Media", "mean"),
        ("Mediana", "median"),
        ("Moda", "mode"),
        ("Q₁", "q1"),
        ("Q₂", "q2"),
        ("Q₃", "q3"),
        ("Decil 9 (D₉)", "d9"),
    ]
    rows = []
    for label, key in measures:
        age_value = age[key] if key == "mode" else format_number(age[key])
        time_value = time[key] if key == "mode" else format_number(time[key])
        rows.append({"Medida": label, "Edad (años)": age_value, "Tiempo de uso (min)": time_value})
    return pd.DataFrame(rows)


def dispersion_table(age: dict, time: dict) -> pd.DataFrame:
    rows = [
        ("Rango (años / min)", "range", False),
        ("Desviación media (años / min)", "mad", False),
        ("Varianza muestral s² (años² / min²)", "variance", False),
        ("Desviación típica muestral s (años / min)", "std", False),
        ("Coeficiente de variación (%)", "cv", True),
    ]
    output = []
    for label, key, percent in rows:
        age_value = format_number(age[key]) + (" %" if percent and pd.notna(age[key]) else "")
        time_value = format_number(time[key]) + (" %" if percent and pd.notna(time[key]) else "")
        output.append({"Medida": label, "Edad (años)": age_value, "Tiempo de uso (min)": time_value})
    return pd.DataFrame(output)


def skew_interpretation(label: str, summary: dict) -> str:
    g1 = summary["skew"]
    if pd.isna(g1):
        return f"{label}: G₁ no disponible; se requieren al menos tres observaciones válidas."
    magnitude = abs(g1)
    sign = "positiva" if g1 > 0 else "negativa" if g1 < 0 else "nula"
    if magnitude < 0.5:
        classification = "aproximadamente simétrica" if g1 == 0 else f"aproximadamente simétrica, con sesgo {sign} leve"
    elif magnitude <= 1:
        classification = f"asimetría {sign} moderada"
    else:
        classification = f"asimetría {sign} fuerte"
    return f"{label}: {classification} (G1 = {format_number(g1)})."


def cv_interpretation(label: str, summary: dict) -> str:
    cv = summary["cv"]
    if pd.isna(cv):
        return f"CV de {label}: no disponible."
    level = "alta" if cv > 30 else "moderada" if cv > 15 else "baja"
    return f"CV de {label} = {format_number(cv)} %: variabilidad {level} (criterio descriptivo orientativo)."


def section_header(kicker: str, title: str, description: str | None = None) -> None:
    copy = f'<p class="section-copy">{description}</p>' if description else ""
    st.markdown(
        f'<div class="section-heading"><div class="section-kicker">{kicker}</div>'
        f'<h2 class="section-title">{title}</h2>{copy}</div>',
        unsafe_allow_html=True,
    )


def style_figure(figure, height: int = 390):
    legend_below = (
        figure.layout.legend.orientation == "h"
        and figure.layout.legend.y is not None
        and figure.layout.legend.y < 0
    )
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": "Inter, DM Sans, Arial, sans-serif", "color": "#17243b", "size": 12},
        height=height,
        margin={"l": 18, "r": 20, "t": 58, "b": 78 if legend_below else 35},
        title={"font": {"family": "Inter, DM Sans, Arial, sans-serif", "size": 16, "color": "#17243b"}},
        legend={
            "bgcolor": "#ffffff",
            "font": {"size": 11, "color": "#263653"},
            "font_color": "#263653",
            "title_font": {"color": "#17243b", "family": "Inter, DM Sans, Arial, sans-serif"},
        },
        hoverlabel={"bgcolor": "#17243b", "font": {"color": "#ffffff", "size": 12}},
    )
    figure.update_xaxes(
        showgrid=True, gridcolor="#e7edf5", zeroline=False, linecolor="#dfe6f0",
        tickfont={"color": "#263653", "size": 11},
        title_font={"color": "#17243b", "size": 12, "family": "Inter, DM Sans, Arial, sans-serif"},
    )
    figure.update_yaxes(
        showgrid=True, gridcolor="#e7edf5", zeroline=False, linecolor="#dfe6f0",
        tickfont={"color": "#263653", "size": 11},
        title_font={"color": "#17243b", "size": 12, "family": "Inter, DM Sans, Arial, sans-serif"},
    )
    return figure


def draw_plot(figure, height: int = 390):
    st.plotly_chart(
        style_figure(figure, height),
        use_container_width=True,
        config={"displayModeBar": False},
    )


def purpose_label(column: str) -> str:
    labels = {
        "finalidad_estudio": "Estudio",
        "finalidad_codigo": "Código",
        "finalidad_busqueda": "Búsqueda",
        "finalidad_redaccion": "Redacción",
        "finalidad_entretenimiento": "Entretenimiento",
    }
    if column in labels:
        return labels[column]
    return column.removeprefix("finalidad_").replace("_", " ").capitalize()


def render_numeric_tab(data: pd.DataFrame) -> None:
    age = numeric_summary(data["edad"])
    time = numeric_summary(data["tiempo_uso"])

    section_header("01 · Distribución", "Frecuencias de tiempo de uso", "Intervalos de igual amplitud; clase modal resaltada en azul.")
    table, _, modal_rows, _ = frequency_distribution(data["tiempo_uso"])
    if table.empty:
        st.info("No hay valores válidos de tiempo_uso para calcular frecuencias.")
    else:
        table.attrs["modal_rows"] = modal_rows
        st.dataframe(frequency_display_table(table), hide_index=True, use_container_width=True)
        n = int(table["Frecuencia absoluta (fᵢ)"].sum())
        modal_interval = " y ".join(table.iloc[index]["Intervalo"] for index in modal_rows)
        modal_count = int(table.iloc[modal_rows[0]]["Frecuencia absoluta (fᵢ)"])
        st.markdown(
            f"<div class='interpretation'><b>Lectura:</b> la clase modal es {modal_interval}, "
            f"con {modal_count} observaciones de {n} ({format_number(modal_count / n * 100)} %).</div>",
            unsafe_allow_html=True,
        )

    section_header("02 · Centro y posición", "Medidas de tendencia central y posición", "Cuantiles calculados mediante interpolación lineal entre observaciones ordenadas.")
    central = central_position_table(age, time)
    st.dataframe(style_plain_table(central), hide_index=True, use_container_width=True)
    st.markdown(
        "<div class='interpretation'><b>Lectura:</b> "
        + "<br>".join([
            skew_interpretation("Edad", age),
            skew_interpretation("Tiempo de uso", time),
        ])
        + "</div>",
        unsafe_allow_html=True,
    )

    section_header("03 · Variabilidad", "Medidas de dispersión", "La varianza y la desviación típica son muestrales (ddof = 1).")
    dispersion = dispersion_table(age, time)
    st.dataframe(style_plain_table(dispersion), hide_index=True, use_container_width=True)
    st.markdown(
        "<div class='interpretation'><b>Lectura:</b> "
        + "<br>".join([
            cv_interpretation("edad", age),
            cv_interpretation("tiempo de uso", time),
        ])
        + "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("Notas metodológicas", expanded=False):
        st.markdown("Los resultados describen la **muestra** observada y no se generalizan a la población.")
        st.markdown("**Cuantiles.** Interpolación lineal entre observaciones ordenadas, equivalente a PERCENTIL.INC de Excel; $Q_2$ es la mediana y $D_9$ el percentil 90.")
        st.markdown("**Moda.** Es el valor o los valores más frecuentes; puede no existir una moda repetida o puede haber varias.")
        st.markdown("**Intervalos.** $k = \\lceil 1 + \\log_2(n) \\rceil$; $A = \\lceil \\mathrm{rango}/k \\rceil$. Cada clase es $[L_i,L_s)$, salvo la última, que incluye el máximo.")
        st.markdown("**Marca de clase.** $x_i = (L_i + L_s)/2$. Frecuencias: $f_i$ absoluta; $n_i=f_i/n$; $F_i=\\sum_{j=1}^{i} f_j$; $N_i=\\sum_{j=1}^{i} n_j$.")
        st.markdown("**Dispersión.** Rango $=\\max-\\min$; desviación media $DM=(1/n)\\sum |x_i-\\bar{x}|$.")
        st.latex(r"s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2 \quad (ddof=1)")
        st.markdown(r"Desviación típica muestral: $s=\sqrt{s^2}$. Coeficiente de variación: $CV=(s/|\bar{x}|)\cdot100$.")
        st.latex(r"G_1 = \frac{n}{(n-1)(n-2)} \cdot \sum_{i=1}^{n} \left(\frac{x_i-\bar{x}}{s}\right)^3")
        st.warning("Con n pequeño, G₁ es sensible a valores extremos; interpreta la asimetría con cautela.")
        st.caption(f"En la vista actual: n = {len(data)} observaciones. Cada estadístico usa sus valores no faltantes.")


def render_visual_tab(data: pd.DataFrame) -> None:
    age = numeric_summary(data["edad"])
    time = numeric_summary(data["tiempo_uso"])
    tools = data["herramienta_ia"].dropna()

    section_header("00 · Indicadores", "Señales rápidas de la muestra", "Indicadores recalculados al cambiar el nivel de experiencia.")
    primary1, primary2, primary3 = st.columns(3)
    primary1.metric("Edad promedio", f"{format_number(age['mean'])} años" if pd.notna(age["mean"]) else "N/D")
    primary2.metric("Herramienta más usada (moda)", format_mode(tools))
    primary3.metric("Mediana del tiempo de uso", f"{format_number(time['median'])} min" if pd.notna(time["median"]) else "N/D")

    iqr = time["q3"] - time["q1"] if pd.notna(time["q3"]) and pd.notna(time["q1"]) else np.nan
    cv = time["cv"]
    cv_label = "Variabilidad alta" if pd.notna(cv) and cv > 30 else "Variabilidad moderada" if pd.notna(cv) and cv > 15 else "Variabilidad baja" if pd.notna(cv) else "No disponible"
    secondary1, secondary2, secondary3 = st.columns(3)
    secondary1.metric("Rango intercuartílico · tiempo", f"{format_number(iqr)} min" if pd.notna(iqr) else "N/D")
    secondary2.metric(
        "Coeficiente de variación · tiempo",
        f"{format_number(cv)} %" if pd.notna(cv) else "N/D",
        cv_label,
        delta_color="off",
    )
    secondary3.metric("Moda · tiempo de uso", time["mode"])

    column_tools, column_purpose = st.columns([1, 1], gap="large")
    with column_tools:
        section_header("01 · Preferencias", "Herramientas de IA", "Porcentaje de respuestas y frecuencia absoluta por herramienta.")
        if tools.empty:
            st.info("No hay datos válidos de herramienta_ia.")
        else:
            counts = tools.value_counts().sort_values(ascending=False)
            names = counts.index.astype(str).tolist()
            values = counts.to_numpy(dtype=int)
            total = int(values.sum())
            positions = ["outside" if count / total < 0.06 else "inside" for count in values]
            labels = [f"{name}<br>{format_number(count / total * 100, 1)} %" for name, count in zip(names, values)]
            pie = px.pie(
                names=names,
                values=values,
                hole=0.42,
                title="Participación por herramienta",
                color_discrete_sequence=["#3563e9", "#13a98b", "#f2a541", "#8b6fe8", "#ef7185", "#173e78"],
            )
            pie.update_traces(
                text=labels,
                texttemplate="%{text}",
                textposition=positions,
                insidetextorientation="horizontal",
                marker={"line": {"color": "#ffffff", "width": 3}},
                hovertemplate="%{label}<br>Frecuencia absoluta: %{value}<br>Porcentaje: %{percent}<extra></extra>",
            )
            pie.update_layout(
                showlegend=False,
                legend_title_text="Herramienta",
                legend={"title": {"text": "Herramienta", "font": {"color": "#17243b", "family": "Inter, DM Sans, Arial, sans-serif"}}},
                annotations=[{"text": f"n = {total}", "x": 0.5, "y": 0.5, "showarrow": False,
                              "font": {"size": 16, "color": "#17243b", "family": "Inter, sans-serif"}}],
            )
            draw_plot(pie, 390)

    with column_purpose:
        section_header("02 · Motivos", "¿Para qué se usa la IA?", "Frecuencia absoluta de selección; una persona puede seleccionar más de una finalidad.")
        purpose_columns = [column for column in data.columns if column.startswith("finalidad_")]
        purpose_counts = []
        for column in purpose_columns:
            normalized = data[column].map(parse_boolean).astype("boolean")
            purpose_counts.append({
                "Finalidad": purpose_label(column),
                "Frecuencia absoluta": int(normalized.eq(True).sum()),
            })
        purposes = pd.DataFrame(purpose_counts).sort_values("Frecuencia absoluta", ascending=True)
        purpose_chart = px.bar(
            purposes,
            x="Frecuencia absoluta",
            y="Finalidad",
            orientation="h",
            title="Respuestas por finalidad",
            text="Frecuencia absoluta",
            labels={"Frecuencia absoluta": "Personas", "Finalidad": ""},
            color_discrete_sequence=["#718096"],
        )
        purpose_chart.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
        purpose_chart.update_xaxes(tickformat="d", showgrid=True)
        purpose_chart.update_layout(yaxis={"categoryorder": "total ascending"})
        draw_plot(purpose_chart, 390)

    column_experience, column_histogram = st.columns([1, 1], gap="large")
    with column_experience:
        section_header("03 · Perfil", "Nivel de experiencia", "Orden ordinal fijo: Básico, Intermedio y Avanzado.")
        experience_counts = (
            data["nivel_experiencia"].value_counts()
            .reindex(EXPERIENCE_ORDER, fill_value=0)
            .rename_axis("Nivel")
            .reset_index(name="Frecuencia absoluta")
        )
        experience_chart = px.bar(
            experience_counts,
            x="Nivel",
            y="Frecuencia absoluta",
            category_orders={"Nivel": EXPERIENCE_ORDER},
            title="Respuestas por nivel",
            text="Frecuencia absoluta",
            labels={"Frecuencia absoluta": "Personas"},
            color="Nivel",
            color_discrete_map=LEVEL_COLORS,
        )
        experience_chart.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0, showlegend=False)
        experience_chart.update_xaxes(categoryorder="array", categoryarray=EXPERIENCE_ORDER)
        experience_chart.update_yaxes(tickformat="d")
        draw_plot(experience_chart, 390)

    with column_histogram:
        section_header("04 · Distribución", "Tiempo de uso", "Histograma por intervalos con polígono de frecuencias cerrado en cero.")
        table, edges, _, frequencies = frequency_distribution(data["tiempo_uso"])
        if table.empty:
            st.info("No hay valores válidos de tiempo_uso para graficar.")
        else:
            centers = table["Marca de clase (xᵢ)"].to_numpy(dtype=float)
            interval_labels = table["Intervalo"].tolist()
            width = float(edges[1] - edges[0]) if len(edges) > 1 else 1.0
            histogram_data = pd.DataFrame({
                "Centro": centers,
                "Frecuencia": frequencies,
                "Intervalo": interval_labels,
            })
            histogram = px.bar(
                histogram_data,
                x="Centro",
                y="Frecuencia",
                title="Frecuencia absoluta por clase",
                labels={"x": "Tiempo de uso (minutos)", "y": "Frecuencia absoluta"},
                custom_data=["Intervalo"],
                color_discrete_sequence=["#91a9f8"],
            )
            histogram.update_traces(
                width=width,
                marker_line_width=0,
                hovertemplate="Intervalo: %{customdata[0]}<br>fᵢ: %{y}<extra></extra>",
                name="Histograma",
            )
            closed_x = np.concatenate(([centers[0] - width], centers, [centers[-1] + width]))
            closed_y = np.concatenate(([0], np.asarray(frequencies, dtype=int), [0]))
            histogram.add_scatter(
                x=closed_x,
                y=closed_y,
                mode="lines+markers",
                name="Polígono de frecuencias",
                line={"width": 3, "color": "#13a98b"},
                marker={"size": 6, "color": "#13a98b", "line": {"color": "#ffffff", "width": 1.5}},
                hovertemplate="Marca de clase: %{x:.2f}<br>fᵢ: %{y}<extra></extra>",
            )
            boundary_text = [format_boundary(value) for value in edges]
            histogram.update_xaxes(
                title_text="Tiempo de uso (min/día)",
                tickmode="array",
                tickvals=edges.tolist(),
                ticktext=boundary_text,
                range=[float(edges[0]) - width, float(edges[-1]) + width],
            )
            histogram.update_yaxes(title_text="Frecuencia absoluta (fᵢ)", tickformat="d", rangemode="tozero")
            histogram.update_layout(
                showlegend=True,
                legend={
                    "orientation": "h", "yanchor": "top", "y": -0.24,
                    "xanchor": "center", "x": 0.5,
                    "font": {"color": "#263653", "family": "Inter, DM Sans, Arial, sans-serif"},
                    "title_font": {"color": "#17243b", "family": "Inter, DM Sans, Arial, sans-serif"},
                },
                margin={"l": 18, "r": 20, "t": 58, "b": 72},
            )
            draw_plot(histogram, 390)

    section_header("05 · Asociación", "Frecuencia semanal y tiempo de uso", "Puntos coincidentes se agrupan; el tamaño indica cuántas personas comparten cada coordenada y nivel.")
    scatter_data = data[["frecuencia_semanal", "tiempo_uso", "nivel_experiencia"]].dropna(
        subset=["frecuencia_semanal", "tiempo_uso", "nivel_experiencia"]
    )
    if scatter_data.empty:
        st.info("No hay pares completos de frecuencia_semanal y tiempo_uso para mostrar.")
    else:
        grouped = (
            scatter_data.groupby(
                ["frecuencia_semanal", "tiempo_uso", "nivel_experiencia"],
                observed=True,
                dropna=False,
            )
            .size()
            .reset_index(name="n_personas")
        )
        grouped = grouped.sort_values("n_personas", ascending=False, kind="mergesort")
        grouped["nivel_experiencia"] = pd.Categorical(
            grouped["nivel_experiencia"], categories=EXPERIENCE_ORDER, ordered=True
        )
        scatter = px.scatter(
            grouped,
            x="frecuencia_semanal",
            y="tiempo_uso",
            color="nivel_experiencia",
            size="n_personas",
            size_max=32,
            category_orders={"nivel_experiencia": EXPERIENCE_ORDER},
            color_discrete_map=LEVEL_COLORS,
            hover_data={"n_personas": True, "frecuencia_semanal": True, "tiempo_uso": True},
            title="Frecuencia semanal frente a duración de uso",
            labels={
                "frecuencia_semanal": "Frecuencia semanal (días por semana)",
                "tiempo_uso": "Tiempo de uso (minutos)",
                "nivel_experiencia": "Nivel de experiencia",
                "n_personas": "Número de personas",
            },
        )
        scatter.update_traces(marker={"opacity": 0.86, "line": {"color": "#ffffff", "width": 1.5}})
        scatter.update_xaxes(tickmode="array", tickvals=sorted(scatter_data["frecuencia_semanal"].unique()),
                             ticktext=[format_boundary(value) for value in sorted(scatter_data["frecuencia_semanal"].unique())])
        y_ticks = list(range(0, 361, 60))
        scatter.update_yaxes(
            tickmode="array", tickvals=y_ticks,
            ticktext=[format_boundary(value) for value in y_ticks],
            range=[0, 400],
        )
        scatter.update_layout(
            legend={
                "title": {"text": "Nivel de experiencia", "font":
                          {"color": "#17243b", "family": "Inter, DM Sans, Arial, sans-serif"}},
                "font": {"color": "#263653", "family": "Inter, DM Sans, Arial, sans-serif"},
            }
        )
        draw_plot(scatter, 430)
        pearson = scatter_data[["frecuencia_semanal", "tiempo_uso"]].corr(method="pearson").iloc[0, 1]
        st.caption(
            f"Correlación de Pearson: r = {format_number(pearson)} · "
            f"n = {len(scatter_data)} pares completos. Correlación describe asociación, no causalidad."
        )


def main() -> None:
    try:
        raw_data = load_dataset()
    except FileNotFoundError as exc:
        st.error(f"No se puede iniciar el dashboard: {exc}")
        st.stop()
    except ValueError as exc:
        st.error(f"No se puede procesar el CSV: {exc}")
        st.stop()
    except Exception as exc:
        st.error(f"No se pudo leer datos_limpios_ia.csv: {exc}")
        st.stop()

    raw_data["edad"] = pd.to_numeric(raw_data["edad"], errors="coerce")
    age_values = raw_data["edad"].dropna()
    if age_values.empty:
        st.error("La columna 'edad' no contiene valores numéricos válidos para crear el filtro de edad.")
        st.stop()

    with st.sidebar:
        st.markdown(
            "<div class='sidebar-brand'><div class='brand-mark'>Panel de investigación</div>"
            "<div class='brand-copy'>Dashboard estadístico interactivo de una muestra empírica.</div></div>",
            unsafe_allow_html=True,
        )
        if st.button("Restablecer filtros", use_container_width=True):
            for key in (
                "experience_filter",
                "age_range_filter",
                "tool_filter",
                "exclude_outliers_filter",
            ):
                st.session_state.pop(key, None)
            st.rerun()

        experience_values = [
            value for value in EXPERIENCE_ORDER
            if value in raw_data["nivel_experiencia"].dropna().astype(str).unique()
        ]
        extras = sorted(
            set(raw_data["nivel_experiencia"].dropna().astype(str)) - set(EXPERIENCE_ORDER)
        )
        experience_values.extend(extras)
        selected_experience = st.selectbox(
            "Nivel de experiencia",
            ["Todos"] + experience_values,
            index=0,
            key="experience_filter",
        )
        age_min = float(age_values.min())
        age_max = float(age_values.max())
        selected_age_range = st.slider(
            "Rango de edad",
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max),
            step=1.0,
            key="age_range_filter",
        )
        tool_options = sorted(raw_data["herramienta_ia"].dropna().astype(str).unique().tolist())
        selected_tools = st.multiselect(
            "Herramientas de IA",
            options=tool_options,
            default=tool_options,
            key="tool_filter",
        )
        exclude_outliers = st.toggle(
            "Excluir valores atípicos de tiempo de uso (regla de Tukey: fuera de [Q1 − 1,5·RIC, Q3 + 1,5·RIC])",
            value=False,
            key="exclude_outliers_filter",
        )

    if selected_experience == "Todos":
        filtered = raw_data.copy()
    else:
        filtered = raw_data.loc[raw_data["nivel_experiencia"] == selected_experience].copy()

    filtered = filtered.loc[
        filtered["edad"].between(selected_age_range[0], selected_age_range[1], inclusive="both")
        & filtered["herramienta_ia"].astype("string").isin(selected_tools)
    ].copy()
    data_before_tukey = filtered.copy()
    outlier_status = None

    if exclude_outliers and not filtered.empty:
        valid_time = pd.to_numeric(filtered["tiempo_uso"], errors="coerce").dropna()
        if not valid_time.empty:
            q1 = valid_time.quantile(0.25, interpolation="linear")
            q3 = valid_time.quantile(0.75, interpolation="linear")
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            time_numeric = pd.to_numeric(filtered["tiempo_uso"], errors="coerce")
            keep_rows = time_numeric.isna() | time_numeric.between(
                lower_bound, upper_bound, inclusive="both"
            )
            filtered = filtered.loc[keep_rows].copy()
        outlier_status = f"Sin atípicos (n = {len(filtered)} de {len(data_before_tukey)})"

    data = filtered
    st.sidebar.caption(f"Registros en la vista: n = {len(data)} / {len(raw_data)}")

    if data.empty:
        st.warning("Los filtros seleccionados no dejan observaciones (n = 0).")
        st.stop()

    if len(data) < 10:
        st.warning(f"Muestra muy pequeña (n = {len(data)}): interpretar con cautela")

    filter_description = (
        outlier_status
        if outlier_status is not None
        else f"Nivel: {selected_experience if selected_experience != 'Todos' else 'Todos los niveles'}"
    )
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-kicker">Panel de análisis · investigación empírica</div>
          <h1 class="hero-title">Inteligencia artificial<br>en perspectiva</h1>
          <p class="hero-copy">Explora patrones de uso, experiencia y finalidades a partir de los registros de la investigación. Las cifras describen esta muestra; no representan parámetros de una población.</p>
          <div class="hero-chips"><span class="hero-chip">MUESTRA · n = {len(data)} de {len(raw_data)}</span><span class="hero-chip">{filter_description}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if outlier_status is not None:
        st.caption("Análisis de sensibilidad, no limpieza de datos.")

    tab_numeric, tab_visual = st.tabs(
        ["Análisis estadístico numérico", "Visualizaciones interactivas"]
    )
    with tab_numeric:
        render_numeric_tab(data)
    with tab_visual:
        render_visual_tab(data)

    st.divider()
    st.caption(
        f"Vista actual: n = {len(data)} observaciones de una muestra empírica. "
        "Los faltantes se excluyen variable por variable; no se imputan en este dashboard."
    )


if __name__ == "__main__":
    main()
