import streamlit as st
import time
import random
import os
import csv
import streamlit_javascript as st_js  # Requiere instalar streamlit-javascript

st.set_page_config(page_title="IAT: Humanos vs IA y Confianza", layout="centered")

# Función auxiliar para reiniciar (rerun) la app
def rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
        get_script_run_ctx().session.request_rerun()

# --- Función para guardar un resultado en results.csv ---
def save_result_to_csv(result):
    """
    Guarda la información de un trial en el archivo results.csv.
    Si el archivo no existe, se crea con encabezados.
    'result' debe ser un dict con keys: 
      ['word', 'tipo', 'respuesta', 'correcto', 'tiempo_ms', 'error'].
    """
    file_exists = os.path.isfile("results.csv")
    correcto_val = 1 if result["correcto"] else 0

    with open("results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["word", "tipo", "respuesta", "correcto", "tiempo_ms", "error"])
        writer.writerow([
            result["word"],
            result["tipo"],
            result["respuesta"],
            correcto_val,
            result["tiempo_ms"],
            result["error"]
        ])

# --- 1) Listas de palabras ---
words_human = [
    "Persona", "Individuo", "Humano", "Gente", "Nosotros",
    "Él", "Ella", "Ellos", "Ciudadano", "Vecino"
]
words_ai = [
    "Robot", "Algoritmo", "Programa", "IA", "Inteligencia Artificial",
    "Máquina", "Computadora", "Bot", "Sistema Inteligente", "Red Neuronal"
]
words_trust = [
    "Confiable", "Seguro", "Honesto", "Sincero", "Auténtico",
    "Fiable", "Veraz", "Responsable", "Leal", "Ético"
]
words_untrust = [
    "No Confiable", "Sospechoso", "Falso", "Engañoso", "Deshonesto",
    "Inseguro", "Irresponsable", "Infiel", "Dudoso", "Poco Ético"
]

# --- 2) Generar estímulos para cada bloque ---
def generate_trials(block):
    trials = []
    if block == 1:
        for word in words_human:
            trials.append({"word": word, "type": "human"})
    elif block == 2:
        for word in words_ai:
            trials.append({"word": word, "type": "ai"})
    elif block in [3, 4]:
        for word in words_human:
            trials.append({"word": word, "type": "human"})
        for word in words_ai:
            trials.append({"word": word, "type": "ai"})
        for word in words_trust:
            trials.append({"word": word, "type": "trust"})
        for word in words_untrust:
            trials.append({"word": word, "type": "untrust"})
    random.shuffle(trials)
    return trials

# --- 3) Determinar la tecla correcta según bloque y tipo de palabra ---
def get_correct_response(trial, block):
    t = trial["type"]
    if block == 1:
        return "E"
    elif block == 2:
        return "I"
    elif block == 3:
        if t in ["human", "trust"]:
            return "E"
        else:
            return "I"
    elif block == 4:
        if t == "human":
            return "I"
        elif t == "ai":
            return "E"
        elif t == "trust":
            return "E"
        else:
            return "I"

# --- 4) Etiquetas superiores para cada bloque ---
def get_block_labels(block):
    if block == 1:
        return ("Seres Humanos", "Inteligencia Artificial")
    elif block == 2:
        return ("Seres Humanos", "Inteligencia Artificial")
    elif block == 3:
        return ("Seres Humanos o Confiable", "IA o No Confiable")
    elif block == 4:
        return ("Seres Humanos o No Confiable", "IA o Confiable")

# --- 5) Colorear las palabras según su tipo ---
def get_word_color(word_type):
    if word_type in ["human", "ai"]:
        return "#1F77B4"  # Azul para categorías factuales
    else:
        return "#2CA02C"  # Verde para atributos

# --- 6) Inicialización de variables en session_state ---
if "block" not in st.session_state:
    st.session_state.block = 1  
if "trials" not in st.session_state:
    st.session_state.trials = generate_trials(st.session_state.block)
if "trial_index" not in st.session_state:
    st.session_state.trial_index = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "results" not in st.session_state:
    st.session_state.results = []

# --- 7) Interfaz de usuario ---
st.title("Test de Asociación Implícita (IAT)")
st.markdown("### Estereotipos: Seres Humanos vs. Inteligencia Artificial y Confianza")

# 7.1) Etiquetas superiores: E (izquierda, centrado) e I (derecha, en la esquina)
left_label, right_label = get_block_labels(st.session_state.block)
top_left_col, top_right_col = st.columns(2)
with top_left_col:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <strong>Presiona 'E' para</strong><br>
            <span style="font-size:18px;">{left_label}</span>
        </div>
        """, unsafe_allow_html=True
    )
with top_right_col:
    st.markdown(
        f"""
        <div style="text-align:right;">
            <strong>Presiona 'I' para</strong><br>
            <span style="font-size:18px;">{right_label}</span>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")

# 7.2) Mostrar la palabra en la parte inferior
if st.session_state.trial_index < len(st.session_state.trials):
    trial = st.session_state.trials[st.session_state.trial_index]
    if st.session_state.start_time is None:
        st.session_state.start_time = time.perf_counter()
    color = get_word_color(trial["type"])
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:40px;
            color:{color};
            min-height:200px;
        ">
            {trial['word']}
        </div>
        """, unsafe_allow_html=True
    )
    
    # Instrucción para que el usuario use el teclado
    st.markdown("<div style='text-align:center; font-size:20px; color:#555;'>Presiona 'E' o 'I' en el teclado para responder.</div>", unsafe_allow_html=True)
    
    # --- 7.3) Capturar la tecla pulsada mediante JavaScript ---
    # El siguiente script espera la pulsación de 'E' o 'I' y retorna la tecla en mayúscula.
    js_code = """
    <script>
    async function getKey() {
      return await new Promise(resolve => {
        document.addEventListener('keydown', function handler(e) {
          let key = e.key.toUpperCase();
          if(key === 'E' || key === 'I'){
            document.removeEventListener('keydown', handler);
            resolve(key);
          }
        });
      });
    }
    getKey().then(key => {
      const streamlitEvent = new CustomEvent("STREAMLIT_KEY", {detail: key});
      window.parent.document.dispatchEvent(streamlitEvent);
    });
    </script>
    """
    # Se inyecta el JS; el componente retornará el valor enviado a través del CustomEvent.
    key_pressed = st_js.st_javascript(js_code, key="key_js")
    
    if key_pressed:
        rt = (time.perf_counter() - st.session_state.start_time) * 1000
        rt = round(rt, 3)
        correct_key = get_correct_response(trial, st.session_state.block)
        correct = (correct_key == key_pressed)
        error = 0 if correct else 1
        result_dict = {
            "word": trial["word"],
            "tipo": trial["type"],
            "respuesta": key_pressed,
            "correcto": correct,
            "tiempo_ms": rt,
            "error": error
        }
        st.session_state.results.append(result_dict)
        save_result_to_csv(result_dict)
        st.session_state.trial_index += 1
        st.session_state.start_time = None
        rerun()
        
    # Se muestra un aviso en caso de error (mensaje fijo, similar a la X roja)
    st.markdown(
        "<div style='text-align:center; color:gray; margin-top:20px;'>"
        "Si te equivocas, aparecerá una X roja (o un aviso). Presiona la otra tecla para continuar."
        "</div>", unsafe_allow_html=True
    )
else:
    st.markdown("### Fin del bloque")
    total_errores = sum(r["error"] for r in st.session_state.results)
    tiempo_promedio = (sum(r["tiempo_ms"] for r in st.session_state.results) / len(st.session_state.results)) if st.session_state.results else 0
    st.write(f"**Total de errores:** {total_errores}")
    st.write(f"**Tiempo de reacción promedio:** {round(tiempo_promedio, 3)} ms")
    
    if st.session_state.block < 4:
        if st.button("Siguiente bloque"):
            st.session_state.block += 1
            st.session_state.trials = generate_trials(st.session_state.block)
            st.session_state.trial_index = 0
            st.session_state.results = []
            st.session_state.start_time = None
            rerun()
    else:
        st.success("Test completado. ¡Gracias por participar!")

