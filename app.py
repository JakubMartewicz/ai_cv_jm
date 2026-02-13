import os
import streamlit as st
from openai import OpenAI

st.write("streamlit version:", st.__version__)
st.write("has chat_message:", hasattr(st, "chat_message"))
st.write("has chat_input:", hasattr(st, "chat_input"))

st.set_page_config(page_title="Jakub Martewicz – AI CV Chat", page_icon="💬")
st.title("💬 Jakub Martewicz AI CV Chat")
st.caption("Zadaj pytanie o moje zawodowe doświadczenie. Odpowiadam na podstawie mojego CV:)")

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
        {"role": "system", "content": system_prompt}
    ]

question = st.chat_input("Np. Jakie mam doświadczenie we wdrożeniach SAP SuccessFactors?")

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
    if m["role"] == "system":
        continue  # system_prompt ma być niewidoczny w UI
    with st.chat_message(m["role"]):
        st.markdown(m["content"])








