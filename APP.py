import streamlit as st
import time
import random
import os
import csv

st.set_page_config(page_title="IAT: Humanos vs IA y Confianza", layout="centered")

# --- Función para guardar un resultado en results.csv ---
def save_result_to_csv(result):
    """
    Guarda la información de un trial en el archivo results.csv.
    Si el archivo no existe, se crea con encabezados.
    'result' debe ser un dict con keys: 
      ['word', 'tipo', 'respuesta', 'correcto', 'tiempo_ms', 'error'].
    """
    file_exists = os.path.isfile("results.csv")
    
    # Aseguramos que 'correcto' se guarde como 0/1 en lugar de True/False
    correcto_val = 1 if result["correcto"] else 0

    with open("results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Si el archivo no existe, escribir la cabecera
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


# --- 1) Definir las listas de palabras ---
# Categoría A: Seres Humanos
words_human = [
    "Persona", "Individuo", "Humano", "Gente", "Nosotros",
    "Él", "Ella", "Ellos", "Ciudadano", "Vecino"
]

# Categoría B: Inteligencia Artificial
words_ai = [
    "Robot", "Algoritmo", "Programa", "IA", "Inteligencia Artificial",
    "Máquina", "Computadora", "Bot", "Sistema Inteligente", "Red Neuronal"
]

# Atributo 1: Confiable / Digno de Confianza
words_trust = [
    "Confiable", "Seguro", "Honesto", "Sincero", "Auténtico",
    "Fiable", "Veraz", "Responsable", "Leal", "Ético"
]

# Atributo 2: No Confiable / No Digno de Confianza
words_untrust = [
    "No Confiable", "Sospechoso", "Falso", "Engañoso", "Deshonesto",
    "Inseguro", "Irresponsable", "Infiel", "Dudoso", "Poco Ético"
]


# --- 2) Generar los "trials" (estímulos) para cada bloque ---
def generate_trials(block):
    """
    Retorna una lista de diccionarios con las palabras
    que se mostrarán en cada bloque.
    """
    trials = []
    if block == 1:
        # Bloque 1: Práctica - Seres Humanos (tecla E)
        for word in words_human:
            trials.append({"word": word, "type": "human"})
    elif block == 2:
        # Bloque 2: Práctica - IA (tecla I)
        for word in words_ai:
            trials.append({"word": word, "type": "ai"})
    elif block in [3, 4]:
        # Bloques combinados
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


# --- 3) Función para determinar la tecla correcta según bloque y tipo de palabra ---
def get_correct_response(trial, block):
    t = trial["type"]
    if block == 1:
        # Práctica: solo "Seres Humanos" -> E
        return "E"
    elif block == 2:
        # Práctica: solo "IA" -> I
        return "I"
    elif block == 3:
        # Bloque Combinado (congruente):
        # Humanos/Confiable -> E, IA/No Confiable -> I
        if t in ["human", "trust"]:
            return "E"
        else:  # "ai", "untrust"
            return "I"
    elif block == 4:
        # Bloque Invertido:
        # Humanos -> I, IA -> E
        # Confiable -> E, No Confiable -> I
        if t == "human":
            return "I"
        elif t == "ai":
            return "E"
        elif t == "trust":
            return "E"
        else:  # "untrust"
            return "I"


# --- 4) Etiquetas que se mostrarán en la parte superior para cada bloque ---
def get_block_labels(block):
    """
    Retorna (label_left, label_right) para mostrarlos
    arriba de las teclas E e I, respectivamente.
    """
    if block == 1:
        # Práctica: Humanos -> E, IA -> I
        return ("Seres Humanos", "Inteligencia Artificial")
    elif block == 2:
        # Práctica: Humanos -> E, IA -> I
        return ("Seres Humanos", "Inteligencia Artificial")
    elif block == 3:
        # Combinado Congruente
        return ("Seres Humanos o Confiable", "IA o No Confiable")
    elif block == 4:
        # Inversión
        return ("Seres Humanos o No Confiable", "IA o Confiable")


# --- 5) Función para colorear palabras según tipo ---
def get_word_color(word_type):
    """
    Asigna un color a la palabra dependiendo de si es
    categoría factual (human/ai) o atributo (trust/untrust).
    """
    if word_type in ["human", "ai"]:
        return "#1F77B4"  # Azul
    else:
        return "#2CA02C"  # Verde


# --- 6) Inicialización de variables de estado ---
if "block" not in st.session_state:
    st.session_state.block = 1  # Bloque inicial
if "trials" not in st.session_state:
    st.session_state.trials = generate_trials(st.session_state.block)
if "trial_index" not in st.session_state:
    st.session_state.trial_index = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "results" not in st.session_state:
    st.session_state.results = []


# --- 7) Mostrar la interfaz de usuario ---
st.title("Test de Asociación Implícita (IAT)")
st.markdown("### Estereotipos: Seres Humanos vs. Inteligencia Artificial y Confianza")

# 7.1) Etiquetas en la parte superior: (E) a la izquierda, (I) a la derecha
left_label, right_label = get_block_labels(st.session_state.block)

# Usamos columnas para alinear a la izquierda y derecha
top_left_col, top_right_col = st.columns(2)

with top_left_col:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <strong>Presiona 'E' para</strong><br>
            <span style="font-size:18px;">{left_label}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with top_right_col:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <strong>Presiona 'I' para</strong><br>
            <span style="font-size:18px;">{right_label}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# 7.2) Mostrar la palabra en la parte inferior (aproximada)
if st.session_state.trial_index < len(st.session_state.trials):
    trial = st.session_state.trials[st.session_state.trial_index]
    # Iniciamos cronómetro al mostrar la palabra
    if st.session_state.start_time is None:
        st.session_state.start_time = time.perf_counter()
    
    # Determinamos color de la palabra
    color = get_word_color(trial["type"])

    # Espacio para empujar la palabra hacia la parte baja
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    # Palabra en el centro
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
        """,
        unsafe_allow_html=True
    )
    
    # 7.3) Botones E / I
    col_e, col_i = st.columns(2)
    
    if col_e.button("E", key="btn_E"):
        rt = (time.perf_counter() - st.session_state.start_time) * 1000
        rt = round(rt, 3)
        correct_key = get_correct_response(trial, st.session_state.block)
        correct = (correct_key == "E")
        error = 0 if correct else 1
        
        # Creamos el registro de resultado
        result_dict = {
            "word": trial["word"],
            "tipo": trial["type"],
            "respuesta": "E",
            "correcto": correct,
            "tiempo_ms": rt,
            "error": error
        }
        
        # Guardamos en session_state y en el CSV
        st.session_state.results.append(result_dict)
        save_result_to_csv(result_dict)  # <-- Guardar en el CSV
        
        st.session_state.trial_index += 1
        st.session_state.start_time = None
        st.experimental_rerun()
    
    if col_i.button("I", key="btn_I"):
        rt = (time.perf_counter() - st.session_state.start_time) * 1000
        rt = round(rt, 3)
        correct_key = get_correct_response(trial, st.session_state.block)
        correct = (correct_key == "I")
        error = 0 if correct else 1
        
        result_dict = {
            "word": trial["word"],
            "tipo": trial["type"],
            "respuesta": "I",
            "correcto": correct,
            "tiempo_ms": rt,
            "error": error
        }
        
        st.session_state.results.append(result_dict)
        save_result_to_csv(result_dict)  # <-- Guardar en el CSV
        
        st.session_state.trial_index += 1
        st.session_state.start_time = None
        st.experimental_rerun()

    # Mensaje de retroalimentación sobre errores
    st.markdown(
        "<div style='text-align:center; color:gray; margin-top:20px;'>"
        "Si te equivocas, aparecerá una X roja (o un aviso). Presiona la otra tecla para continuar."
        "</div>",
        unsafe_allow_html=True
    )

else:
    # 7.4) Fin del bloque actual
    st.markdown("### Fin del bloque")
    total_errores = sum(r["error"] for r in st.session_state.results)
    tiempo_promedio = (
        sum(r["tiempo_ms"] for r in st.session_state.results) / len(st.session_state.results)
        if st.session_state.results else 0
    )
    st.write(f"**Total de errores:** {total_errores}")
    st.write(f"**Tiempo de reacción promedio:** {round(tiempo_promedio, 3)} ms")
    
    # Avanzar al siguiente bloque si no hemos llegado al 4
    if st.session_state.block < 4:
        if st.button("Siguiente bloque"):
            st.session_state.block += 1
            st.session_state.trials = generate_trials(st.session_state.block)
            st.session_state.trial_index = 0
            st.session_state.results = []
            st.session_state.start_time = None
            st.experimental_rerun()
    else:
        st.success("Test completado. ¡Gracias por participar!")
