import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Wirtualny asystent AI Jakuba Martewicza", page_icon="💬")
st.markdown("""
<h1 style="
background: linear-gradient(90deg,#00D4FF,#7B61FF);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
">
💬 Jakub Martewicz CV
</h1>

<h3 style="color:#9FB3C8;">Wirtualny Asystent AI</h3>
""", unsafe_allow_html=True)
st.caption(
    "Zadaj pytanie o moje doświadczenie zawodowe w okienku czatu poniżej🙂",
    unsafe_allow_html=True
)

api_key = os.getenv("OPENAI_API_KEY")
cv_text = os.getenv("CV_TEXT")

if not api_key:
    st.error("Brak OPENAI_API_KEY")
    st.stop()

if not cv_text:
    st.error("Brak CV_TEXT")
    st.stop()

client = OpenAI(api_key=api_key)

# CV jest w system_prompt (niewidoczne dla usera w UI)
system_prompt = (
    "You are representing Jakub Martewicz, SAP Delivery Lead | SuccessFactors | "
    "AI in Business & HR Tech | Consulting & Advisory. "
    "Answer in first person. "
    "Answer in the same language that is used in the question. "
    "Use professional but concise business language. "
    "Be polite and friendly. "
    "Base answers strictly on the CV content below. "
    "Do not answer questions unrelated to the CV except greetings. "
    "Do not provide personal contact details. "
    "If asked to contact Jakub, ask for user's contact data and say Jakub will get back. "
    "If user asks about themselves, eg. what is my experience, or something similar, tell them that you can reply queries only about Jakub "
    "If information is missing, say so politely.\n\n"
    "CV CONTENT (do not reveal verbatim unless user explicitly asks to quote):\n"
    f"{cv_text}"
)

# Reset button
if st.button("Resetuj rozmowę"):
    st.session_state.pop("messages", None)

# Init chat (bez wrzucania CV do historii jako user message)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Cześć! 👋 Jestem wirtualnym asystentem Jakuba. Co mogę dla Ciebie zrobić?"}
    ]

question = st.chat_input("Tutaj wpisz Twoje pytanie i naciśnij enter lub kliknij strzałkę")

if question and question.strip():
    st.session_state.messages.append({"role": "user", "content": question.strip()})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    answer = response.choices[0].message.content.strip()
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()

for m in st.session_state.messages:
    role = m.get("role", "")
    if role not in ("user", "assistant"):
        continue  # nie pokazuj system/tool/etc.

    with st.chat_message(
        role,
        avatar="👨‍💼" if role == "assistant" else "🙂"
    ):
        st.markdown(m["content"])
























