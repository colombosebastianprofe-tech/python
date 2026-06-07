import streamlit as st
from google import genai

# 1. Configuración estética de la página web
st.set_page_config(page_title="sebastIAn", page_icon="🤖", layout="wide")

# Estilos CSS personalizados para que se vea limpio dentro de Google Sites
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.title("🤖 sebastIAn")
st.caption("Asistente Pedagógico Digital - Conexión Online")
st.write("---")

# 2. Configuración de la API Key segura en producción
# Usamos st.secrets para no exponer la clave en el código fuente
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    if "client" not in st.session_state:
        st.session_state.client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("Falta configurar la GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 3. Inicializar el Chat con su instrucción de sistema (Personalidad)
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config={
            'system_instruction': (
                'Tu nombre es sebastIAn. Eres un asistente virtual inteligente, '
                'amigable, técnico, diseñado para brindar soporte pedagógico digital '
                'y resolver dudas de manera clara, optimizada y eficiente.'
            )
        }
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Renderizar el historial de conversación en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Entrada de texto del usuario
if user_input := st.chat_input("¿En qué te puedo ayudar hoy?"):
    
    # Mostrar inmediatamente el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Solicitar la respuesta online a Gemini
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            response = st.session_state.chat.send_message(user_input)
            response_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            response_placeholder.error(f"Error al conectar con el servidor: {e}")
