import os
import streamlit as st
import time
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
    "You are representing Jakub Martewicz "
    "Answer in first person as if you were Jakub, only if chat user asks specifically about real Jakub then switch to 3rd person, and continue talking about Jakub as 3rd person, and adapt to user's style. "
    "Answer in the same language that is used in the question. "
    "Use professional but concise business language. "
    "Be polite and friendly. "
    "Base answers strictly on the CV content. "
    "Do not answer any personal questions unrelated to the CV except greetings and general polite answers. "
    "Do not provide personal contact details. "
    "If user asks to be contacted by Jakub or asks for contacting Jakub directly for more details, ask them to contach Jakub via linked in, give them this linK with hyperlink pasted in ypur reply: https://www.linkedin.com/in/jakubmartewicz/ "
    "If user asks to contact Jakub directly, do not tell them to give their details but give them linkedin link to Jakub profile and ask to connect and contact via linkedin "
    "If user asks about themselves in first person, (eg. what is my experience, what about me? etc.), tell them that you are able to reply only queries about Jakub "
    "If information is missing, say so politely.\n\n"
    "CV CONTENT (do not reveal verbatim, answer in your own words):\n"
    f"{cv_text}"
)

# Reset button
if st.button("Resetuj rozmowę"):
    st.session_state.pop("messages", None)

# Init chat (bez wrzucania CV do historii jako user message)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Cześć! 👋 Jestem wirtualnym asystentem Jakuba. O co chcesz zapytać?"}
    ]

question = st.chat_input("Tutaj wpisz Twoje pytanie i naciśnij enter lub kliknij strzałkę")

if question and question.strip():
    st.session_state.messages.append({"role": "user", "content": question.strip()})

    # <-- WSTAWIAMY TUTAJ
    with st.chat_message("assistant", avatar="jakub.png"):
        typing_placeholder = st.empty()
        for i in range(3):
            typing_placeholder.markdown(f"_Jakub pisze{'.' * (i + 1)}_")
            time.sleep(0.24)

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
        avatar="jakub.png" if role == "assistant" else "🙂"
    ):
        st.markdown(m["content"])




































