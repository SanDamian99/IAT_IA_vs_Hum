import streamlit as st
import time
import random

st.set_page_config(page_title="IAT: Humanos vs IA y Confianza", layout="centered")

# Listas de palabras
# Categoría A: Seres Humanos
words_human = ["Persona", "Individuo", "Humano", "Gente", "Nosotros", "Él", "Ella", "Ellos", "Ciudadano", "Vecino"]

# Categoría B: Inteligencia Artificial
words_ai = ["Robot", "Algoritmo", "Programa", "IA", "Inteligencia Artificial", "Máquina", "Computadora", "Bot", "Sistema Inteligente", "Red Neuronal"]

# Atributo 1: Confiable / Digno de Confianza
words_trust = ["Confiable", "Seguro", "Honesto", "Sincero", "Auténtico", "Fiable", "Veraz", "Responsable", "Leal", "Ético"]

# Atributo 2: No Confiable / No Digno de Confianza
words_untrust = ["No Confiable", "Sospechoso", "Falso", "Engañoso", "Deshonesto", "Inseguro", "Irresponsable", "Infiel", "Dudoso", "Poco Ético"]

# Función para generar los trials según el bloque
def generate_trials(block):
    trials = []
    if block == 1:
        # Bloque de Práctica: Seres Humanos
        for word in words_human:
            trials.append({"word": word, "type": "human"})
    elif block == 2:
        # Bloque de Práctica: Inteligencia Artificial
        for word in words_ai:
            trials.append({"word": word, "type": "ai"})
    elif block in [3, 4]:
        # Bloques combinados (3: Congruente, 4: Inversión)
        # Se incluyen palabras de ambas categorías y de ambos atributos.
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

# Función que define la respuesta correcta según el bloque y el tipo de palabra
def get_correct_response(trial, block):
    t = trial["type"]
    if block == 1:
        # Práctica: Solo se muestran palabras de "Seres Humanos" → tecla E.
        return "E"
    elif block == 2:
        # Práctica: Solo se muestran palabras de "Inteligencia Artificial" → tecla I.
        return "I"
    elif block == 3:
        # Bloque Combinado Congruente:
        # "Seres Humanos" y "Confiable" se asignan a E; 
        # "Inteligencia Artificial" y "No Confiable" se asignan a I.
        if t in ["human", "trust"]:
            return "E"
        elif t in ["ai", "untrust"]:
            return "I"
    elif block == 4:
        # Bloque de Inversión:
        # Las categorías se invierten: "Seres Humanos" → I y "Inteligencia Artificial" → E;
        # Los atributos se mantienen: "Confiable" → E y "No Confiable" → I.
        if t == "human":
            return "I"
        elif t == "ai":
            return "E"
        elif t == "trust":
            return "E"
        elif t == "untrust":
            return "I"

# Inicialización en session_state
if "block" not in st.session_state:
    st.session_state.block = 1  # 1: Práctica Humanos, 2: Práctica IA, 3: Combinado Congruente, 4: Inversión
if "trials" not in st.session_state:
    st.session_state.trials = generate_trials(st.session_state.block)
if "trial_index" not in st.session_state:
    st.session_state.trial_index = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "results" not in st.session_state:
    st.session_state.results = []

# Función para mostrar las instrucciones según el bloque
def show_instructions(block):
    if block == 1:
        st.info(
            "Bloque de Práctica: **Seres Humanos**\n\n"
            "Instrucciones: Presiona **E** cuando veas palabras que representen a Seres Humanos.\n\n"
            "Ejemplos: Persona, Individuo, Humano, etc."
        )
    elif block == 2:
        st.info(
            "Bloque de Práctica: **Inteligencia Artificial**\n\n"
            "Instrucciones: Presiona **I** cuando veas palabras que representen a Inteligencia Artificial.\n\n"
            "Ejemplos: Robot, Algoritmo, Programa, etc."
        )
    elif block == 3:
        st.info(
            "Bloque Combinado: **Seres Humanos o Confiable** / **Inteligencia Artificial o No Confiable**\n\n"
            "Instrucciones: Presiona **E** si la palabra representa a Seres Humanos **o** significa algo Confiable/Digno de Confianza.\n"
            "Presiona **I** si la palabra representa a Inteligencia Artificial **o** significa algo No Confiable/No Digno de Confianza."
        )
    elif block == 4:
        st.info(
            "Bloque de Inversión:\n\n"
            "Ahora, la asignación de categorías se invierte:\n"
            "- **Seres Humanos** se clasifica con la tecla **I**\n"
            "- **Inteligencia Artificial** se clasifica con la tecla **E**\n\n"
            "Las asignaciones para los atributos se mantienen:\n"
            "- **Confiable** → **E**\n"
            "- **No Confiable** → **I**\n\n"
            "Instrucciones: Presiona la tecla correspondiente según el origen de la palabra."
        )

st.title("Test de Asociación Implícita (IAT)")
st.markdown("### Estereotipos: Seres Humanos vs. Inteligencia Artificial y la Confianza")

# Mostrar instrucciones según el bloque actual
show_instructions(st.session_state.block)

# Si aún hay trials por realizar
if st.session_state.trial_index < len(st.session_state.trials):
    trial = st.session_state.trials[st.session_state.trial_index]
    st.markdown(f"#### Palabra: **{trial['word']}**")
    
    # Iniciar el cronómetro cuando se muestra la palabra
    if st.session_state.start_time is None:
        st.session_state.start_time = time.perf_counter()
    
    # Mostrar dos botones para responder: "E" y "I"
    col1, col2 = st.columns(2)
    
    if col1.button("E", key="btn_E"):
        rt = (time.perf_counter() - st.session_state.start_time) * 1000  # Tiempo en ms
        rt = round(rt, 3)  # Precisión de 0.001 ms
        correct_key = get_correct_response(trial, st.session_state.block)
        correct = (correct_key == "E")
        error = 0 if correct else 1
        st.session_state.results.append({
            "word": trial["word"],
            "tipo": trial["type"],
            "respuesta": "E",
            "correcto": correct,
            "tiempo_ms": rt,
            "error": error
        })
        st.session_state.trial_index += 1
        st.session_state.start_time = None
        st.experimental_rerun()
        
    if col2.button("I", key="btn_I"):
        rt = (time.perf_counter() - st.session_state.start_time) * 1000
        rt = round(rt, 3)
        correct_key = get_correct_response(trial, st.session_state.block)
        correct = (correct_key == "I")
        error = 0 if correct else 1
        st.session_state.results.append({
            "word": trial["word"],
            "tipo": trial["type"],
            "respuesta": "I",
            "correcto": correct,
            "tiempo_ms": rt,
            "error": error
        })
        st.session_state.trial_index += 1
        st.session_state.start_time = None
        st.experimental_rerun()
else:
    # Al finalizar el bloque, se muestran los resultados
    st.markdown("### Fin del bloque")
    total_errores = sum(r["error"] for r in st.session_state.results)
    tiempo_promedio = (sum(r["tiempo_ms"] for r in st.session_state.results) /
                       len(st.session_state.results)) if st.session_state.results else 0
    st.write(f"**Total de errores:** {total_errores}")
    st.write(f"**Tiempo de reacción promedio:** {round(tiempo_promedio, 3)} ms")
    
    # Botón para avanzar al siguiente bloque (si lo hay)
    if st.session_state.block < 4:
        if st.button("Siguiente bloque"):
            st.session_state.block += 1
            st.session_state.trials = generate_trials(st.session_state.block)
            st.session_state.trial_index = 0
            st.session_state.results = []
            st.session_state.start_time = None
            st.experimental_rerun()
    else:
        st.success("Test completado. Gracias por participar.")

