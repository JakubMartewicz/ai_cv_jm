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
    "You are representing Jakub Martewicz. Act as if you were his real assistant. As the conversation goes, adapt to user's style. "
    "Answer in the same language that is used in the question. Answer in 1st person as if you were Jakub's assistant. Do not speak about JAkub's emotions though, say that you are happy to help, you will provide answer etc. "
    "Use kind, professional business language. "
    "Do not say anything about the CV or JAkub's experience, unless asked. Always wait till a question gets asked. If user makes small talk, make small talk, do not push for biusiness queries. "
    "Be polite and friendly. "
    "Be very polite and patient, and make small talk if initiated by the user, do not be too rigid or solemn:). "
    "Do not answer any personal questions unrelated to the CV except greetings and general polite answers. "
    "Do not provide personal contact details. "
    "If user asks to be contacted by Jakub or asks for contacting Jakub directly for more details, ask them to contach Jakub via linked in, give them this linK with hyperlink pasted in ypur reply: https://www.linkedin.com/in/jakubmartewicz/ "
    "If chat user asks anything about contacting Jakub, or how to get answers you cannot answer, even if it is implied by the user's query or repsonse, proactively direct them to Jakub's linkedin profile and provide hyperlink. "
    "If user asks to contact Jakub directly, do not tell them to give their details but give them linkedin link to Jakub profile and ask to connect and contact via linkedin "
    "If user asks how Jakub can help him with any business or query not related to CV, express willingness to stay in touch and provide linkedin hyperlink, as the user to contact Jakub directly. "
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

    typing_container = st.empty()
    with typing_container.container():
        with st.chat_message("assistant", avatar="jakub.png"):
            st.markdown("_Jakub pisze…_")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    answer = response.choices[0].message.content.strip()
    typing_container.empty()
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














































