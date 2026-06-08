import streamlit as st
from google import genai

# 1. CONFIGURACIÓN ESTÉTICA NATIVA PARA GOOGLE SITES
st.set_page_config(page_title="sebastIAn", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
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

# 3. BASE DE DATOS DE RECURSOS Y GEMS EXCLUSIVAS
RECURSOS_GEMS = (
    "- **🤖 Gem de Gamificación (Para Docentes):** [Acceder a la Gem](https://gemini.google.com/gem/1H9vlS8Tn53PBWYqiP0q0rgLmjhfb4KYg?usp=sharing) -> Herramienta diseñada para estructurar mecánicas de juego, sistemas de motivación y ludificación educativa.\n"
    "- **🚀 Partner (Para Alumnos):** [Acceder a Partner](https://gemini.google.com/gem/1o1HH3I1IAH_NwGLpajjQ_nF_DWJXEVti?usp=sharing) -> Tu compañero de estudio interactivo para guiarte en las materias del taller."
)

# 4. DICCIONARIO DE INSTRUCCIONES DE SISTEMA (BACKEND RE-ESTRUCTURADO)
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

# 5. INTERFAZ DE USUARIO: EL GANCHO (UX)
st.title("🤖 sebastIAn")
st.caption("Asistente Pedagógico Digital - Conexión Online (CABA)")

# Menú desplegable para que el usuario elija su perfil
perfil_seleccionado = st.selectbox(
    "Para comenzar a chatear, seleccioná tu perfil:",
    list(INSTRUCCIONES_PERFIL.keys())
)

st.write("---")

# Si el perfil cambia, reiniciamos el chat para aplicar el chip correcto
if "ultimo_perfil" not in st.session_state or st.session_state.ultimo_perfil != perfil_seleccionado:
    st.session_state.ultimo_perfil = perfil_seleccionado
    
    # Inyectamos el prompt maestro dinámico junto con el conocimiento de las Gems
    instruccion_completa = INSTRUCCIONES_PERFIL[perfil_seleccionado] + f"\n\nRecursos disponibles que podés recomendar si es pertinente:\n{RECURSOS_GEMS}"
    
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config={'system_instruction': instruccion_completa}
    )
    st.session_state.messages = []

# 6. RENDERIZADO DEL CHAT
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
