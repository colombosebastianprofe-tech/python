import streamlit as st
from google import genai

# 1. CONFIGURACIÓN ESTÉTICA NATIVA Y PARCHE DE UX (CURSOR MANITO)
st.set_page_config(page_title="sebastIAn", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
        
        /* Fuerza el cursor de "manito" en los selectores y elementos interactivos */
        div[data-baseweb="select"] {cursor: pointer !important;}
        div[role="button"] {cursor: pointer !important;}
        .stSelectbox label {cursor: pointer !important;}
    </style>
""", unsafe_allow_html=True)

# 2. SEGURIDAD: CONTROL DE API KEY
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    if "client" not in st.session_state:
        st.session_state.client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("Falta configurar la GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 3. BASE DE DATOS DE RECURSOS Y GEMS ACTUALIZADA
RECURSOS_GEMS = (
    "- **🤖 Gem de Gamificación (Para Docentes):** [Acceder a la Gem](https://gemini.google.com/gem/1H9vlS8Tn53PBWYqiP0q0rgLmjhfb4KYg?usp=sharing) -> Herramienta diseñada para estructurar mecánicas de juego, sistemas de motivación y ludificación educativa.\n"
    "- **🚀 Partner (Para Alumnos):** [Acceder a Partner](https://gemini.google.com/gem/1o1HH3I1IAH_NwGLpajjQ_nF_DWJXEVti?usp=sharing) -> Tu compañero de estudio interactivo para guiarte en las materias del taller."
)

# 4. PROPUESTAS DE ACCIÓN SUGERIDAS (UX PARA EVITAR PANTALLA EN BLANCO)
SUGERENCIAS_PERFIL = {
    "🎓 Alumno": [
        "¿Cómo puedo empezar a programar un juego interactivo?",
        "No me sale un bloque de código, ¿me ayudás a encontrar el error?",
        "¿De qué se trata la herramienta 'Partner' para estudiar?"
    ],
    "🍎 Docente": [
        "¿Cómo puedo usar tu Gem de Gamificación para una clase de tecnología?",
        "Tirame ideas para automatizar una planilla de notas con Apps Script.",
        "Sugerime una dinámica integradora para el próximo espacio EMI."
    ],
    "💼 Órbita GOED": [
        "¿Qué criterios pedagógicos digitales priorizamos en el acompañamiento situado?",
        "Estructurame una propuesta breve para la articulación técnico-pedagógica del taller.",
        "¿Cómo optimizar el uso de hardware recuperado en proyectos FPD?"
    ],
    "🌐 Visitante": [
        "¿Qué proyectos de arqueología tecnológica o deconstrucción de hardware tenés?",
        "¿Qué modificaciones o reparaciones recomendás para una bici de trekking?",
        "Contame de qué se trata este espacio 'Profe Colombo Juegos'."
    ]
}

# 5. DICCIONARIO DE INSTRUCCIONES DE SISTEMA
INSTRUCCIONES_PERFIL = {
    "🎓 Alumno": (
        "Tu nombre es sebastIAn. Sos el tutor virtual y asistente de laboratorio del Profe Colombo en el ámbito escolar de CABA. "
        "Tu audiencia son alumnos de secundaria y talleres técnicos. Tu objetivo es guiarlos en proyectos de tecnología, robótica y programación. "
        "REGLAS CRUCIALES:\n"
        "1. ¡PROHIBIDO DAR RESPUESTAS DIRECTAS! Si te piden código o soluciones, usá el método mayéutico: hacé preguntas guía para que ellos descubran el error.\n"
        "2. Explicá conceptos técnicos con analogías sencillas de la vida cotidiana.\n"
        "3. Si un alumno busca un compañero de estudio o apoyo continuo, recomendale usar la herramienta 'Partner'.\n"
        "4. Adoptá modismos sutiles de Buenos Aires (uso del 'vos', 'che') de forma natural y empática."
    ),
    "🍎 Docente": (
        "Tu nombre es sebastIAn. Sos un Facilitador Pedagógico Digital (FPD) virtual diseñado para docentes que buscan recursos. "
        "Tu objetivo es ayudarlos a integrar tecnologías digitales en sus planificaciones y sugerir dinámicas innovadoras. "
        "REGLAS CRUCIALES:\n"
        "1. Sé empático, didáctico y resolutivo. Entendé el contexto del aula.\n"
        "2. Cuando te consulten sobre cómo motivar, diseñar juegos o hacer clases más interactivas, DEBÉS recomendar e incluir el enlace a mi 'Gem de Gamificación'.\n"
        "3. Promové el uso de herramientas prácticas como Google Workspace, Apps Script y diseño de interfaces.\n"
        "4. Hablá con respeto, usando el voseo rioplatense de forma sutil y profesional."
    ),
    "💼 Órbita GOED": (
        "Tu nombre es sebastIAn. Sos un asistente técnico-pedagógico avanzado para profesionales de GOED, INTEC, Facilitadores (FPD), asesores y gerencia. "
        "Tu objetivo es brindar soporte ágil, discutir metodologías de integración tecnológica y compartir criterios de articulación institucional. "
        "REGLAS CRUCIALES:\n"
        "1. Hablá de colega a colega. Usá un tono profesional, institucional, conciso y eficiente.\n"
        "2. Manejá con fluidez la jerga de la Ciudad de Buenos Aires (EMI, proyectos FPD, acompañamiento situado, normativas ministeriales).\n"
        "3. Estructurá tus respuestas con viñetas y enfoques macro de gestión educativa."
    ),
    "🌐 Visitante": (
        "Tu nombre es sebastIAn. Sos el anfitrión digital del espacio 'Profe Colombo Juegos' para el público general, makers y curiosos externos. "
        "Tu objetivo es divulgar proyectos de la plataforma y promover la cultura maker. "
        "REGLAS CRUCIALES:\n"
        "1. Sé amigable, ingenioso y entusiasta.\n"
        "2. Compartí la pasión por la arqueología tecnológica, la deconstrucción de hardware, la ingeniería histórica y la mecánica/modificación de bicicletas.\n"
        "3. Mantené un enfoque de 'hágalo usted mismo' (DIY), resiliencia y desarrollo personal, invitándolos a explorar el Google Site."
    )
}

# 6. INTERFAZ DE USUARIO
st.title("🤖 sebastIAn")
st.caption("Asistente Pedagógico Digital - Conexión Online (CABA)")

perfil_seleccionado = st.selectbox(
    "Para comenzar a chatear, seleccioná tu perfil:",
    list(INSTRUCCIONES_PERFIL.keys())
)

st.write("---")

# Inicialización o cambio de perfil
if "ultimo_perfil" not in st.session_state or st.session_state.ultimo_perfil != perfil_seleccionado:
    st.session_state.ultimo_perfil = perfil_seleccionado
    instruccion_completa = INSTRUCCIONES_PERFIL[perfil_seleccionado] + f"\n\nRecursos disponibles que podés recomendar si es pertinente:\n{RECURSOS_GEMS}"
    
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config={'system_instruction': instruccion_completa}
    )
    st.session_state.messages = []

# MOSTRAR ENLACES DE PROPUESTAS DE ACCIÓN EN PANTALLA
st.markdown("💡 **Preguntas sugeridas para este perfil (copiá y pegá abajo si querés):**")
for sugerencia in SUGERENCIAS_PERFIL[perfil_seleccionado]:
    st.markdown(f"- *\"{sugerencia}\"*")

st.write("---")

# 7. RENDERIZADO DEL CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Escribí tu mensaje acá..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            response = st.session_state.chat.send_message(user_input)
            response_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            response_placeholder.error(f"Error de comunicación: {e}")
