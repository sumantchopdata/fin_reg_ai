import streamlit as st
from llm import ask_llm
import json

st.title("Financial Regulation Assistant")

query = st.text_input("Ask a question")

if st.button("Search"):

    answer = ask_llm(query)
    answer = json.loads(answer.replace("```json", "").replace("```", "").strip())

    st.write(answer["executive_summary"])

    st.subheader("Technical Explanation")
    st.write(answer["technical_explanation"])

    st.subheader("Sources")
    st.write(answer["citations"])

    st.subheader("Confidence")
    st.write(answer["confidence"])