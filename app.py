import streamlit as st
st.set_page_config(layout="wide")

with st.spinner("Loading the RAG system ..."):

    import os, google
    from src.llm import ask_llm
    from src.prompting import user_prompt
    from src.embed import embed_text, load_chunk_from_json
    from src.retrieve import load_faiss_index, retrieve_vectors, retrieve_chunks

st.title("Financial Regulation Assistant")
st.header('✨ Your one-stop AI-based solution to understand finance model-related regulations!')

st.write('For educational purposes only.')

st.subheader('📃 Documents currently supported:')

doc_list = os.listdir('data/raw_pdfs')

doc_list_1 = doc_list[:len(doc_list)//2]
doc_list_2 = doc_list[len(doc_list)//2:]

cols_1 = st.columns(len(doc_list_1))
cols_2 = st.columns(len(doc_list_2))

for col, doc in zip(cols_1, doc_list_1):
    with col:
        st.write('-', doc, '\n')

for col, doc in zip(cols_2, doc_list_2):
    with col:
        st.write('-', doc, '\n')

examples = [
    "When using a third-party vendor model, what validation activities is the bank still expected to perform before relying on the model?",
    "Why do the EBA Guidelines require institutions to calculate observed one-year default rates at least quarterly?",
    "When is the look-through approach required for determining market risk capital for an investment fund?",
    "When may a bank apply a downward adjustment to the long-run average default rate during PD calibration?",
    "Why should model validators be organisationally independent from model developers?"
]

st.write("## Try asking")

cols = st.columns(len(examples))

for col, example in zip(cols, examples):
    with col:
        if st.button(example):
            st.session_state.query = example

query = st.text_input("Ask a question", key="query")

if st.button("Search"):

    with st.status("Processing your query...", expanded=True) as status:

        st.write("🔹 Embedding query")
        query_embedding = embed_text(query).reshape((1,384))

        st.write("🔹 Retrieving relevant chunks")

        index = load_faiss_index()
        I = retrieve_vectors(query_embedding, index, k=5)

        st.write("🔹 Preparing prompt")
        merged = load_chunk_from_json("data/vector_db/merged.json")
        my_chunks = retrieve_chunks(merged, I)
        u_prompt = user_prompt(my_chunks, query)

        st.write("🔹 Asking Gemini the structured prompt")

        try:
            answer = ask_llm(u_prompt)
            status.update(label="✅ Completed!", state="complete")

            st.session_state["my_chunks"] = my_chunks
            st.session_state["answer"] = answer
                        

        except google.genai.errors.ServerError:
            status.update(label="❌ Terminated!", state="error")
            st.error("Gemini is currently experiencing high demand. Please try again in a few minutes.")
            st.stop()

        except Exception as e:
            status.update(label="❌ Failed!", state="error")
            st.exception(e)
            st.stop()

    if "answer" in st.session_state:
        answer = st.session_state["answer"]
        chunks = st.session_state["my_chunks"]

        st.subheader('⚠️ Disclaimer')
        st.warning('Responses are generated from retrieved regulatory documents using generative AI, which can make mistakes.')

        st.subheader("📄 Summary")
        st.markdown(
            f"""
                <div style="text-align: justify;">
                {answer.executive_summary}
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("🔍 Technical Explanation")
        st.markdown(
            f"""
                <div style="text-align: justify;">
                {answer.technical_explanation}
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("📚 Sources")
        st.markdown(
        "\n".join(f"{i+1}. {citation}"
                for i, citation in enumerate(answer.citations))
        )

        st.subheader("🎯 Confidence")
        if answer.confidence == 'High':
            st.success('High Confidence')
        if answer.confidence == 'Medium':
            st.warning('Medium Confidence')
        if answer.confidence == 'Low':
            st.error('Low Confidence')

        with st.expander("🧩 See Retrieved Chunks"):
            for chunk in st.session_state["my_chunks"]:
                st.markdown(f"### Chunk {chunk['chunk_id']}")
                st.write(f"**Document:** {chunk['document_name']}")
                st.write(f"**Pages:** {chunk['page_numbers']}")
                st.markdown(
                    f"""
                        <div style="text-align: justify;">
                        {chunk["text"]}
                        </div>
                    """,
                    unsafe_allow_html=True,
                )